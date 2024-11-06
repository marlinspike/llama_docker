#!/bin/bash
# Allow the container to run with GPU acceleration if available
if command -v nvidia-smi &> /dev/null; then
  echo "Running with GPU acceleration"
  export CUDA_VISIBLE_DEVICES=0
fi

# Start the FastAPI server
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
