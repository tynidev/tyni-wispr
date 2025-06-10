"""Setup script for Tyni-Wispr."""

from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Parse requirements.txt to separate regular packages from PyTorch
requirements = []
pytorch_requirements = []
extra_index_urls = []

try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("//"):
                if line.startswith("--extra-index-url"):
                    # Extract the URL after --extra-index-url
                    url = line.split("--extra-index-url", 1)[1].strip()
                    extra_index_urls.append(url)
                elif line.startswith("torch"):
                    # Handle PyTorch separately
                    pytorch_requirements.append(line)
                elif not line.startswith("--"):
                    requirements.append(line)
except FileNotFoundError:    # Fallback requirements if file doesn't exist
    requirements = [
        "faster-whisper",
        "torch>=2.0.0",
        "sounddevice",
        "numpy", 
        "pyautogui",
        "scipy",
        "keyboard",
        "requests",
        "language_tool_python",
    ]

# Add PyTorch as regular requirement if no extra index URLs
if not extra_index_urls:
    requirements.extend(pytorch_requirements)

setup(
    name="tyni-wispr",
    version="1.0.0",
    author="Tyler",
    description="Real-time speech-to-text transcription using OpenAI's Whisper model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tyni-wispr=tyni_wispr.main:main",
        ],
    },
    keywords="speech-to-text, whisper, transcription, voice, audio, ai",
)

# Show post-installation instructions
if __name__ == '__main__' and len(sys.argv) > 1 and any(cmd in sys.argv for cmd in ['install', 'develop']):
    print("\n" + "="*70)
    print("🎉 TYNI-WISPR INSTALLATION COMPLETE!")
    print("="*70)
    
    if extra_index_urls and pytorch_requirements:
        print("⚠️  IMPORTANT: PYTORCH CUDA INSTALLATION REQUIRED")
        print("="*70)
        print("To enable GPU acceleration, install PyTorch with CUDA support:")
        print("")
        for url in extra_index_urls:
            for torch_req in pytorch_requirements:
                print(f"   pip install --extra-index-url {url} {torch_req} --force-reinstall")
        print("")
        print("Alternative: For CPU-only (no GPU acceleration):")
        print("   pip install torch --force-reinstall")
        print("")
        print("After PyTorch installation, you can use:")
    else:
        print("📝 Quick Start:")
    
    print("   tyni-wispr --help                    # Show help")
    print("   tyni-wispr                           # Start with default settings")
    print("   tyni-wispr -m small.en -l            # Use small English model with logging")
    print("   tyni-wispr --llm-enhance             # Enable LLM text enhancement")
    print("")
    print("🎯 Usage:")
    print("   1. Run: tyni-wispr")
    print("   2. Press RIGHT SHIFT to start/stop recording")
    print("   3. Text will be typed automatically!")
    print("="*70 + "\n")
