import os
import sys
import json
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil

class SetjaControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SETJA Control Panel - CEO Edition")
        self.geometry("600x500")
        self.configure(bg="#1e1e2e")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        
        # Colors
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.btn_color = "#313244"
        
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        self.style.configure("TButton", background=self.btn_color, foreground=self.fg_color, font=("Segoe UI", 10, "bold"), borderwidth=0)
        self.style.map("TButton", background=[("active", self.accent_color)])
        self.style.configure("TRadiobutton", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        
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
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Label(main_frame, text="SETJA - Advanced Screen Translator", bg=self.bg_color, fg=self.accent_color, font=("Segoe UI", 16, "bold"))
        header.pack(pady=(0, 20))
        
        # Engine Selection
        engine_frame = ttk.LabelFrame(main_frame, text=" Translation Engine ", padding=15)
        engine_frame.pack(fill=tk.X, pady=10)
        
        self.engine_var = tk.StringVar(value=self.settings.get("engine", "offline"))
        r1 = ttk.Radiobutton(engine_frame, text="Offline (Local AI Models - Strict Privacy)", variable=self.engine_var, value="offline", command=self.on_engine_change)
        r1.pack(anchor=tk.W, pady=2)
        r2 = ttk.Radiobutton(engine_frame, text="Online (Gemini API - High Speed)", variable=self.engine_var, value="gemini", command=self.on_engine_change)
        r2.pack(anchor=tk.W, pady=2)
        
        # API Key
        self.api_frame = ttk.Frame(engine_frame)
        ttk.Label(self.api_frame, text="Gemini API Key:").pack(side=tk.LEFT, padx=(0, 10))
        self.api_entry = ttk.Entry(self.api_frame, width=40)
        self.api_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.api_entry.insert(0, self.settings.get("api_key", ""))
        
        if self.engine_var.get() == "gemini":
            self.api_frame.pack(fill=tk.X, pady=10)
            
        # Model Installer
        model_frame = ttk.LabelFrame(main_frame, text=" Model Management ", padding=15)
        model_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(model_frame, text="Want to use a custom CTranslate2 model?").pack(side=tk.LEFT)
        ttk.Button(model_frame, text="Browse & Install Model", command=self.install_model).pack(side=tk.RIGHT)
        
        # Start/Stop Button
        self.start_btn = tk.Button(main_frame, text="START SETJA", bg="#a6e3a1", fg="#11111b", font=("Segoe UI", 14, "bold"), borderwidth=0, cursor="hand2", command=self.toggle_setja)
        self.start_btn.pack(fill=tk.X, pady=30, ipady=10)
        
    def on_engine_change(self):
        if self.engine_var.get() == "gemini":
            self.api_frame.pack(fill=tk.X, pady=10)
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
                messagebox.showerror("Error", f"Python environment not found at: {self.py_exe}\nPlease run Setup first.")
                return
                
            self.start_btn.config(text="STOP SETJA", bg="#f38ba8")
            self.is_running = True
            threading.Thread(target=self.run_processes, daemon=True).start()
        else:
            self.stop_processes()
            self.start_btn.config(text="START SETJA", bg="#a6e3a1")
            self.is_running = False
            
    def run_processes(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = self.src_dir
        
        cmds = [
            # Region Selector
            {"cmd": ["cmd", "/c", "run_selector.cmd"], "cwd": os.path.join(self.src_dir, "capture", "region_selector")},
            # Screen Capture EXE
            {"cmd": [os.path.join(self.src_dir, "capture", "screen_capture", "app", "screen_capture.exe")], "cwd": self.src_dir},
            # OCR
            {"cmd": [self.py_exe, "-u", os.path.join(self.src_dir, "ocr", "app", "ocr_main.py")], "cwd": self.src_dir},
            # Translator
            {"cmd": [self.py_exe, "-u", "-m", "app.t_main"], "cwd": os.path.join(self.src_dir, "translator")},
            # TXT Viewer Base
            {"cmd": [self.py_exe, "-u", "txt_viewer.py"], "cwd": os.path.join(self.src_dir, "txt_viewer")},
            # TXT Viewer Overlay
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
