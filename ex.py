import edge_tts
import asyncio


async def text_to_speech(text: str, output_filename: str):
    # Specify the voice as te-IN-MohanNeural
    communicate = edge_tts.Communicate(text, voice='te-IN-MohanNeural')

    try:
        # Generate the audio from text
        await communicate.save(output_filename)
        print(f"Audio saved as {output_filename}")
    except Exception as e:
        print(f"Error occurred: {e}")


# Define the text you want to convert to speech (in Telugu)
text = "ఎనిమిదవ తరగతినుండి మొదలు పెడితే డిగ్రీ వరకు 'తెలుగువాక్యం' పాఠ్యాంశంగా ఉంది. అంతేగాకుండా రకరకాలైన పోటీపరీక్షల్లో కూడ దీని అవసరం ఉంది. అందుకే విద్యార్థుల సౌకర్యార్థం దానికి సంబంధించిన పాఠాలు అందిస్తున్నాం."  # "Hello, how are you?" in Telugu

# Output audio filename
output_filename = "output_audio_te_in_mohan.mp3"

# Run the text to speech function
asyncio.run(text_to_speech(text, output_filename))
