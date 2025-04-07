import os
import time
from app.models.chatbot import Chatbot
from app.models.tts import TTS
from app.models.whisper_model import WhisperModel
from app.audio_processing.record_audio import record_audio
from app.audio_processing.play_audio import play_audio
from app.utils.config import Config

class ConversationManager:
    def __init__(self):
        self.chatbot = Chatbot()
        self.tts = TTS(output_dir=Config.AUDIO_DIR)
        self.whisper = WhisperModel(model_size=Config.WHISPER_MODEL_SIZE)
        self.input_audio_path = os.path.join(Config.AUDIO_DIR, "input.wav")
        self.output_audio_path = os.path.join(Config.AUDIO_DIR, "output.mp3")
        self.is_first_interaction = True

    def start_conversation(self):
        print("Starting voice assistant... Say 'exit' to quit.")
        self._speak("Hello! I'm your AI assistant. How can I help you today?")
        
        while True:
            try:
                print("\nListening... (Speak now)")
                record_audio(self.input_audio_path, 
                           duration=Config.DEFAULT_DURATION, 
                           sample_rate=Config.SAMPLE_RATE)
                
                print("Processing...")
                text = self.whisper.transcribe(self.input_audio_path)
                
                if not text.strip():
                    self._speak("Sorry, I didn't hear anything. Could you repeat?")
                    continue
                
                print(f"You: {text}")
                
                if "exit" in text.lower():
                    self._speak("Goodbye! Have a great day.")
                    break
                
                # Only process the actual user input
                response = self.chatbot.get_response(text)
                print(f"Assistant: {response}")
                self._speak(response)
                
            except KeyboardInterrupt:
                self._speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                self._speak("Sorry, I encountered an issue. Let's try again.")
                continue

    def _speak(self, text: str):
        try:
            self.tts.synthesize(text, filename="response.mp3")
            play_audio(os.path.join(Config.AUDIO_DIR, "response.mp3"))
        except Exception as e:
            print(f"TTS Error: {e}")
            print(f"[TTS Failed] Assistant: {text}")

if __name__ == "__main__":
    assistant = ConversationManager()
    assistant.start_conversation()