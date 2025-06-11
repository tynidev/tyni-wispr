"""LLM text enhancement functionality using Ollama."""

from typing import Optional
import requests
from .azure_openai_client import AzureOpenAIClient

class LLMEnhancer:
    """Handles text enhancement using Ollama LLM."""
    
    @classmethod
    def for_ollama(cls, model="gemma3:12b", base_url="http://localhost:11434"):
        """Create an enhancer that uses only Ollama for text enhancement.
        
        Args:
            model (str): Ollama model name to use.
            base_url (str): Ollama base URL.
            
        Returns:
            LLMEnhancer: Instance configured for Ollama only.
        """
        instance = cls.__new__(cls)  # Create instance without calling __init__
        instance.model = model
        instance.base_url = base_url
        instance.ollama_available = False
        
        # Disable Azure OpenAI for this instance
        instance.azure_client = None
        instance.azure_available = False
        
        return instance
    
    @classmethod
    def for_azure_openai(cls, api_key=None, endpoint=None, api_version=None, 
                        deployment_name=None, model_name=None):
        """Create an enhancer that uses only Azure OpenAI for text enhancement.
        
        Args:
            api_key: Azure OpenAI API key (optional, can use env var)
            endpoint: Azure OpenAI endpoint URL (optional, can use env var)
            api_version: API version (optional, can use env var)
            deployment_name: Deployment name (optional, can use env var)
            model_name: Model name (optional, can use env var)
            
        Returns:
            LLMEnhancer: Instance configured for Azure OpenAI only.
        """
        instance = cls.__new__(cls)  # Create instance without calling __init__
        
        # Disable Ollama for this instance
        instance.model = None
        instance.base_url = None
        instance.ollama_available = False

        # Initialize Azure OpenAI client with custom parameters
        try:
            instance.azure_client = AzureOpenAIClient(api_key=api_key,
                                                      endpoint=endpoint,
                                                      api_version=api_version,
                                                      deployment_name=deployment_name,
                                                      model_name=model_name)
            instance.azure_available = True
        except Exception as e:
            print(f"⚠️  Azure OpenAI client initialization failed: {str(e)}")
            instance.azure_client = None
            instance.azure_available = False
        
        return instance
        
    def is_ollama_running(self, timeout=5):
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
                    print(f"📦 Ollama running with model: {self.model}")
                    self.ollama_available = True
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
            
        self.ollama_available = False
        return False
    
    def enhance(self, text, timeout=10):
        if self.azure_available and self.azure_client:
            return self.enhance_azure_openai(text)
        elif self.ollama_available:
            return self.enhance_ollama(text, timeout)
        else:
            raise RuntimeError("No LLM client available for enhancement. Please check configuration.")
    
    def enhance_azure_openai(self, text):
        """Enhance text using Azure OpenAI to fix punctuation and improve clarity.
        
        Args:
            text (str): Text to enhance.
            
        Returns:
            str: Enhanced text, or original text if enhancement fails.
        """
        if not self.azure_available or not self.azure_client:
            print("⚠️  Azure OpenAI client not available. Using original text.")
            return text
            
        system_message = """Fix any punctuation errors and rewrite the following text to improve brevity and clarity while preserving the original meaning. Keep slang where appropriate and only use standard ASCII characters. ONLY return revised text."""

        try:
            enhanced_text = self.azure_client.simple_chat(
                prompt=text,
                system_message=system_message,
                temperature=0.3,
                max_tokens=250
            )

            # Only return enhanced text if it's not empty and reasonable
            if enhanced_text and len(enhanced_text) < len(text) * 3:  # Sanity check
                return enhanced_text.strip()
            
            # If enhancement fails, return original text
            return text
        except Exception as e:
            print(f"⚠️  Azure OpenAI enhancement error: {str(e)}")
            return text
        
    def enhance_ollama(self, text, timeout=10):
        """Enhance text using Ollama LLM to fix punctuation and improve clarity.
        
        Args:
            text (str): Text to enhance.
            timeout (int): Request timeout in seconds.
            
        Returns:
            str: Enhanced text, or original text if enhancement fails.
        """
        if not self.ollama_available:
            return text
            
        try:
            url = f"{self.base_url}/api/generate"
            
            prompt = f"""Fix any punctuation errors and rewrite the following text to improve brevity and clarity while preserving the original meaning. Keep slang where appropriate and only use standard ASCII characters. ONLY return revised text.

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
