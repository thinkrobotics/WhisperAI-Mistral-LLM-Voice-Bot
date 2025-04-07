from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from app.models.chatbot import Chatbot
from app.models.tts import TTS
from app.models.whisper_model import WhisperModel
from app.audio_processing.record_audio import record_audio
from app.audio_processing.save_audio import save_audio
from app.audio_processing.play_audio import play_audio
from app.utils.config import Config
import os

app = FastAPI(title="Speech Conversation API", description="An API for real-time speech-based conversations.")

# Reinitialize chatbot to ensure the updated version is used
chatbot = Chatbot()
tts = TTS(output_dir=Config.AUDIO_DIR)
whisper = WhisperModel(model_size=Config.WHISPER_MODEL_SIZE)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Landing page with API details"""
    return """
    <html>
        <head>
            <title>Speech Conversation API</title>
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1>Welcome to the Speech Conversation API</h1>
            <p>This API enables real-time speech-to-text, chatbot interaction, and text-to-speech.</p>
            <p><b>Available Endpoints:</b></p>
            <ul style="list-style: none;">
                <li><a href="/docs" target="_blank">📖 API Documentation (Swagger UI)</a></li>
                <li><a href="/redoc" target="_blank">📜 API Documentation (ReDoc)</a></li>
            </ul>
        </body>
    </html>
    """

@app.post("/process_audio/")
async def process_audio(file: UploadFile = File(...)):
    """Processes an uploaded audio file"""
    audio_path = save_audio(await file.read(), "input.wav", Config.AUDIO_DIR)
    text = whisper.transcribe(audio_path)
    response_text = chatbot.get_response(text)
    output_audio_path = tts.synthesize(response_text)
    play_audio(output_audio_path)  # Play the response immediately
    return {
        "transcribed_text": text,
        "response_text": response_text,
        "audio_response_path": output_audio_path
    }

@app.get("/converse/")
async def converse():
    """Handles a single turn of real-time conversation"""
    input_audio_path = os.path.join(Config.AUDIO_DIR, "input.wav")
    output_audio_path = os.path.join(Config.AUDIO_DIR, "output.mp3")
    
    # Record audio from the user
    record_audio(input_audio_path, duration=Config.DEFAULT_DURATION, sample_rate=Config.SAMPLE_RATE)
    
    # Transcribe the audio
    text = whisper.transcribe(input_audio_path)
    print(f"You said: {text}")
    
    # Get chatbot response
    response_text = chatbot.get_response(text)
    print(f"Chatbot: {response_text}")
    
    # Synthesize and play the response
    tts.synthesize(response_text, filename="output.mp3")
    play_audio(output_audio_path)
    
    return {
        "transcribed_text": text,
        "response_text": response_text,
        "audio_response_path": output_audio_path
    }