import os

def save_audio(audio_data, filename="input.wav", output_dir="audio_files"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "wb") as f:
        f.write(audio_data)
    return output_path