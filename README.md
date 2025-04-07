
# Voice Assistant with Local LLM and Audio I/O

This project is a comprehensive **voice assistant system** implemented in Python that functions entirely offline. It combines speech recognition, a locally hosted language model, and text-to-speech capabilities to deliver a seamless voice interaction experience.

---

## 🔧 Features

- 🎙️ **Speech Recognition**: Converts voice to text using OpenAI Whisper.
- 🤖 **Conversational Intelligence**: Powered by TinyLlama 1.1B GGUF model running with CTransformers.
- 🗣️ **Text-to-Speech (TTS)**: Generates voice responses using a custom TTS module.
- 🔁 **Voice Interaction Loop**: Record → Transcribe → Respond → Speak.
- 🧠 **Factual Knowledge**: Built-in fact resolution for known queries (like Indian political figures).
- 💻 **Fully Offline**: Runs without internet after setup.
- 🎚️ **Error Tolerant**: Handles silence, errors, and interruptions gracefully.

---

## 📁 Project Structure

```bash
voice-assistant/
├── app/
│   ├── audio_processing/
│   │   ├── record_audio.py       # Records audio from mic
│   │   └── play_audio.py         # Plays generated TTS
│   ├── models/
│   │   ├── chatbot.py            # Chat logic and response
│   │   ├── tts.py                # Text-to-speech synthesis
│   │   └── whisper_model.py      # Whisper-based transcription
│   └── utils/
│       └── config.py             # Configuration variables
├── local_llm.py                  # Loads and interacts with local LLM
├── main.py                       # Main interaction loop
└── README.md
```

---

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
Ensure you have `ffmpeg` installed for audio handling.

### 2. Download Models
- **Whisper**: Installed via `openai-whisper`
- **TinyLlama GGUF**: [Download from HuggingFace](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF) and place it in `models/`

---

## 🔊 Audio Workflow

### 1. Record Audio
```python
record_audio(path, duration, sample_rate)
```
Records user input and stores it as WAV.

### 2. Speech to Text
```python
WhisperModel.transcribe(path)
```
Uses Whisper to convert WAV to text.

### 3. Text to Speech + Playback
```python
TTS.synthesize(text, filename)
play_audio(filepath)
```
Synthesizes speech and plays it back to user.

---

## 🧠 Chatbot Intelligence

### Fact-based Responses
- Recognizes and answers time-specific questions about Indian leaders.
- Supports queries like "Who was the Prime Minister of India in 2014?"

### LLM-based Responses
- If no factual match is found, input is sent to TinyLlama for a smart reply.
- Enhances prompts with current date for better relevance.

---

## 🛠️ Local LLM (TinyLlama)

### Powered by CTransformers
- Model: `tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf`
- Threads: 8
- GPU Support: Configurable (currently CPU-only)

```python
response = llm.generate_response(prompt)
```

---

## 🔄 Main Interaction Loop

```python
assistant = ConversationManager()
assistant.start_conversation()
```
The user speaks → assistant transcribes → chatbot replies → TTS responds.

---

## 🧩 Config File (`config.py`)
```python
AUDIO_DIR = "path/to/audio"
DEFAULT_DURATION = 5  # seconds
SAMPLE_RATE = 16000
WHISPER_MODEL_SIZE = "base"
```

---

## ⚠️ Error Handling

- Empty input: prompts re-recording
- KeyboardInterrupt: exits gracefully
- Exceptions: logs and continues loop

---

## 🚫 Known Limitations

- No conversation memory
- No contextual awareness
- Cannot answer real-time news or internet-based queries
- LLM may hallucinate or give verbose answers

---

## 🌱 Future Enhancements

- Add memory and contextual flow
- Replace TTS with more natural voice
- Switch to `faster-whisper` for faster inference
- Add multi-language support
- Add GUI interface for desktop use

---

## 🙏 Credits

- [OpenAI Whisper](https://github.com/openai/whisper)
- [TinyLlama](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF)
- [CTransformers](https://github.com/marella/ctransformers)

---

## 📄 License

MIT License. You are free to use, modify, and distribute with attribution.

---

## 👨‍💻 Author

Developed by **Dhruv Khatter**
