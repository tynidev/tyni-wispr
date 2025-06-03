# Tyni-Wispr: Mac Setup Instructions

## 1. Download the Project from GitHub

- Open your web browser and go to the GitHub repository page for Tyni-Wispr.
- Click the green "Code" button, then select "Download ZIP".
- Once downloaded, unzip the file to your desired location (for example, your Desktop or Documents folder).
- Open Terminal and navigate to the unzipped project folder. For example:
  ```sh
  cd ~/Desktop/tyni-wispr
  ```

---

## 2. Install Python

- Install Homebrew if you don’t have it:
  ```sh
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
- Install Python:
  ```sh
  brew install python
  ```

---

## 3. Install Project Dependencies

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

## 4. Run the App

- Start the app:
  ```sh
  python tyni-wispr.py
  ```
