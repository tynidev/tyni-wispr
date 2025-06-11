"""Model loading and management for Whisper."""

import torch
import faster_whisper
from .enhancement import LLMEnhancer

def load_whisper(model_size):
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
        model = faster_whisper.WhisperModel(model_size, device=device)
        print("📦 Whisper model:", model_size.strip(), "loaded successfully on", device.upper())
    except Exception as e:
        if device == "cuda":
            print(f"⚠️  GPU loading failed ({str(e)}), falling back to CPU...")
            device = "cpu"
            model = faster_whisper.WhisperModel(model_size, device=device)
            print("📦 Whisper model:", model_size.strip(), "loaded on CPU (fallback)")
        else:
            raise e
    return model, device

def load_enhancer_llm(args):
    """Load and configure the LLM enhancer based on user arguments.
    
    This function initializes either an Ollama or Azure OpenAI LLM enhancer
    based on the command-line arguments provided. It validates that the
    selected service is available before returning the enhancer instance.
    
    Args:
        args (argparse.Namespace): Parsed command-line arguments containing:
            - llm_enhance_ollama (bool): Whether to use Ollama enhancement
            - llm_enhance_azure_openai (bool): Whether to use Azure OpenAI enhancement
            - ollama_model (str): Name of the Ollama model to use
            - ollama_base_url (str): Base URL for the Ollama server
    
    Returns:
        LLMEnhancer or None: Configured LLM enhancer instance if available,
                            None if the selected service is not accessible
    
    Note:
        Only one enhancement service can be active at a time. If both are
        specified, Ollama takes precedence.
    """
    enhancer = None
    
    if args.llm_enhance_ollama:
        enhancer = LLMEnhancer.for_ollama(model=args.ollama_model, base_url=args.ollama_base_url)
        if not enhancer.is_ollama_running():
            print("⚠️  LLM enhancement disabled - Ollama not available")
            enhancer = None
        else:
            print(f"📦 LLM Enhance running with Ollama model: {args.ollama_model} and url: {args.ollama_base_url}")

    if not enhancer and args.llm_enhance_azure_openai:
        enhancer = LLMEnhancer.for_azure_openai()
        if not enhancer.azure_available:
            print("⚠️  LLM enhancement disabled - Azure OpenAI not available")
            enhancer = None
        else:
            print("📦 LLM Enhance running with Azure OpenAI")
    
    return enhancer
