import os
import pandas as pd
from telugu_phoneme_mapper import process_text

# Paths
data_folder = r"C:\Users\ravin\Downloads\te_in_male"
tsv_file = os.path.join(data_folder, "line_index.tsv")
output_file = os.path.join(data_folder, "metadata.csv")

# Load the .tsv file with proper decoding using utf-8-sig
with open(tsv_file, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

# Prepare the metadata
metadata = []

for line in lines:
    # Split the line into filename and transcript (Telugu text)
    file_name, text = line.strip().split("\t")

    # Clean up any extra spaces or newlines from the text
    text = text.strip()

    # Construct the audio file path
    audio_path = os.path.join(data_folder, f"{file_name}.wav")

    # Convert the transcript to phoneme representation using the process_text function
    phoneme_representation = process_text(text)

    # Add entry to metadata list
    metadata.append([audio_path, text, phoneme_representation])

# Create a pandas DataFrame for easy handling and proper encoding
df = pd.DataFrame(metadata, columns=["audio_file_path", "transcript", "phoneme_representation"])

# Save the metadata to a CSV file using utf-8-sig encoding
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Metadata saved to: {output_file}")
