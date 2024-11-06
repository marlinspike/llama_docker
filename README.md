Llama FastAPI Application
This project is a FastAPI application that uses the Llama 3.1 model for text generation. The application loads a pre-converted GGUF model file and provides an API endpoint to generate text based on a given prompt.


### Installation
**Clone the Repository**
```git clone https://github.com/your-username/llama-fastapi-app.git
cd llama-fastapi-app
```

**Create a Virtual Environment (Optional but Recommended)**
```python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

**Install Dependencies**
```
pip install --upgrade pip
pip install -r requirements.txt
```

### Configuration**
**Copy the Example Environment File**. Copy the .env.example file to .env:

**Set Up Environment Variables**. Edit the .env file and set the following variables:


```HUGGINGFACE_TOKEN=hf_your_huggingface_token
MODEL_NAME=meta-llama/Llama-3.1-8B
MODEL_CACHE_DIR=./model_cache
RESPONSE_MAX_LENGTH=1000
GGUF_MODEL_PATH=./model_cache_gguf/llama-3.1-8b.gguf
HUGGINGFACE_TOKEN: Your Hugging Face API token.
MODEL_NAME: The name of the model repository on Hugging Face.
MODEL_CACHE_DIR: Directory to cache the downloaded model.
RESPONSE_MAX_LENGTH: Maximum length of the generated response.
GGUF_MODEL_PATH: Path to the pre-converted GGUF model file.
```

### Model Conversion
Before running the application, you need to convert the Hugging Face model to GGUF format using the convert-hf-to-gguf.py script from the llama.cpp repository.

**Clone the llama.cpp Repository**
```
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
```

**Install Required Dependencies**
`pip install torch transformers sentencepiece`

**Convert the Model to GGUF Format**
- Option A: Using Local Model Directory
If you've already downloaded the model:

```
python convert-hf-to-gguf.py \
  /path/to/your/model \
  --outfile /path/to/output/llama-3.1-8b.gguf
```

For example, here's a model conversion command:
```
python convert_hf_to_gguf.py \\n  /Users/reubencleetus/code/python/ossllm/llama_docker/model_cache/models--meta-llama--Llama-3.1-8B/snapshots/d04e592bb4f6aa9cfee91e2e20afa771667e1d4b \\n  --outfile /Users/reubencleetus/code/python/ossllm/llama_docker/model_cache_gguf/llama-3.1-8b.gguf\n
```


- Option B: Letting the Script Download the Model
This will only work for GGUF Models in the Hugging Face Model Hub. Llama 3.1 isn't distributed by Meta in GGUF format, so you'll need to download and convert it manually. Otherwise, you can download a version of the model that's already in GGUF format.

Set your Hugging Face API token:
```
export HUGGINGFACEHUB_API_TOKEN=hf_your_huggingface_token
```
Run the conversion script:

```
python convert-hf-to-gguf.py \
  meta-llama/Llama-3.1-8B \
  --outfile /path/to/output/llama-3.1-8b.gguf
```

**Move the Converted Model to the Application Directory**. Copy the GGUF model file to the model_cache_gguf directory in your application:

`cp /path/to/output/llama-3.1-8b.gguf /path/to/llama-fastapi-app/model_cache_gguf/`

Ensure the GGUF_MODEL_PATH in your .env file points to this location.

### Running the Application
**Start the Application**

`python llama.py`

**Test the API**
Use curl or an API client to test the /generate endpoint.

### Running Using Docker
**Build the Docker Image**

`docker build -t llama-fastapi-app .`

**Run the Docker Container**
`docker run -p 8000:8000 llama-fastapi-app`

**API Usage**

POST /generate
```
{
  "prompt": "Your prompt here",
  "system_prompt": "Optional system prompt",
  "max_tokens": 1000
}
```

- prompt: The input text prompt.
- system_prompt: An optional system prompt to guide the model.
- max_tokens: The maximum number of tokens to generate (default is 1000).

**Example Request**
```
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "Hello, how are you?",
           "system_prompt": "You are a helpful assistant.",
           "max_tokens": 50
         }'
```

**Example Response**
```
{
  "response": "I'm doing well, thank you! How can I assist you today?"
}
```

### Settings and Configuration
**Environment Variables**
- HUGGINGFACE_TOKEN: Your Hugging Face API token for authenticated model downloads.
- MODEL_NAME: The Hugging Face model repository name.
- MODEL_CACHE_DIR: Directory to cache the downloaded Hugging Face model.
- RESPONSE_MAX_LENGTH: Maximum length of the generated response.
- GGUF_MODEL_PATH: Path to the pre-converted GGUF model file.

### Application Settings
- n_gpu_layers: Number of layers to offload to the GPU. Adjust this in llama.py based on your GPU capacity.
- n_ctx: Context size for the model (default is 2048).

### License
This project is licensed under the MIT License.

Additional Notes
Model Licensing: Ensure you comply with the licensing terms of the Llama 3.1 model when downloading and using it.
Hardware Requirements: The application may require significant CPU and memory resources, especially for larger models.
GPU Support: For GPU acceleration, ensure CUDA is installed and llama-cpp-python is installed with CUDA support.
Contributing
Contributions are welcome! Please open an issue or submit a pull request.

Contact
For questions or support, please contact your-email@example.com.

Summary
You've now dockerized your application and have a comprehensive README.md to guide users through configuration, model conversion, and running the app. The application is ready to be shared or deployed as needed.