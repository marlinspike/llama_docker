import os

class Config:
    MODEL_NAME = os.getenv("MODEL_NAME", "decapoda-research/llama-7b-hf")
    MAX_REQUEST_SIZE = int(os.getenv("MAX_REQUEST_SIZE", 512))
    USE_GPU = os.getenv("USE_GPU", "true").lower() in ("yes", "true", "t", "1")

config = Config()
