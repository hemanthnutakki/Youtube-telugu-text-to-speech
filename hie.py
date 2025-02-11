import requests
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import asyncio
import edge_tts
from pydub import AudioSegment

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

def optimize_audio(input_file, output_file, format="flac"):
    """Optimize audio quality and convert to FLAC format."""
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format=format)
    print(f"Optimized audio saved as {output_file}")

def main():
    # File paths
    english_audio_path = r"C:\Users\ravin\Downloads\The sacks you use are actually made from plants #shorts.mp3"
    telugu_audio_tts_path = "telugu_audio.wav"  # Intermediate WAV output for high quality
    final_output_flac_path = "telugu_audio_final.flac"  # Lossless FLAC output

    # Step 1: Transcribe the English audio
    print("Transcribing audio...")
    transcribed_text = transcribe_audio(english_audio_path)
    if not transcribed_text:
        print("No transcription available. Exiting.")
        return
    print(f"Transcribed Text: {transcribed_text}")

    # Step 2: Translate to Telugu
    print("Translating text to Telugu...")
    translated_text = translate_text(transcribed_text)
    print(f"Translated Text (Telugu): {translated_text}")

    # Step 3: Convert Telugu text to speech (save as WAV for high quality)
    print("Converting Telugu text to speech...")
    asyncio.run(text_to_speech(translated_text, telugu_audio_tts_path))

    # Step 4: Optimize audio and save in FLAC format
    print("Optimizing audio...")
    optimize_audio(telugu_audio_tts_path, final_output_flac_path, format="flac")
    print(f"Final FLAC audio output saved as: {final_output_flac_path}")

if __name__ == "__main__":
    main()
