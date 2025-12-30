<div align="center">
  <h1>🚀 SETJA</h1>
  <p><b>High-Performance, Real-Time AI Screen Translator</b></p>
  
  <a href="https://github.com/MONaser04/SETJA"><img src="https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white" alt="Windows"></a>
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/C++-DirectX-red?logo=c%2B%2B" alt="C++">
  <img src="https://img.shields.io/badge/GPU-Accelerated-76B900?logo=nvidia&logoColor=white" alt="Nvidia">
</div>

---

**SETJA** is an ultra-fast, hardware-accelerated screen translation tool designed for seamless, real-time text extraction and translation. Built with an optimized microservice architecture, SETJA operates primarily **offline** for maximum privacy, while also offering a hybrid cloud-fallback via any Custom Online API. 

Currently specializing in **English to Arabic** translation, SETJA is ideal for gamers, developers, and researchers who require instant translations overlayed directly on their screens without intrusive UI blocks.

---

## ✨ Key Features

* **⚡ Millisecond-Level Capture:** Utilizes a custom C++ & DirectX (DXGI) engine bypassing standard Windows APIs to achieve zero-latency desktop duplication and frame capturing.
* **🧠 Hybrid AI Translation:** 
  * **Fully Offline Mode:** Powered by highly optimized `CTranslate2` and `MarianMT` models for private, local execution.
  * **Online Mode (Custom API):** Seamlessly toggle (via `F9`) to any Cloud/REST API for contextual, cloud-based translation.
* **👁️ State-of-the-Art OCR:** Integrates `PaddleOCR` running as a decoupled microservice, processing shared-memory frames with extremely high accuracy.
* **🎨 Immersive Overlay UI:** 
  * **Acrylic & Frameless:** A modern `PySide6` UI that perfectly blends with Windows 11 design standards.
  * **Click-Through Mode:** The translation window stays always-on-top but ignores mouse events, allowing uninterrupted interaction with underlying applications (perfect for gaming).
  * **Smart Debouncing:** Built-in logic to avoid text flickering and translation redundancies.

---

## 🏗️ Architecture & Project Structure

SETJA is engineered as a robust multi-process system to ensure the heavy AI models do not block the UI or capture loops. It relies on **Shared Memory (SHM)** for IPC image transfers and **Local HTTP REST APIs** for AI inference.

```text
📦 SETJA
 ┣ 📂 capture/        # 📷 Screen Capture Engine
 ┃ ┣ 📂 screen_capture/ # C++ DirectX (DXGI) executable for ultra-fast frame acquisition.
 ┃ ┗ 📂 region_selector/# Python script providing a lightweight UI to select screen coordinates.
 ┣ 📂 ocr/            # 🔍 Optical Character Recognition Service
 ┃ ┗ 📂 app/          # Flask-based REST API wrapping the PaddleOCR engine. Reads frames via SHM.
 ┣ 📂 translator/     # 🌐 Translation Engine
 ┃ ┣ 📂 core/         # CTranslate2 / MarianMT models and online API fallback logic.
 ┃ ┗ 📂 app/          # Standalone HTTP service to serve translation requests on port 15199.
 ┣ 📂 txt_viewer/     # 🖥️ User Interface
 ┃ ┗ 📜 txt_viewer.py # PySide6 Acrylic Overlay. Handles UI rendering and click-through mechanics.
 ┣ 📂 bridge/         # 🌉 The Orchestrator
 ┃ ┗ 📜 bridge_ocr_t.py # The brain linking OCR outputs to the Translator. Manages caching and identical-text suppression.
 ┗ 📜 main.cmd        # 🚀 Entry point: spins up all microservices and establishes IPC.
```

---

## 🛠️ Tech Stack

* **Core AI:** `PaddleOCR`, `CTranslate2`, `MarianMT`, `Custom Cloud APIs`
* **Desktop UI & Capture:** `PySide6 (Qt)`, `C++ (MSVC)`, `Windows DXGI Desktop Duplication API`
* **IPC & Concurrency:** Multi-processing, `Shared Memory (SHM)`, `Flask REST APIs`

---

## 📦 Installation & Usage

### Prerequisites
* **OS:** Windows 10 / 11
* **Hardware:** An NVIDIA GPU (CUDA) is highly recommended for real-time performance.
* **Storage:** ~7 GB available space (due to the PyTorch/CUDA environment and translation models).

### Setup Guide
1. Download the latest release from the [Releases](https://github.com/MONaser04/SETJA/releases) tab. *(Note: Ensure you download the AI model binaries if they are packaged separately).*
2. Extract the archive to your preferred location.
3. Run `Setup_Env.exe` to automatically configure the virtual environment and dependencies.
4. Execute `main.cmd` to boot the microservices.
5. Use the on-screen prompt to draw a selection box over the **English text** you wish to translate.
6. Press **`F9`** anytime to toggle between Offline AI and Online Custom API translation.

---

<div align="center">
  <i>Developed and optimized by <a href="https://github.com/MONaser04">MONaser04</a>. Contributions and issue reports are welcome!</i>
</div>
