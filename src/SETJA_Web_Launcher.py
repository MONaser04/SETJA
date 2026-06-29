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
        self.src_dir = os.path.join(self.root_dir, "src") if not getattr(sys, 'frozen', False) else os.path.join(self.root_dir, "_internal", "src")
        # In PyInstaller, the web files are extracted to sys._MEIPASS
        self.settings_path = os.path.join(self.root_dir, "settings.json")
        self.py_exe = os.path.join(self.root_dir, "setja_stable", "Scripts", "python.exe")
        self.processes = []

        # Ensure settings exist
        if not os.path.exists(self.settings_path):
            self.save_settings({"engine": "offline", "api_key": ""})

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
            return False

        try:
            # Start processes silently
            flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            
            scripts = ["capture/main.py", "ocr/main.py", "translator/main.py", "bridge/main.py", "txt_viewer/main.py"]
            for script in scripts:
                script_path = os.path.join(self.src_dir, script.replace('/', os.sep))
                p = subprocess.Popen([self.py_exe, script_path], cwd=self.root_dir, creationflags=flags)
                self.processes.append(p)
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

def get_entrypoint():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'web', 'index.html')
    return os.path.join(os.path.dirname(__file__), 'web', 'index.html')

if __name__ == '__main__':
    api = Api()
    webview.create_window(
        'SETJA Control Panel - CEO Edition', 
        url=get_entrypoint(),
        js_api=api,
        width=650, 
        height=550,
        resizable=False,
        frameless=False
    )
    webview.start(http_server=True)
