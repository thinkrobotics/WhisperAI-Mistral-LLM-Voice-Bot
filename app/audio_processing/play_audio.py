from pydub import AudioSegment
from pydub.playback import play

def play_audio(audio_path):
    audio = AudioSegment.from_file(audio_path)
    print("Playing response...")
    play(audio)
    print("Playback finished")