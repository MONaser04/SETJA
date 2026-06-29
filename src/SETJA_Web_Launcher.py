import os
import sys
import json
import subprocess
import threading
import shutil
import webview

class Api:
    def __init__(self):
        self.root_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.src_dir = os.path.join(self.root_dir, "src")
        self.settings_path = os.path.join(self.root_dir, "settings.json")
        py_exe_scripts = os.path.join(self.root_dir, "setja_stable", "Scripts", "python.exe")
        py_exe_bin = os.path.join(self.root_dir, "setja_stable", "bin", "python.exe")
        self.py_exe = py_exe_scripts if os.path.exists(py_exe_scripts) else py_exe_bin
        self.processes = []

        # Ensure settings exist
        if not os.path.exists(self.settings_path):
            self.save_settings({
                "engine": "offline", 
                "api_key": "",
                "api_url": "",
                "api_model": ""
            })

    def get_settings(self):
        try:
            with open(self.settings_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"engine": "offline", "api_key": ""}

    def save_settings(self, settings):
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def install_model(self):
        # We can use PyWebView's native file dialog instead of tkinter!
        window = webview.windows[0]
        file_types = ('CTranslate2 Bin (*.bin)', 'All files (*.*)')
        result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        
        if result and len(result) > 0:
            filepath = result[0]
            target_dir = os.path.join(self.root_dir, "translator_model")
            os.makedirs(target_dir, exist_ok=True)
            try:
                shutil.copy2(filepath, os.path.join(target_dir, "model.bin"))
                return {"success": True, "message": "Model installed successfully!"}
            except Exception as e:
                return {"success": False, "message": f"Error: {str(e)}"}
        return {"success": False, "message": ""}

    def start_setja(self):
        if not os.path.exists(self.py_exe):
            print("Python executable not found at:", self.py_exe)
            return False

        try:
            # Start processes silently
            flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
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
                    p = subprocess.Popen(c["cmd"], cwd=c["cwd"], env=env, creationflags=flags)
                    self.processes.append(p)
                except Exception as e:
                    print(f"Failed to start {c['cmd']}: {e}")
            return True
        except Exception as e:
            print(f"Failed to start SETJA: {e}")
            self.stop_setja()
            return False

    def stop_setja(self):
        for p in self.processes:
            try:
                p.terminate()
            except:
                pass
        self.processes = []
        return True

    def minimize(self):
        webview.windows[0].minimize()

    def close_app(self):
        webview.windows[0].destroy()

def get_entrypoint():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'web', 'index.html')
    return os.path.join(os.path.dirname(__file__), 'web', 'index.html')

if __name__ == '__main__':
    api = Api()
    webview.create_window(
        'SETJA Control Panel', 
        url=get_entrypoint(),
        js_api=api,
        width=750, 
        height=750,
        resizable=False,
        frameless=True,
        easy_drag=False
    )
    webview.start(http_server=True)
