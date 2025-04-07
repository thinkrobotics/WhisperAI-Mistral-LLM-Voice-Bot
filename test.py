# from gtts import gTTS

# # Define the text to be spoken
# text = "Goodbye, see you later! Bye for now!"

# # Generate speech
# tts = gTTS(text, lang="en")

# # Save the file
# file_path = "bye_message.mp3"
# tts.save(file_path)

# print(f"Audio file saved as {file_path}")


import requests

url = "http://127.0.0.1:8000/process_audio/"
file_path = r"D:\Speech_Assistent\bye_message.mp3"  

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print(response.json())  # Print API response

