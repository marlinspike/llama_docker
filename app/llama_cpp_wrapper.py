import ctypes
import logging

# Load the llama shared library
try:
    llama_lib = ctypes.CDLL('./llama_cpp/libllama.so')
except Exception as e:
    logging.error(f"Failed to load llama_cpp shared library: {e}")
    raise

class LlamaCppWrapper:
    def __init__(self):
        llama_lib.llama_init()

    def run(self, input_text):
        result = llama_lib.llama_run_inference(input_text.encode('utf-8'))
        return result.decode('utf-8')
