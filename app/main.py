from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from .model_manager import ModelManager  # <-- Make sure this import is correct
from .config import Config  # Assuming config.py is in the same directory
import logging


app = FastAPI()
model_manager = ModelManager()

@app.get("/")
def read_root():
    return {"message": "Welcome to HuggingFace Model API"}

@app.post("/predict/")
async def predict(request: Request):
    try:
        data = await request.json()
        input_text = data.get("input_text", "").strip()
        if not input_text:
            raise HTTPException(status_code=400, detail="Input text is required")
        if len(input_text) > 512:
            raise HTTPException(status_code=413, detail="Input text is too large")
        result = model_manager.run_inference(input_text)
        return {"result": result}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logging.error(f"Error during inference: {e}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@app.get("/health/")
def health_check():
    return {"status": "healthy"}
