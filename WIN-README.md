# Tyni-Wispr: Windows Setup Instructions

## 1. ⬇️ Download the Project from GitHub

- Open your web browser and go to the GitHub repository page for Tyni-Wispr.
- Click the green "Code" button, then select "Download ZIP".
- Once downloaded, unzip the file to your desired location (for example, your Desktop or Documents folder).
- Open **PowerShell** and navigate to the unzipped project folder. For example:
  ```powershell
  cd "$env:USERPROFILE\Desktop\tyni-wispr"
  ```

---

## 🪟 Step 2: Install Python

- Download the latest version of Python from [python.org](https://www.python.org/downloads/windows/).
- Run the installer and **make sure to check "Add Python to PATH"** during installation.
- Verify installation:
  ```powershell
  python --version
  ```

---

## 🛠 Step 3: Create and activate a virtual environment

### Create a new virtual environment:
```powershell
python -m venv whisper_env
```

### Activate the environment:
```powershell
.\whisper_env\Scripts\Activate.ps1
```

---

## 📦 Step 4: Install dependencies

- Navigate to your project folder (if not already there):
  ```powershell
  cd "C:\path\to\tyni-wispr"
  ```
  (Replace with your actual path.)

- Install dependencies:
  ```powershell
  pip install -r requirements.txt
  ```

If you encounter issues with PyTorch, you can install the CPU-only version directly:
```powershell
pip install torch torchvision torchaudio
```
Then re-run:
```powershell
pip install -r requirements.txt
```

---

## ▶️ Step 5: Run your script

- Start the app:
  ```powershell
  python tyni-wispr.py
  ```

## 🛡️ Permissions (Required on Windows)

To allow microphone and keyboard access:

1. Go to **Settings > Privacy & security**
2. Under **Microphone**, allow access for **Desktop apps** (make sure Python or your terminal is allowed)