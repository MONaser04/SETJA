import os
import subprocess
import sys
import atexit
from pathlib import Path

from bridge_ocr_t import wait_for_ports

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

CAPTURE_CMD = ROOT / "capture" / "capture_launcher.cmd"
OCR_PY = ROOT / "ocr" / "app" / "ocr_main.py"
TRANSLATOR_DIR = ROOT / "translator"
VIEWER_PY = ROOT / "txt_viewer" / "txt_viewer.py"

_processes = []

def _cleanup_processes():
    for p in reversed(_processes):
        try:
            p.terminate()
        except Exception:
            pass
atexit.register(_cleanup_processes)

def _run_background(args: list, cwd: Path):
    p = subprocess.Popen(args, cwd=str(cwd), shell=False)
    _processes.append(p)


import json

def is_offline_enabled():
    try:
        settings_path = ROOT / "settings.json"
        if settings_path.exists():
            with open(settings_path, "r", encoding="utf-8") as f:
                return json.load(f).get("enable_offline", True)
    except Exception:
        pass
    return True

def main():
    # 1) Capture (C++ executables)
    _run_background(["cmd.exe", "/c", "call", str(CAPTURE_CMD)], CAPTURE_CMD.parent)

    # 2) OCR
    _run_background([PYTHON, "-u", str(OCR_PY)], ROOT)

    ports_to_wait = [("OCR", "127.0.0.1", 15188)]

    # 3) Translator (Only if enabled)
    if is_offline_enabled():
        _run_background([PYTHON, "-u", "-m", "app.t_main"], TRANSLATOR_DIR)
        ports_to_wait.append(("Translator", "127.0.0.1", 15199))

    wait_for_ports(
        ports_to_wait,
        label="[WAIT]",
        check_interval=0.4,
    )

    # 4) Viewer (needs PYTHONPATH=ROOT to import bridge)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    viewer_proc = subprocess.Popen(
        [PYTHON, "-u", str(VIEWER_PY)],
        cwd=str(VIEWER_PY.parent),
        shell=False,
        env=env,
    )
    _processes.append(viewer_proc)
    
    # Wait for the viewer to exit
    try:
        viewer_proc.wait()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
