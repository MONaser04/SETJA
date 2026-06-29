import os
import sys
import json
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import customtkinter as ctk

# Set modern appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SetjaControlPanel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SETJA Control Panel - CEO Edition")
        self.geometry("650x550")
        
        self.processes = []
        self.is_running = False
        
        self.root_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.src_dir = os.path.join(self.root_dir, "src")
        self.py_exe = os.path.join(self.root_dir, "setja_stable", "Scripts", "python.exe")
        self.settings_path = os.path.join(self.src_dir, "settings.json")
        
        self.load_settings()
        self.build_ui()
        
    def load_settings(self):
        self.settings = {"engine": "offline", "enable_offline": True, "api_key": ""}
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    self.settings.update(json.load(f))
            except Exception as e:
                print(f"Error loading settings: {e}")
                
    def save_settings(self):
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def build_ui(self):
        # Header
        self.header_label = ctk.CTkLabel(self, text="SETJA Advanced Screen Translator", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=(20, 10))
        self.sub_label = ctk.CTkLabel(self, text="Manage Translation Engines and Models", font=ctk.CTkFont(size=14), text_color="gray")
        self.sub_label.pack(pady=(0, 20))
        
        # Engine Frame
        self.engine_frame = ctk.CTkFrame(self)
        self.engine_frame.pack(fill="x", padx=20, pady=10)
        
        self.engine_label = ctk.CTkLabel(self.engine_frame, text="Translation Engine", font=ctk.CTkFont(size=16, weight="bold"))
        self.engine_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        self.engine_var = ctk.StringVar(value=self.settings.get("engine", "offline"))
        
        self.radio_offline = ctk.CTkRadioButton(self.engine_frame, text="Offline (Local AI Models - Strict Privacy)", variable=self.engine_var, value="offline", command=self.on_engine_change)
        self.radio_offline.pack(anchor="w", padx=30, pady=5)
        
        self.radio_online = ctk.CTkRadioButton(self.engine_frame, text="Online (Gemini API - High Speed)", variable=self.engine_var, value="gemini", command=self.on_engine_change)
        self.radio_online.pack(anchor="w", padx=30, pady=5)
        
        # API Key Frame
        self.api_frame = ctk.CTkFrame(self.engine_frame, fg_color="transparent")
        
        self.api_label = ctk.CTkLabel(self.api_frame, text="Gemini API Key:")
        self.api_label.pack(side="left", padx=(30, 10))
        
        self.api_entry = ctk.CTkEntry(self.api_frame, width=300, placeholder_text="Enter your API key here...")
        self.api_entry.pack(side="left", fill="x", expand=True, padx=(0, 30))
        self.api_entry.insert(0, self.settings.get("api_key", ""))
        
        if self.engine_var.get() == "gemini":
            self.api_frame.pack(fill="x", pady=10)
            
        # Model Management Frame
        self.model_frame = ctk.CTkFrame(self)
        self.model_frame.pack(fill="x", padx=20, pady=10)
        
        self.model_label = ctk.CTkLabel(self.model_frame, text="Model Management", font=ctk.CTkFont(size=16, weight="bold"))
        self.model_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        self.model_sub_label = ctk.CTkLabel(self.model_frame, text="Want to use a custom CTranslate2 model?")
        self.model_sub_label.pack(side="left", padx=30, pady=15)
        
        self.install_btn = ctk.CTkButton(self.model_frame, text="Browse & Install Model", command=self.install_model)
        self.install_btn.pack(side="right", padx=30, pady=15)
        
        # Start Button
        self.start_btn = ctk.CTkButton(self, text="START SETJA", font=ctk.CTkFont(size=18, weight="bold"), height=50, fg_color="#2ecc71", hover_color="#27ae60", text_color="white", command=self.toggle_setja)
        self.start_btn.pack(fill="x", padx=20, pady=(30, 20))
        
    def on_engine_change(self):
        if self.engine_var.get() == "gemini":
            self.api_frame.pack(fill="x", pady=10)
        else:
            self.api_frame.pack_forget()
            
    def install_model(self):
        filepath = filedialog.askopenfilename(title="Select Model File", filetypes=[("CTranslate2 Bin", "*.bin"), ("All Files", "*.*")])
        if filepath:
            target_dir = os.path.join(self.src_dir, "translator", "core", "translator_model")
            os.makedirs(target_dir, exist_ok=True)
            try:
                shutil.copy(filepath, os.path.join(target_dir, "model.bin"))
                messagebox.showinfo("Success", "Custom model installed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to install model: {e}")
                
    def toggle_setja(self):
        if not self.is_running:
            # Save settings
            self.settings["engine"] = self.engine_var.get()
            self.settings["enable_offline"] = (self.engine_var.get() == "offline")
            self.settings["api_key"] = self.api_entry.get().strip()
            self.save_settings()
            
            if not os.path.exists(self.py_exe):
                messagebox.showerror("Error", f"Python environment not found at:\n{self.py_exe}\n\nPlease run Setup first.")
                return
                
            self.start_btn.configure(text="STOP SETJA", fg_color="#e74c3c", hover_color="#c0392b")
            self.is_running = True
            threading.Thread(target=self.run_processes, daemon=True).start()
        else:
            self.stop_processes()
            self.start_btn.configure(text="START SETJA", fg_color="#2ecc71", hover_color="#27ae60")
            self.is_running = False
            
    def run_processes(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = self.src_dir
        
        cmds = [
            {"cmd": ["cmd", "/c", "run_selector.cmd"], "cwd": os.path.join(self.src_dir, "capture", "region_selector")},
            {"cmd": [os.path.join(self.src_dir, "capture", "screen_capture", "app", "screen_capture.exe")], "cwd": self.src_dir},
            {"cmd": [self.py_exe, "-u", os.path.join(self.src_dir, "ocr", "app", "ocr_main.py")], "cwd": self.src_dir},
            {"cmd": [self.py_exe, "-u", "-m", "app.t_main"], "cwd": os.path.join(self.src_dir, "translator")},
            {"cmd": [self.py_exe, "-u", "txt_viewer.py"], "cwd": os.path.join(self.src_dir, "txt_viewer")},
            {"cmd": [self.py_exe, "-u", "instant_overlay.py"], "cwd": os.path.join(self.src_dir, "txt_viewer")}
        ]
        
        for c in cmds:
            try:
                p = subprocess.Popen(c["cmd"], cwd=c["cwd"], env=env, creationflags=subprocess.CREATE_NO_WINDOW)
                self.processes.append(p)
            except Exception as e:
                print(f"Failed to start {c['cmd']}: {e}")
                
    def stop_processes(self):
        for p in self.processes:
            try:
                p.terminate()
            except:
                pass
        self.processes.clear()

if __name__ == "__main__":
    app = SetjaControlPanel()
    app.mainloop()
