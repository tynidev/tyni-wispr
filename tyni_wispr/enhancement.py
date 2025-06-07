"""LLM text enhancement functionality using Ollama."""

import requests

class LLMEnhancer:
    """Handles text enhancement using Ollama LLM."""
    
    def __init__(self, model="gemma3:12b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.available = False
        
    def check_availability(self, timeout=5):
        """Check if Ollama is running and the specified model is available.
        
        Args:
            timeout (int): Request timeout in seconds.
            
        Returns:
            bool: True if Ollama is available and model exists, False otherwise.
        """
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=timeout)
            
            if response.status_code == 200:
                models_data = response.json()
                available_models = [m['name'] for m in models_data.get('models', [])]
                
                if self.model in available_models:
                    print(f"✅ Ollama running with model: {self.model}")
                    self.available = True
                    return True
                else:
                    print(f"⚠️  Model '{self.model}' not found. Available models: {', '.join(available_models)}")
                    print(f"💡 To install: ollama pull {self.model}")
                    
        except requests.exceptions.ConnectionError:
            print("⚠️  Ollama not running. Start with: ollama serve")
        except requests.exceptions.Timeout:
            print("⚠️  Ollama connection timed out")
        except Exception as e:
            print(f"⚠️  Error checking Ollama: {str(e)}")
            
        self.available = False
        return False
        
    def enhance(self, text, timeout=10):
        """Enhance text using Ollama LLM to fix punctuation and improve clarity.
        
        Args:
            text (str): Text to enhance.
            timeout (int): Request timeout in seconds.
            
        Returns:
            str: Enhanced text, or original text if enhancement fails.
        """
        if not self.available:
            return text
            
        try:
            url = f"{self.base_url}/api/generate"
            
            prompt = f"""Fix any punctuation errors and rewrite the following text for clarity while preserving the original meaning. Only return the corrected text without any explanation or quotes:

{text}"""
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3,  # Lower temperature for more consistent output
                "max_tokens": 150
            }
            
            response = requests.post(url, json=payload, timeout=timeout)
            
            if response.status_code == 200:
                result = response.json()
                enhanced_text = result.get("response", "").strip()
                # Only return enhanced text if it's not empty and reasonable
                if enhanced_text and len(enhanced_text) < len(text) * 3:  # Sanity check
                    return enhanced_text
                    
        except requests.exceptions.ConnectionError:
            print("⚠️  Ollama not running. Skipping LLM enhancement.")
        except requests.exceptions.Timeout:
            print("⚠️  Ollama request timed out. Using original text.")
        except Exception as e:
            print(f"⚠️  LLM enhancement error: {str(e)}")
            
        return text
