"""
Real-time speech-to-text transcription using OpenAI's Whisper model.

1. Press hotkey (right shift) to record
2. Press again to stop. 
3. Transcribes audio and types text in active window.

It automatically detects CPU/GPU availability and gracefully handles 
GPU memory errors.

Usage:
    python tyni-wispr.py [--model MODEL_NAME] [--log-performance]

Options:
    --model, -m            Whisper model to use (default: turbo).
    --log-performance, -l  Enable logging of transcription performance metrics.

Example:
    python tyni-wispr.py -m small.en -l

Requirements:
    - Python 3.7+
    - PyTorch (with optional CUDA support)
    - whisper, sounddevice, numpy, pyautogui, keyboard
"""

import warnings
import whisper # type: ignore
import torch # type: ignore
import sounddevice as sd # type: ignore
import numpy as np # type: ignore
import pyautogui # type: ignore
import keyboard # type: ignore
import argparse
import sys
import time
import csv
import os
from datetime import datetime

warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")

def main():
    """Main entry point for the Tyni-Wispr speech-to-text application.
    
    Initializes the Whisper model, sets up audio recording, and handles
    the hotkey-based recording workflow for real-time transcription.
    """
    # Parse command-line arguments
    args = parse_arguments()
    MODEL_SIZE = args.model
    ENABLE_LOGGING = args.log_performance
    SILENT_MODE = args.silent

    print(f"🎤 Starting Tyni-Wispr with model: {MODEL_SIZE}")
    if ENABLE_LOGGING:
        print("📊 Performance logging enabled - data will be saved to transcription_performance.csv")

    # Settings
    HOTKEY = 'right shift'
    SAMPLERATE = 16000
    CHANNELS = 1

    model, device = load_model(MODEL_SIZE)

    print("🎯 Ready! Hold the hotkey to record.")

    # Audio buffer
    audio_buffer = []
    recording = False
    audio_stream = None

    def record_audio_buffer(indata, frames, time, status):
        """Callback function for audio stream to capture audio data.
        
        Args:
            indata (numpy.ndarray): Input audio data from the microphone.
            frames (int): Number of frames in the audio data.
            time (CData): Time info from the audio stream.
            status (CallbackFlags): Status flags from the audio stream.
        """
        nonlocal recording, audio_buffer
        if recording:
            audio_buffer.append(indata.copy())

    # Start audio stream
    audio_stream = sd.InputStream(samplerate=SAMPLERATE, channels=CHANNELS, dtype='int16', callback=record_audio_buffer)
    audio_stream.start()

    try:
        while True:
            keyboard.wait(HOTKEY)
            if not SILENT_MODE:
                print("🎙️  Recording...")
            audio_buffer = []
            recording = True     
            
            keyboard.wait(HOTKEY)  # Wait for another press to stop recording
            recording = False
            if not SILENT_MODE:
                print("🛑 Recording stopped. Processing...")

            # Process the audio buffer
            if audio_buffer:
                audio_mono, audio_duration = read_audio_from_buffer(audio_buffer, SAMPLERATE)
                try:
                    text = transcribe_audio(model, audio_mono, ENABLE_LOGGING, SILENT_MODE, MODEL_SIZE, audio_duration)
                    # if text is not empty write it to active window
                    if text:
                        pyautogui.write(text + ' ')
                except torch.cuda.OutOfMemoryError:
                    print("⚠️  GPU memory error during transcription. Consider using a smaller model or switching to CPU.")
                    # Clear GPU cache and retry
                    if device == "cuda":
                        torch.cuda.empty_cache()
                        print("🧹 GPU cache cleared. Please try again.")
                except Exception as e:
                    print(f"❌ Transcription error: {str(e)}")
            else:
                print("⚠️  No audio recorded! Audio buffer is empty.")

    except KeyboardInterrupt:
        print("\n👋 Exiting.")
    finally:
        if audio_stream:
            audio_stream.stop()
            audio_stream.close()

