import requests
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from pydub import AudioSegment
import asyncio
import edge_tts

# Whisper API Configuration
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
HEADERS = {"Authorization": "Bearer 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"}

def transcribe_audio(file_path):
    """Send audio file to Whisper API and get the transcription."""
    with open(file_path, "rb") as f:
        audio_data = f.read()
    response = requests.post(API_URL, headers=HEADERS, data=audio_data)
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ""

def split_text(text, max_length=256):
    """Split text into smaller chunks to avoid translation truncation."""
    sentences = text.split('. ')  # Split by sentences for better readability
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def translate_text(text, model_checkpoint="aryaumesh/english-to-telugu", max_length=256):
    """Translate text using MBart model with chunking and recombination."""
    tokenizer = MBart50TokenizerFast.from_pretrained(model_checkpoint)
    model = MBartForConditionalGeneration.from_pretrained(model_checkpoint)
    translated_chunks = []
    for chunk in split_text(text, max_length=max_length):
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=max_length)
        outputs = model.generate(**inputs, max_length=max_length)
        translated_chunks.append(tokenizer.decode(outputs[0], skip_special_tokens=True))
    return " ".join(translated_chunks)

async def text_to_speech(text, output_filename):
    """Convert text to speech using edge_tts."""
    communicate = edge_tts.Communicate(text, voice='te-IN-MohanNeural')
    try:
        await communicate.save(output_filename)
        print(f"Audio saved as {output_filename}")
    except Exception as e:
        print(f"Error occurred: {e}")




def main():
    # File paths
    english_audio_path = r"C:\Users\ravin\Downloads\The sacks you use are actually made from plants #shorts.mp3"
    telugu_audio_tts_path = "telugu_audio.mp3"
    adjusted_telugu_audio_path = "telugu_audio_adjusted.mp3"
    final_output_path = "final_output.mp3"

    # Transcribe the English audio
    print("Transcribing audio...")
    transcribed_text = transcribe_audio(english_audio_path)
    if not transcribed_text:
        print("No transcription available. Exiting.")
        return
    print(f"Transcribed Text: {transcribed_text}")

    # Translate to Telugu
    print("Translating text to Telugu...")
    translated_text = translate_text(transcribed_text)
    print(f"Translated Text (Telugu): {translated_text}")

    # Convert Telugu text to speech
    print("Converting Telugu text to speech...")
    asyncio.run(text_to_speech(translated_text, telugu_audio_tts_path))



if __name__ == "__main__":
    main()
