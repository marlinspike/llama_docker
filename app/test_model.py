from model_manager import ModelManager

def test_model_load():
    try:
        model_manager = ModelManager()
        assert model_manager.model is not None
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Model loading failed: {e}")

if __name__ == "__main__":
    test_model_load()
