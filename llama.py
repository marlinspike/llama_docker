import os
import logging
from typing import Optional

import llama_cpp  # Import the llama_cpp module
from llama_cpp import Llama
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Read the GGUF_MODEL_PATH from the .env file
GGUF_MODEL_PATH = os.getenv('GGUF_MODEL_PATH', './model_cache_gguf/llama-3.1-8b.gguf')
RESPONSE_MAX_LENGTH = int(os.getenv('RESPONSE_MAX_LENGTH', '1000'))

# Pydantic models
class GenerateRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    max_tokens: Optional[int] = RESPONSE_MAX_LENGTH

class GenerateResponse(BaseModel):
    response: str

# Global model variable
llama_model: Optional[Llama] = None

def load_llama_model(gguf_model_path: str) -> Llama:
    """Load the GGUF Llama model."""
    logger.info(f"Loading Llama model from '{gguf_model_path}'")

    # Determine if GPU acceleration is available
    n_gpu_layers = 1024
    if hasattr(llama_cpp, 'LLAMA_SUPPORTS_GPU_OFFLOAD') and llama_cpp.LLAMA_SUPPORTS_GPU_OFFLOAD:
        n_gpu_layers = 100  # Adjust based on your GPU capacity
        logger.info("GPU acceleration is available. Using GPU layers.")
    else:
        logger.info("GPU acceleration is not available. Using CPU only.")

    llama_model_instance = Llama(
        model_path=gguf_model_path,
        n_ctx=2048,
        n_gpu_layers=n_gpu_layers
    )
    logger.info("Llama model loaded successfully")
    return llama_model_instance

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function to handle startup and shutdown."""
    global llama_model
    try:
        # Ensure the model file exists
        if not os.path.exists(GGUF_MODEL_PATH):
            logger.error(f"GGUF model not found at '{GGUF_MODEL_PATH}'. Please ensure the model file is present.")
            raise RuntimeError("GGUF model not found.")
        llama_model = load_llama_model(GGUF_MODEL_PATH)
        logger.info("Model initialized during startup")
        yield
        # Shutdown code (if any)
        logger.info("Shutting down")
    except Exception as e:
        logger.error(f"Failed to load model during startup: {e}")
        raise RuntimeError("Failed to load model") from e

# Initialize the FastAPI app with the lifespan function
app = FastAPI(lifespan=lifespan)

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate text using the Llama model."""
    if llama_model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    full_prompt = ''
    if request.system_prompt:
        full_prompt += f"{request.system_prompt}\n"
    full_prompt += request.prompt

    try:
        output = llama_model(
            prompt=full_prompt,
            max_tokens=request.max_tokens,
            stop=["<|endoftext|>"],
            echo=False
        )
        response_text = output['choices'][0]['text'].strip()
        return GenerateResponse(response=response_text)
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        raise HTTPException(status_code=500, detail="Error generating text.")




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)