def show_help():
    """Display help information about available Whisper models and usage."""
    help_text = """
🎤 TYNI-WISPR: Real-time Speech-to-Text using Whisper
=====================================================

USAGE:
    python tyni-wispr.py [--model MODEL_NAME] [--log-performance] [--help]

ARGUMENTS:
    --model, -m              Whisper model to use (default: turbo)
    --log-performance, -l    Enable performance logging to CSV file
    --help, -h               Show this help message and exit

HOW TO USE:
    1. Run the script: python tyni-wispr.py
    2. Press and hold the right shift key to start recording
    3. Release the right shift key to stop recording
    4. The transcribed text will be automatically typed in the active window

AVAILABLE WHISPER MODELS:
==========================

🏃 TINY MODELS (39M parameters, ~150MB)
    • tiny     - Multilingual, fastest speed (10x vs large), lowest accuracy
    • tiny.en  - English-only variant, optimized for English content
    Best for: Quick transcriptions, limited resources, clear audio with minimal noise

⚡ BASE MODELS (74M parameters, ~300MB) 
    • base     - Multilingual, good balance for limited resources (7x vs large)
    • base.en  - English-only variant, better performance on English
    Best for: General purpose transcription with reasonable accuracy when resources are limited

🚀 SMALL MODELS (244M parameters, ~1GB)
    • small    - Multilingual, recommended for most use cases (4x vs large)
    • small.en - English-only variant, more efficient for English content
    Best for: Daily transcription needs with good accuracy and reasonable speed

🎯 MEDIUM MODELS (769M parameters, ~3GB)
    • medium   - Multilingual, high accuracy (2x vs large)
    • medium.en- English-only variant, optimized for English
    Best for: High-quality transcriptions where accuracy is important

🔥 LARGE MODELS (1.5B parameters, ~6GB)
    • large-v1 - Original large model
    • large-v2 - Improved large model  
    • large-v3 - Latest large model with best accuracy
    • large    - Alias for latest large model
    Best for: Professional transcription where maximum accuracy is essential

⚡ ADVANCED MODELS
    • turbo    - Optimized for speed while maintaining accuracy (RECOMMENDED)

SELECTION TIPS:
===============
    • For English-only: Use .en variants for better performance and efficiency
    • For multilingual: Use standard models (support 100+ languages)
    • CPU-only systems: Stick to tiny/base models
    • Consumer GPUs: small/medium models work well
    • High-end GPUs: can efficiently run large models
    • Clear audio: Smaller models may be sufficient
    • Challenging audio (noise/accents): Use larger models

EXAMPLES:
=========
    python tyni-wispr.py                    # Use default turbo model
    python tyni-wispr.py --model small.en   # Use small English-only model
    python tyni-wispr.py -m tiny            # Use tiny multilingual model
    python tyni-wispr.py --log-performance  # Enable performance logging
    python tyni-wispr.py -m turbo -l        # Use turbo model with logging
    python tyni-wispr.py --help             # Show this help

REQUIREMENTS:
=============
    • Python 3.7+
    • PyTorch with CUDA support (optional, for GPU acceleration)
    • Microphone access
    • Required packages: whisper, torch, sounddevice, numpy, pyautogui, keyboard
"""
    print(help_text)

def parse_arguments():
    """Parse command-line arguments for the application.
    
    Returns:
        argparse.Namespace: Parsed arguments containing model, log_performance, and help flags.
    """
    parser = argparse.ArgumentParser(
        description="Real-time speech-to-text using Whisper",
        add_help=False  # We'll handle help manually
    )
    parser.add_argument(
        '--model', '-m',
        type=str,
        default='turbo',
        help='Whisper model to use (default: turbo)'
    )
    
    parser.add_argument(
        '--log-performance', '-l',
        action='store_true',
        help='Enable performance logging to CSV file'
    )
    
    parser.add_argument(
        '--help', '-h',
        action='store_true',
        help='Show help message and exit'
    )
    
    parser.add_argument(
        '--silent', '-s',
        action='store_true',
        help='Suppress startup and completion log messages (see docs)'
    )
    
    args = parser.parse_args()
    
    if args.help:
        show_help()
        sys.exit(0)
    
    return args

