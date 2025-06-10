"""Whisper transcription functionality."""

import torch
def transcribe_audio(model, audio_data):
    """Transcribe audio data using the Whisper model.
    
    Args:
        model: Loaded Whisper model instance.
        audio_data (numpy.ndarray): Normalized float32 audio data to transcribe.
        
    Returns:
        str: Transcribed text from the model.
    """
    try:
        # faster_whisper returns segments and info
        segments, info = model.transcribe(audio_data)
        # Extract text from segments
        text = " ".join([segment.text for segment in segments]).strip()
        return text
    except torch.cuda.OutOfMemoryError:
        print("⚠️  GPU memory error during transcription.")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("🧹 GPU cache cleared. Please try again.")
        raise
    except Exception as e:
        print(f"❌ Transcription error: {str(e)}")
        raise
