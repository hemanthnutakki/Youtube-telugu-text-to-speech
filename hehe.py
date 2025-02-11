import os
from pydub import AudioSegment, effects  # Ensure you install pydub with `pip install pydub`

# Define file paths
input_file = r"C:\Users\ravin\Downloads\The sacks you use are actually made from plants #shorts.mp3"
telugu_file = r"C:\Users\ravin\PycharmProjects\TELUGU VOICES\output_audio_te_in_mohan.mp3"

# Load the input and Telugu files
input_audio = AudioSegment.from_file(input_file)
telugu_audio = AudioSegment.from_file(telugu_file)

# Get durations in milliseconds
input_duration = len(input_audio)
telugu_duration = len(telugu_audio)

# Print durations for debugging
print(f"Original Input file duration: {input_duration / 1000} seconds")
print(f"Original Telugu file duration: {telugu_duration / 1000} seconds")

# Calculate speed factor
speed_factor = telugu_duration / input_duration

# Print speed factor for debugging
print(f"Speed Factor: {speed_factor}")

# Adjust Telugu file speed to match input file duration using effects.speedup
adjusted_telugu_audio = effects.speedup(telugu_audio, playback_speed=speed_factor)

# Verify adjusted duration
adjusted_telugu_duration = len(adjusted_telugu_audio)

# Print adjusted duration for debugging
print(f"Adjusted Telugu file duration: {adjusted_telugu_duration / 1000} seconds")

# Check if the adjusted duration matches the input duration
if abs(adjusted_telugu_duration - input_duration) < 1:  # Allowing slight deviation
    print("The adjusted Telugu file duration matches the input file duration.")
else:
    print("The adjusted Telugu file duration does not match the input file duration. Please check the speed adjustment logic.")

# Export the adjusted Telugu file
output_telugu_file = r"C:\Users\ravin\PycharmProjects\TELUGU VOICES\output_audio_te_in_mohan_adjusted.mp3"
adjusted_telugu_audio.export(output_telugu_file, format="mp3")

print(f"Adjusted Telugu file saved to: {output_telugu_file}")
