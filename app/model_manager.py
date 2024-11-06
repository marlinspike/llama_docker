from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from .config import config
import logging
import os
from dotenv import load_dotenv

load_dotenv()

class ModelManager:
    def __init__(self, model_name=None):
        # Use configured model name or default
        self.model_name = model_name or os.getenv("MODEL_NAME", "meta-llama/Llama-3.1-8B") # Model name
        self.cache_dir = os.getenv("MODEL_CACHE_DIR", "./model_cache") # Cache directory for model and tokenizer
        self.max_length = os.getenv("RESPONSE_MAX_LENGTH", 50) # Maximum length of generated response
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN") # Hugging Face API token

        if not self.hf_token:
            raise ValueError("Hugging Face API token is not set. Please set the HUGGINGFACE_TOKEN environment variable.")

        logging.info(f"Initializing model '{self.model_name}' with cache directory at '{self.cache_dir}'")

        try:
            # Load tokenizer and model from Hugging Face with a specified cache directory and authentication token
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir, use_auth_token=self.hf_token)
            
            # Set up device to use CUDA if available, otherwise use CPU
            self.device = torch.device("cuda" if torch.cuda.is_available() and config.USE_GPU else "cpu")
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, cache_dir=self.cache_dir, use_auth_token=self.hf_token).to(self.device)

            logging.info(f"Successfully loaded model '{self.model_name}' on device '{self.device}'")
        except Exception as e:
            logging.error(f"Failed to load model '{self.model_name}': {e}")
            raise RuntimeError(f"Model loading failed: {e}")

    def run_inference(self, input_text):
        try:
            # Tokenize the input and ensure tensors are moved to appropriate device
            inputs = self.tokenizer(input_text, return_tensors="pt").to(self.device)
            
            # Run inference
            with torch.no_grad():
                output = self.model.generate(**inputs, max_length=int(self.max_length))

            # Decode generated tokens into text
            result = self.tokenizer.decode(output[0], skip_special_tokens=True)
            logging.info(f"Inference result: {result}")
            return result

        except Exception as e:
            logging.error(f"Inference failed: {e}")
            raise RuntimeError(f"Inference failed: {e}")
