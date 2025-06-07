"""Model loading and management for Whisper."""

import torch
import whisper

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
