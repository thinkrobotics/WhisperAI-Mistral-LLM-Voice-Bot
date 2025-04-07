from ctransformers import AutoModelForCausalLM
import os
import warnings

# Disable all warnings
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
os.environ['CTRANSFORMERS_NO_SYMLINK_WARNING'] = '1'

class LocalLLM:
    def __init__(self):
        self.model_path = "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
        
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}\n"
                "Please download it manually from:\n"
                "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
            )
            
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path_or_repo_id=self.model_path,
            model_type="llama",
            local_files_only=True,
            gpu_layers=0,  # Set to 30+ if you have NVIDIA GPU
            threads=8       # CPU threads to use
        )
    
    def generate_response(self, prompt_text):
        try:
            # Only process the single user input
            full_prompt = f"User: {prompt_text}\nAssistant:"
            
            response = self.model(
                full_prompt,
                max_new_tokens=150,  # Reduced from 300
                temperature=0.7,
                stop=["User:", "\n\n"]  # Stop if it tries to generate user input
            )
            
            # Clean up response
            if "Assistant:" in response:
                response = response.split("Assistant:")[-1].strip()
            return response
        except Exception as e:
            warnings.warn(f"Generation error: {e}")
            return None