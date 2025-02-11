import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

# Use CPU instead of GPU
device = "cpu"  # Force the model to use CPU

# Load model and tokenizer
model = ParlerTTSForConditionalGeneration.from_pretrained("ai4bharat/indic-parler-tts").to(device)
tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-parler-tts")
description_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)

# Example input prompt
prompt = """ఇది భారతదేశంలో జనపనారను పండించే భారతీయ రైతు, దీనిని సాఫ్ట్ గోల్డ్ అని కూడా పిలుస్తారు. జనపనార అనేది బస్తాలు, తాడులు మరియు కర్టెన్లు వంటి అనేక రోజువారీ వస్తువులను తయారు చేయడానికి ఉపయోగించే ముడి పదార్థం. పంట కోసిన తరువాత, జనపనారను నది నీటిలో కొంత సమయం పాటు నానబెట్టి, పైన మట్టి పొరను వ్యాపించి ఉంచుతారు. ఇది మొక్క నుండి మలినాలను మరియు చేదును తొలగించడంలో సహాయపడుతుంది, అదే సమయంలో ప్రాసెసింగ్ కోసం ఫైబర్‌లను వేరు చేయడం సులభం చేస్తుంది. ఒకసారి నానబెట్టిన తరువాత, జనపనార యొక్క బయటి పొర సులభంగా పీల్ అవుతుంది. బలమైన మరియు ధరించడానికి-నిరోధకత కలిగిన ఫైబర్‌లను తీయడమే లక్ష్యం. పీల్ చేసిన తర్వాత, తదుపరి దశల కోసం వర్క్‌షాప్‌లకు పంపే ముందు ఫైబర్‌లను ఎండలో ఎండబెట్టాలి. వర్క్‌షాప్‌ల వద్ద, యంత్రాలు వదులుగా ఉండే ఫైబర్‌ల ద్వారా దువ్వెనతో సహజ జనపనార కట్టలను సృష్టిస్తాయి. ఈ ఫైబర్‌లను నూలుగా తిప్పవచ్చు లేదా రగ్గులు మరియు ఇతర నేసిన ఉత్పత్తులను తయారు చేయవచ్చు. జనపనార అంతులేని ఉపయోగాలతో చాలా బహుముఖమైనది."""

description = "Prakash's voice is monotone yet slightly fast in delivery, with a very close recording that almost has no background noise."

# Tokenize the description and prompt
description_input_ids = description_tokenizer(description, return_tensors="pt").to(device)
prompt_input_ids = tokenizer(prompt, return_tensors="pt").to(device)

# Generate speech from the prompt and description
generation = model.generate(input_ids=description_input_ids.input_ids,
                            attention_mask=description_input_ids.attention_mask,
                            prompt_input_ids=prompt_input_ids.input_ids,
                            prompt_attention_mask=prompt_input_ids.attention_mask)

# Convert generated speech to numpy array and save as wav file
audio_arr = generation.cpu().numpy().squeeze()
sf.write("indic_tts_out.wav", audio_arr, model.config.sampling_rate)
