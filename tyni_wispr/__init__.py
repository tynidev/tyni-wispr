"""Tyni-Wispr: Real-time speech-to-text transcription using OpenAI's Whisper model."""

__version__ = "1.0.0"

import warnings

warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")

from .main import main

__all__ = ['main']
