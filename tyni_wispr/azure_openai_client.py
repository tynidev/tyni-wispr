import os
import sys
from typing import Optional, List, Dict, Any, Union
from openai.types.chat import ChatCompletion
from openai import APIError, APIConnectionError, RateLimitError, AuthenticationError

try:
    from openai import AzureOpenAI
except ImportError:
    print("OpenAI library not found. Please install it using:")
    print("pip install openai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    # Load environment variables from .env file if it exists
    load_dotenv()
except ImportError:
    # python-dotenv is optional
    pass


class AzureOpenAIClient:
    """A wrapper class for Azure OpenAI API interactions"""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        api_version: Optional[str] = None,
        deployment_name: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        """
        Initialize the Azure OpenAI client
        
        Args:
            api_key: Your Azure OpenAI API key (if None, will look for AZUREAI_API_KEY env var)
            endpoint: Azure OpenAI endpoint URL (if None, will look for AZUREAI_ENDPOINT env var)
            api_version: API version (if None, will look for AZUREAI_API_VERSION env var)
            deployment_name: Deployment name (if None, will look for AZUREAI_DEPLOYMENT_NAME env var)
            model_name: Model name (if None, will look for AZUREAI_MODEL env var)
        """
        self.api_key = api_key or os.getenv('AZUREAI_API_KEY')
        self.endpoint = endpoint or os.getenv('AZUREAI_ENDPOINT')
        self.api_version = api_version or os.getenv('AZUREAI_API_VERSION', '2024-12-01-preview')
        self.deployment_name = deployment_name or os.getenv('AZUREAI_DEPLOYMENT_NAME')
        self.model_name = model_name or os.getenv('AZUREAI_MODEL', 'gpt-4o')
        
        # Validate required parameters
        if not self.api_key:
            raise ValueError("API key is required. Set AZUREAI_API_KEY environment variable or pass api_key parameter.")
        
        if not self.endpoint:
            raise ValueError("Azure endpoint is required. Set AZUREAI_ENDPOINT environment variable or pass endpoint parameter.")
        
        if not self.deployment_name:
            raise ValueError("Deployment name is required. Set AZUREAI_DEPLOYMENT_NAME environment variable or pass deployment_name parameter.")
        
        # Initialize the Azure OpenAI client
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
        )
    
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        deployment: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        top_p: float = 1.0,
        **kwargs
    ) -> Optional[ChatCompletion]:
        """
        Create a chat completion using Azure OpenAI
        
        Args:
            messages: List of message dictionaries
            deployment: Deployment name to use (defaults to instance deployment_name)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            **kwargs: Additional parameters for the API call
        
        Returns:
            Chat completion response
            
        Raises:
            AuthenticationError: If API key is invalid
            RateLimitError: If rate limit is exceeded
            APIConnectionError: If connection to API fails
        """
        try:
            response = self.client.chat.completions.create(
                model=deployment or self.deployment_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                **kwargs
            )
            return response
        except AuthenticationError as e:
            print(f"Authentication error: {e}")
            raise
        except RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
            raise
        except APIConnectionError as e:
            print(f"API connection error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error making chat completion request: {e}")
            raise
    
    def simple_chat(
        self, 
        prompt: str, 
        deployment: Optional[str] = None,
        system_message: str = "You are a helpful assistant.",
        **kwargs
    ) -> Optional[str]:
        """
        Simple chat interface with a single prompt
        
        Args:
            prompt: The user's prompt
            deployment: Deployment name to use
            system_message: System message to set context
            **kwargs: Additional parameters
        
        Returns:
            String response from the AI
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        response = self.chat_completion(messages, deployment, **kwargs)
        
        if response:
            # take the top response from the choices
            return response.choices[0].message.content
        return None
    
    def get_client_info(self) -> Dict[str, str]:
        """Get information about the configured client"""
        return {
            "endpoint": self.endpoint,
            "api_version": self.api_version,
            "deployment_name": self.deployment_name,
            "model_name": self.model_name
        }
    
    def validate_configuration(self) -> bool:
        """
        Validate the client configuration by making a test request
        
        Returns:
            bool: True if configuration is valid
        """
        try:
            response = self.simple_chat("Hello", max_tokens=10)
            return response is not None
        except Exception as e:
            print(f"Configuration validation failed: {e}")
            return False
