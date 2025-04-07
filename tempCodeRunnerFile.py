import os
import warnings
from app.models.chatbot import Chatbot
from app.models.tts import TTS
from app.models.whisper_model import WhisperModel
from app.audio_processing.record_audio import record_audio
from app.audio_processing.play_audio import play_audio
from app.utils.config import Config
from transformers import pipeline

# Suppress FP16 warning from Whisper
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Initialize Hugging Face chatbot model
chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

def main():
    # Initialize components
    tts = TTS(output_dir=Config.AUDIO_DIR)
    whisper = WhisperModel(model_size=Config.WHISPER_MODEL_SIZE)
    
    # Ensure audio directory exists
    if not os.path.exists(Config.AUDIO_DIR):
        os.makedirs(Config.AUDIO_DIR)
    
    input_audio_path = os.path.join(Config.AUDIO_DIR, "input.wav")
    output_audio_path = os.path.join(Config.AUDIO_DIR, "output.mp3")
    
    print("Starting conversation... Say something to begin (or say 'exit' to stop).")
    
    while True:
        # Record user's speech
        record_audio(input_audio_path, duration=Config.DEFAULT_DURATION, sample_rate=Config.SAMPLE_RATE)
        
        # Transcribe the audio
        try:
            text = whisper.transcribe(input_audio_path)
            print(f"You: {text}")
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            text = ""
        
        if text.lower() == "exit":
            print("Exiting the conversation.")
            break

        # Generate chatbot response using Hugging Face's model
        response = chatbot(text)[0]['generated_text']
        print(f"Chatbot: {response}")
        
        # Synthesize and play the response
        tts.synthesize(response, filename="output.mp3")
        play_audio(output_audio_path)

if __name__ == "__main__":
    main()
