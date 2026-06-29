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

class SetupWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Setup - SETJA")
        self.geometry("500x380")
        self.resizable(False, False)
        
        # Ensure icon if exists, otherwise default
        self.mode_var = tk.StringVar(value="full")
        self.current_step = 0
        
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", side="bottom")
        
        self.bottom_bar = tk.Frame(self, bg="#f0f0f0")
        self.bottom_bar.pack(fill="x", side="bottom")
        
        self.btn_cancel = ttk.Button(self.bottom_bar, text="Cancel", command=self.cancel_setup)
        self.btn_cancel.pack(side="right", padx=10, pady=12)
        
        self.btn_next = ttk.Button(self.bottom_bar, text="Next >", command=self.next_step)
        self.btn_next.pack(side="right", padx=0, pady=12)
        
        self.btn_back = ttk.Button(self.bottom_bar, text="< Back", command=self.prev_step)
        self.btn_back.pack(side="right", padx=5, pady=12)

        self.pages = []
        self.build_welcome_page()
        self.build_mode_page()
        self.build_ready_page()
        self.build_install_page()
        self.build_finish_page()
        
        self.show_page(0)

    def cancel_setup(self):
        if messagebox.askyesno("Exit Setup", "Setup is not complete. If you exit now, the program will not be installed.\n\nExit Setup?"):
            self.destroy()

    def show_page(self, index):
        for p in self.pages:
            p.pack_forget()
            
        self.pages[index].pack(fill="both", expand=True)
        self.current_step = index
        
        if index == 0:
            self.btn_back.config(state="disabled")
            self.btn_next.config(text="Next >", state="normal")
        elif index == 1:
            self.btn_back.config(state="normal")
            self.btn_next.config(text="Next >", state="normal")
        elif index == 2:
            self.btn_back.config(state="normal")
            self.btn_next.config(text="Install", state="normal")
            self.update_ready_summary()
        elif index == 3:
            self.btn_back.config(state="disabled")
            self.btn_next.config(state="disabled")
            self.btn_cancel.config(state="disabled")
            self.start_installation()
        elif index == 4:
            self.btn_back.pack_forget()
            self.btn_cancel.pack_forget()
            self.btn_next.config(text="Finish", command=self.destroy, state="normal")

    def next_step(self):
        if self.current_step < len(self.pages) - 1:
            self.show_page(self.current_step + 1)

    def prev_step(self):
        if self.current_step > 0:
            self.show_page(self.current_step - 1)

    def build_welcome_page(self):
        page = tk.Frame(self.container, bg="#ffffff")
        self.pages.append(page)
        
        left_pane = tk.Frame(page, bg="#0b2866", width=160)
        left_pane.pack(side="left", fill="y")
        left_pane.pack_propagate(False)
        
        # "SETJA" vertical text or logo placeholder
        tk.Label(left_pane, text="SETJA\nAI", font=("Segoe UI", 24, "bold"), bg="#0b2866", fg="white").pack(pady=40)
        
        right_pane = tk.Frame(page, bg="#ffffff", padx=20, pady=20)
        right_pane.pack(side="right", fill="both", expand=True)
        
        tk.Label(right_pane, text="Welcome to the SETJA\nSetup Wizard", font=("Segoe UI", 16, "bold"), bg="#ffffff", justify="left", anchor="w").pack(fill="x", pady=(10, 20))
        tk.Label(right_pane, text="This will install SETJA v1.0 on your computer.", font=("Segoe UI", 9), bg="#ffffff", justify="left", anchor="w").pack(fill="x", pady=5)
        tk.Label(right_pane, text="It is recommended that you close all other applications before continuing.", font=("Segoe UI", 9), bg="#ffffff", justify="left", anchor="w", wraplength=280).pack(fill="x", pady=5)
        tk.Label(right_pane, text="Click Next to continue, or Cancel to exit Setup.", font=("Segoe UI", 9), bg="#ffffff", justify="left", anchor="w").pack(fill="x", pady=(20, 5))

    def create_top_banner(self, parent, title, subtitle):
        banner = tk.Frame(parent, bg="#ffffff", height=60)
        banner.pack(fill="x", side="top")
        banner.pack_propagate(False)
        tk.Label(banner, text=title, font=("Segoe UI", 10, "bold"), bg="#ffffff", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        tk.Label(banner, text=subtitle, font=("Segoe UI", 9), bg="#ffffff", anchor="w").pack(fill="x", padx=35)
        ttk.Separator(parent, orient="horizontal").pack(fill="x", side="top")

    def build_mode_page(self):
        page = tk.Frame(self.container, bg="#f0f0f0")
        self.pages.append(page)
        
        self.create_top_banner(page, "Installation Mode", "Please select how you want to install SETJA.")
        
        content = tk.Frame(page, bg="#f0f0f0", padx=30, pady=20)
        content.pack(fill="both", expand=True)
        
        tk.Label(content, text="Select the components you want to install:", font=("Segoe UI", 9), bg="#f0f0f0").pack(anchor="w", pady=(0, 10))
        
        r1 = tk.Radiobutton(content, text="Full Installation (Offline Local Model + Online API)", variable=self.mode_var, value="full", font=("Segoe UI", 9), bg="#f0f0f0", activebackground="#f0f0f0")
        r1.pack(anchor="w", pady=5)
        
        r2 = tk.Radiobutton(content, text="Online API Only (Lightweight, Saves ~5GB of space)", variable=self.mode_var, value="online", font=("Segoe UI", 9), bg="#f0f0f0", activebackground="#f0f0f0")
        r2.pack(anchor="w", pady=5)
        
        r3 = tk.Radiobutton(content, text="Local Offline Model Only (Strict Privacy Mode)", variable=self.mode_var, value="offline", font=("Segoe UI", 9), bg="#f0f0f0", activebackground="#f0f0f0")
        r3.pack(anchor="w", pady=5)

    def build_ready_page(self):
        page = tk.Frame(self.container, bg="#f0f0f0")
        self.pages.append(page)
        
        self.create_top_banner(page, "Ready to Install", "Setup is now ready to begin installing SETJA on your computer.")
        
        content = tk.Frame(page, bg="#f0f0f0", padx=30, pady=20)
        content.pack(fill="both", expand=True)
        
        tk.Label(content, text="Click Install to continue with the installation.", font=("Segoe UI", 9), bg="#f0f0f0").pack(anchor="w", pady=(0, 10))
        
        self.summary_text = tk.Text(content, height=8, width=40, font=("Consolas", 9), state="disabled")
        self.summary_text.pack(fill="both", expand=True)

    def update_ready_summary(self):
        mode = self.mode_var.get()
        summary = "Installation Type:\n"
        if mode == "full":
            summary += "  Full Installation\n\nComponents to install:\n  - Core Application (UI, Capture, OCR)\n  - Local AI Translation Models\n  - Online API Fallback Support\n\nDisk Space Required: ~6 GB"
        elif mode == "online":
            summary += "  Online API Only\n\nComponents to install:\n  - Core Application (UI, Capture, OCR)\n  - Online API Support\n\nDisk Space Required: ~1 GB"
        else:
            summary += "  Local Offline Model Only\n\nComponents to install:\n  - Core Application (UI, Capture, OCR)\n  - Local AI Translation Models\n\nDisk Space Required: ~6 GB"
            
        self.summary_text.config(state="normal")
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)
        self.summary_text.config(state="disabled")

    def build_install_page(self):
        page = tk.Frame(self.container, bg="#f0f0f0")
        self.pages.append(page)
        
        self.create_top_banner(page, "Installing", "Please wait while Setup installs SETJA on your computer.")
        
        content = tk.Frame(page, bg="#f0f0f0", padx=30, pady=20)
        content.pack(fill="both", expand=True)
        
        self.lbl_progress = tk.Label(content, text="Preparing to install...", font=("Segoe UI", 9), bg="#f0f0f0")
        self.lbl_progress.pack(anchor="w", pady=(0, 5))
        
        self.progress = ttk.Progressbar(content, mode="indeterminate")
        self.progress.pack(fill="x", pady=5)
        
        self.log_text = tk.Text(content, height=6, font=("Consolas", 8), bg="#ffffff", fg="#333333", state="disabled")
        self.log_text.pack(fill="both", expand=True, pady=(10, 0))

    def build_finish_page(self):
        page = tk.Frame(self.container, bg="#ffffff")
        self.pages.append(page)
        
        left_pane = tk.Frame(page, bg="#0b2866", width=160)
        left_pane.pack(side="left", fill="y")
        left_pane.pack_propagate(False)
        tk.Label(left_pane, text="SETJA\n✓", font=("Segoe UI", 28, "bold"), bg="#0b2866", fg="white").pack(pady=40)
        
        right_pane = tk.Frame(page, bg="#ffffff", padx=20, pady=20)
        right_pane.pack(side="right", fill="both", expand=True)
        
        tk.Label(right_pane, text="Completing the SETJA\nSetup Wizard", font=("Segoe UI", 16, "bold"), bg="#ffffff", justify="left", anchor="w").pack(fill="x", pady=(10, 20))
        
        self.finish_lbl1 = tk.Label(right_pane, text="Setup has finished installing SETJA on your computer. The application may be launched by running main.cmd.", font=("Segoe UI", 9), bg="#ffffff", justify="left", anchor="w", wraplength=280)
        self.finish_lbl1.pack(fill="x", pady=5)
        
        tk.Label(right_pane, text="Click Finish to exit Setup.", font=("Segoe UI", 9), bg="#ffffff", justify="left", anchor="w").pack(fill="x", pady=(20, 5))

    def log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        self.lbl_progress.config(text=msg)

    def run_cmd(self, cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=str(ROOT))
        for line in process.stdout:
            self.log(line.strip())
        process.wait()
        return process.returncode == 0

    def start_installation(self):
        self.progress.start(10)
        threading.Thread(target=self.install_worker, daemon=True).start()

    def install_worker(self):
        mode = self.mode_var.get()
        
        if not PYTHON_EXE.exists():
            self.log("Creating Virtual Environment...")
            if not self.run_cmd(f'"{sys.executable}" -m venv setja_stable'):
                self.fail_installation()
                return
                
        self.log("Upgrading pip...")
        self.run_cmd(f'"{PYTHON_EXE}" -m pip install --upgrade pip')
        
        self.log("Installing Core Application Files...")
        if not self.run_cmd(f'"{PYTHON_EXE}" -m pip install -r req_core.txt'):
            self.fail_installation()
            return
            
        enable_offline = mode in ("full", "offline")
        if enable_offline:
            self.log("Installing Local AI Translation Models...")
            if not self.run_cmd(f'"{PYTHON_EXE}" -m pip install -r req_offline.txt'):
                self.fail_installation()
                return
                
        custom_req = ROOT / "req_custom_model.txt"
        if custom_req.exists():
            self.log("Installing Custom Client Models...")
            self.run_cmd(f'"{PYTHON_EXE}" -m pip install -r req_custom_model.txt')
            
        self.log("Configuring System Settings...")
        self.update_settings(mode, enable_offline)
        
        self.progress.stop()
        self.lbl_progress.config(text="Installation Complete!")
        self.after(1000, lambda: self.show_page(4))

    def fail_installation(self):
        self.progress.stop()
        self.lbl_progress.config(text="Installation Failed!")
        self.btn_cancel.config(text="Close", command=self.destroy, state="normal")
        messagebox.showerror("Setup Error", "An error occurred during installation. Please check the log.")

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
        if mode == "online" and settings.get("engine", "offline") == "offline":
            settings["engine"] = "gemini"
            
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

if __name__ == "__main__":
    app = SetupWizard()
    app.mainloop()
