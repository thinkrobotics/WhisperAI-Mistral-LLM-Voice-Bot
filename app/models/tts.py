import gtts
import os

class TTS:
    def __init__(self, output_dir="audio_files"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def synthesize(self, text, filename="output.mp3"):
        tts = gtts.gTTS(text=text, lang='en')
        output_path = os.path.join(self.output_dir, filename)
        tts.save(output_path)
        return output_path