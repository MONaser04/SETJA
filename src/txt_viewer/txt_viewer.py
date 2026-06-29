import os, tempfile
AR_OUT_PATH = os.path.join(tempfile.gettempdir(), "setja_ar.txt")

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge.bridge_ocr_t import BridgeConfig, run_bridge, wait_for_ports

_last_err = {"key": None}

def _print_error(kind: str, info: str):
    if info == _last_err["key"]:
        return
    _last_err["key"] = info
    print(info)


def _print_result(cur_text: str, mt_j: dict):
    lines = mt_j.get("lines")
    if not lines and mt_j.get("text"):
        lines = [mt_j.get("text")]

    ms = float(mt_j.get("ms") or 0.0)
    waiting = bool(mt_j.get("waiting_for_stability", False))

    if waiting or not lines:
        ar_text = ""
    else:
        ar_text = " ".join(
            ln.strip() for ln in lines if (ln or "").strip()
        )

    tmp = AR_OUT_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(ar_text)
    os.replace(tmp, AR_OUT_PATH)

    print("-" * 60)
    print(f"EN: {cur_text}")

    if waiting or not lines:
        print("AR: (waiting_for_stability)")
    else:
        print("AR:")
        for ln in lines:
            if (ln or "").strip():
                print(ln)

    print(f"MT_time: {ms:.2f} ms")
    print("-" * 60)


def main():
    cfg = BridgeConfig(
        ocr_url="http://127.0.0.1:15188/ocr_shm",
        mt_url="http://127.0.0.1:15199/translate",
        lang="en",
        gpu=1,
        poll_interval_ms=80,
        skip_empty=True,
        unique_stream_per_text=True,
        stream_id="bridge_ocr",
        similarity_threshold=0.8,
        cooldown_sec=1.0,
    )

    wait_for_ports(
        [
            ("OCR", "127.0.0.1", 15188),
            ("Translator", "127.0.0.1", 15199),
        ],
        label="[WAIT]",
        check_interval=0.4,
    )
    print("SETJA Ready to Translate (Press F9 to toggle between Offline and Gemini)")

    import keyboard
    import json
    
    settings_path = os.path.join(str(Path(__file__).resolve().parents[1]), "settings.json")
    def toggle_engine(e):
        engine = "offline"
        api_key = ""
        model_name = "gemini-3.1-flash-lite"
        if os.path.exists(settings_path):
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    s = json.load(f)
                    engine = s.get("engine", "offline")
                    api_key = s.get("gemini_api_key", "")
                    model_name = s.get("gemini_model", "gemini-3.1-flash-lite")
            except:
                pass

        if engine == "offline":
            new_engine = "gemini"
            print("\n" + "="*60)
            print(">>> ENGINE SWITCHED TO: Gemini (Online) <<<")
            print("="*60 + "\n")
        else:
            new_engine = "offline"
            print("\n" + "="*60)
            print(">>> ENGINE SWITCHED TO: Offline <<<")
            print("="*60 + "\n")

        try:
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump({"engine": new_engine, "gemini_api_key": api_key, "gemini_model": model_name}, f, indent=4)
        except Exception as err:
            print(f"Error saving setting: {err}")

    keyboard.on_press_key("f9", toggle_engine)

    run_bridge(cfg, on_result=_print_result, on_error=_print_error)


if __name__ == "__main__":
    main()
