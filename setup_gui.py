import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import sys
import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / "setja_stable"
PYTHON_EXE = VENV_DIR / "Scripts" / "python.exe"

class SetupGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SETJA - Smart Installer")
        self.geometry("600x450")
        self.configure(padx=20, pady=20)
        
        # Check if already installed
        is_installed = VENV_DIR.exists() and PYTHON_EXE.exists()
        title_text = "Repair / Modify SETJA Installation" if is_installed else "Install SETJA"
        
        tk.Label(self, text=title_text, font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))
        
        # Installation modes
        self.mode_var = tk.StringVar(value="full")
        
        modes_frame = tk.LabelFrame(self, text=" Installation Mode ", font=("Segoe UI", 10), padx=10, pady=10)
        modes_frame.pack(fill="x", pady=10)
        
        tk.Radiobutton(modes_frame, text="Full Installation (Offline Model + Online API)", variable=self.mode_var, value="full", font=("Segoe UI", 10)).pack(anchor="w", pady=5)
        tk.Radiobutton(modes_frame, text="Online API Only (Lightweight, Saves ~5GB)", variable=self.mode_var, value="online", font=("Segoe UI", 10)).pack(anchor="w", pady=5)
        tk.Radiobutton(modes_frame, text="Local Offline Model Only (Privacy focused)", variable=self.mode_var, value="offline", font=("Segoe UI", 10)).pack(anchor="w", pady=5)
        
        # Log Box
        self.log_text = tk.Text(self, height=10, state="disabled", font=("Consolas", 9), bg="#1e1e1e", fg="#cccccc")
        self.log_text.pack(fill="both", expand=True, pady=10)
        
        # Action Button
        self.run_btn = ttk.Button(self, text="Start Setup", command=self.start_setup)
        self.run_btn.pack(pady=5, ipadx=20, ipady=5)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def run_cmd(self, cmd, desc):
        self.log(f"[*] {desc}...")
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=str(ROOT)
        )
        for line in process.stdout:
            self.log("  " + line.strip())
        process.wait()
        if process.returncode != 0:
            self.log(f"[ERROR] Command failed with code {process.returncode}")
            return False
        return True

    def start_setup(self):
        self.run_btn.config(state="disabled")
        for widget in self.winfo_children():
            if isinstance(widget, tk.LabelFrame):
                for child in widget.winfo_children():
                    try:
                        child.config(state="disabled")
                    except tk.TclError:
                        pass
                    
        threading.Thread(target=self.install_process, daemon=True).start()

    def install_process(self):
        mode = self.mode_var.get()
        self.log(f"Starting {mode} installation...")
        
        # 1. Create Virtual Environment
        if not PYTHON_EXE.exists():
            success = self.run_cmd(f'"{sys.executable}" -m venv setja_stable', "Creating Virtual Environment")
            if not success:
                self.setup_finished(False, "Failed to create virtual environment.")
                return
        
        # Upgrade pip
        self.run_cmd(f'"{PYTHON_EXE}" -m pip install --upgrade pip', "Upgrading pip")
        
        # 2. Install Core Requirements
        success = self.run_cmd(f'"{PYTHON_EXE}" -m pip install -r req_core.txt', "Installing Core Requirements")
        if not success:
            self.setup_finished(False, "Failed to install core requirements.")
            return
            
        # 3. Install Offline Requirements if needed
        enable_offline = mode in ("full", "offline")
        if enable_offline:
            success = self.run_cmd(f'"{PYTHON_EXE}" -m pip install -r req_offline.txt', "Installing Offline AI Requirements (This may take a while...)")
            if not success:
                self.setup_finished(False, "Failed to install offline requirements.")
                return
                
        # 4. Install Custom Models if requested (Future expansion)
        custom_req = ROOT / "req_custom_model.txt"
        if custom_req.exists():
            self.run_cmd(f'"{PYTHON_EXE}" -m pip install -r req_custom_model.txt', "Installing Custom Local Models")
            
        # 5. Update settings.json
        self.update_settings(mode, enable_offline)
        
        self.setup_finished(True, "Installation completed successfully!")

    def update_settings(self, mode, enable_offline):
        settings_path = ROOT / "settings.json"
        settings = {}
        if settings_path.exists():
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
            except Exception:
                pass
                
        settings["enable_offline"] = enable_offline
        
        # Auto-configure engine fallback logic
        if mode == "online" and settings.get("engine", "offline") == "offline":
            settings["engine"] = "gemini"  # Default to online api if they chose online only
            
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        
        self.log("[*] Updated settings.json configuration.")

    def setup_finished(self, success, msg):
        self.log("\n" + "="*40)
        self.log(msg)
        if success:
            messagebox.showinfo("Success", msg + "\nYou can now launch SETJA using main.cmd")
        else:
            messagebox.showerror("Error", "Setup encountered errors. Please check the log.")
        self.run_btn.config(state="normal", text="Close", command=self.destroy)

if __name__ == "__main__":
    app = SetupGUI()
    app.mainloop()
