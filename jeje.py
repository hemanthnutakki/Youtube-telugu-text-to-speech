import librosa
import soundfile as sf

def change_speed_librosa(input_file, output_file, speed_factor):
    # Load audio
    audio, sr = librosa.load(input_file, sr=None)

    # Perform time-stretching on the audio signal
    sped_up_audio = librosa.effects.time_stretch(y=audio, rate=speed_factor)

    # Save the modified audio
    sf.write(output_file, sped_up_audio, sr)
    print(f"Audio saved at {output_file} with {speed_factor}x speed.")

input_audio_file = r"C:\\Users\\ravin\\PycharmProjects\\TELUGU VOICES\\output_audio_te_in_mohan.mp3"
output_audio_file = r"C:\\Users\\ravin\\Downloads\\high_quality_sped_up.mp3"
speed_factor = 1.434

change_speed_librosa(input_audio_file, output_audio_file, speed_factor)
