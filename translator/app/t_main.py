import sys
import os
import site
from pathlib import Path

if sys.platform == "win32":
    for sp in site.getsitepackages():
        nvidia_dir = os.path.join(sp, "nvidia")
        if os.path.exists(nvidia_dir):
            for lib in os.listdir(nvidia_dir):
                bin_dir = os.path.join(nvidia_dir, lib, "bin")
                if os.path.exists(bin_dir):
                    os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")
                    if hasattr(os, "add_dll_directory"):
                        try:
                            os.add_dll_directory(bin_dir)
                        except Exception:
                            pass

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.config.t_config import HOST, PORT
from core.api.t_api import app

def main():
    import uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="warning",
        access_log=False,   
    )

if __name__ == "__main__":
    main()
