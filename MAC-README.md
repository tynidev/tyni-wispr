# Tyni-Wispr: Mac Setup Instructions

## 1. ⬇️ Download the Project from GitHub

- Open your web browser and go to the GitHub repository page for Tyni-Wispr.
- Click the green "Code" button, then select "Download ZIP".
- Once downloaded, unzip the file to your desired location (for example, your Desktop or Documents folder).
- Open Terminal and navigate to the unzipped project folder. For example:
  ```sh
  cd ~/Desktop/tyni-wispr
  ```

---

## 🍎 Step 2: Install Python (Apple Silicon compatible)

### Install Homebrew (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Install Python via Homebrew:
```bash
brew install python
```

This gives you access to `python3` and `pip3`.

---

## 🛠 Step 3: Create and activate a virtual environment

### Create a new virtual environment:
```bash
python3 -m venv whisper_env
```

### Activate the environment:
```bash
source whisper_env/bin/activate
```

---

## 📦 Step 4: Install dependencies

- Navigate to your project folder (if not already there):
  ```sh
  cd /path/to/tyni-wispr
  ```
  (Replace with your actual path.)

- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```

If you encounter issues with PyTorch, you can install the CPU-only version directly:
```sh
pip install torch torchvision torchaudio
```
Then re-run:
```sh
pip install -r requirements.txt
```

---

## ▶️ Step 5: Run your script

- Start the app:
  ```sh
  python tyni-wispr.py
  ```

## 🛡️ Permissions (Required on macOS)

To allow microphone and keyboard access:

1. Go to **System Settings > Privacy & Security**
2. Under **Microphone**, allow access for **Terminal**
3. Under **Accessibility**, add **Terminal** and grant permission