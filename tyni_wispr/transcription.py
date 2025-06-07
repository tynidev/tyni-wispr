"""Whisper transcription functionality."""

import torch
from .utils import post_process_transcription

def transcribe_audio(model, audio_data):
    """Transcribe audio data using the Whisper model.
    
    Args:
        model: Loaded Whisper model instance.
        audio_data (numpy.ndarray): Normalized float32 audio data to transcribe.
        
    Returns:
        str: Cleaned and formatted transcribed text from the model.
    """
    try:
        result = model.transcribe(audio_data)
        text = result['text'].strip()
        return post_process_transcription(text)
    except torch.cuda.OutOfMemoryError:
        print("⚠️  GPU memory error during transcription.")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("🧹 GPU cache cleared. Please try again.")
        raise
    except Exception as e:
        print(f"❌ Transcription error: {str(e)}")
        raise
