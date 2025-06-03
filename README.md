# Tyni-Wispr

Tyni-Wispr is a real-time speech-to-text transcription tool using OpenAI's Whisper model. It supports hotkey-based recording, automatic typing of transcribed text, and performance logging. The project includes a Windows startup shortcut installer for easy background use.

## Features
- Real-time speech-to-text using Whisper
- Hotkey (right shift) to start/stop recording
- Automatic typing of transcribed text in the active window
- Performance logging to CSV (optional)
- Windows startup shortcut installer (PowerShell)

## Requirements
- Python 3.7+
- PyTorch (with optional CUDA support)
- whisper, sounddevice, numpy, pyautogui, keyboard
- PowerShell 7 (for startup shortcut)

## Quick Start
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   python tyni-wispr.py
   ```
3. (Optional) Install as a Windows startup app:
   ```
   pwsh install_startup_shortcut.ps1
   ```

## License
See [LICENSE](LICENSE).