def load_model(model_size):
    """Load Whisper model with GPU support and fallback to CPU if necessary.
    
    Args:
        model_size (str): Name of the Whisper model to load (e.g., 'tiny', 'base', 'turbo').
        
    Returns:
        tuple: A tuple containing (model, device) where model is the loaded Whisper model
               and device is either 'cuda' or 'cpu'.
    """
    if torch.cuda.is_available():
        device = "cuda"
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"🚀 CUDA available! Using GPU: {gpu_name} ({gpu_memory:.1f}GB)")
    else:
        device = "cpu"
        print("💻 CUDA not available. Using CPU.")

    print("🔁 Loading Whisper model...")
    try:
        model = whisper.load_model(model_size, device=device)
        print("✅ Model loaded successfully on", device.upper())
    except Exception as e:
        if device == "cuda":
            print(f"⚠️  GPU loading failed ({str(e)}), falling back to CPU...")
            device = "cpu"
            model = whisper.load_model(model_size, device=device)
            print("✅ Model loaded on CPU (fallback)")
        else:
            raise e
    return model, device

def read_audio_from_buffer(audio_buffer, samplerate):
    """Convert audio buffer to normalized float32 mono audio data.
    
    Args:
        audio_buffer (list): List of numpy arrays containing int16 audio chunks.
        samplerate (int): Sample rate of the audio in Hz.
        
    Returns:
        tuple: A tuple containing (audio_mono, audio_duration) where audio_mono is
               normalized float32 audio data and audio_duration is the duration in seconds.
    """
    audio_np = np.concatenate(audio_buffer, axis=0)
    # Convert audio to float32 and normalize for direct transcription
    audio_float = audio_np.astype(np.float32) / 32768.0  # Convert int16 to float32
    audio_mono = audio_float.flatten()  # Ensure mono
    # Calculate audio duration
    audio_duration = len(audio_mono) / samplerate
    return audio_mono, audio_duration

def transcribe_audio(model, audio_data, ENABLE_LOGGING=False, SILENT_MODE=True,  MODEL_SIZE=None, audio_duration=None):
    """Transcribe audio data using the Whisper model.
    
    Args:
        model: Loaded Whisper model instance.
        audio_data (numpy.ndarray): Normalized float32 audio data to transcribe.
        ENABLE_LOGGING (bool): Whether to log performance metrics.
        MODEL_SIZE (str): Name of the model being used (for logging).
        audio_duration (float): Duration of the audio in seconds (for logging).
        
    Returns:
        str: Transcribed text with first letter capitalized, or empty string if no speech detected.
    """
    start_time = time.time()
    result = model.transcribe(audio_data)
    transcription_time = time.time() - start_time

    # Sanitize the text 
    text = result["text"].strip()
    if not text:
        return ""
    # Capitalize the first letter if text is not empty
    text = text[0].upper() + text[1:]

    if not SILENT_MODE:
        print(f"📝 Transcribed: {text} (⏱️ {transcription_time:.2f}s / {transcription_time*1000:.0f}ms)")

    # Log performance metrics if enabled
    if ENABLE_LOGGING and MODEL_SIZE is not None and audio_duration is not None:
        log_performance(MODEL_SIZE, transcription_time, len(text), audio_duration)
        
    return text

def log_performance(model_name, transcription_time, text_length, audio_duration):
    """Log performance metrics to a CSV file.
    
    Args:
        model_name (str): Name of the Whisper model used.
        transcription_time (float): Time taken to transcribe in seconds.
        text_length (int): Length of the transcribed text in characters.
        audio_duration (float): Duration of the audio in seconds.
    """
    log_file = "transcription_performance.csv"
    file_exists = os.path.exists(log_file)
    
    with open(log_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'model', 'transcription_time_ms', 'text_length', 'audio_duration_ms', 'time_per_char_ms', 'realtime_factor']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file is new
        if not file_exists:
            writer.writeheader()
        
        time_per_char = transcription_time / text_length if text_length > 0 else 0
        realtime_factor = transcription_time / audio_duration if audio_duration > 0 else 0
        
        writer.writerow({
            'timestamp': datetime.now().isoformat(),
            'model': model_name,
            'transcription_time_ms': round(transcription_time * 1000, 2),
            'text_length': text_length,
            'audio_duration_ms': round(audio_duration * 1000, 2),
            'time_per_char_ms': round(time_per_char * 1000, 4),
            'realtime_factor': round(realtime_factor, 3)
        })

if __name__ == "__main__":
    main()