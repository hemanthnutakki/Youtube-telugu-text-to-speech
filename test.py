from telugu_phoneme_mapper import map_to_phonemes

telugu_text ="""ఇది మృదువైన బంగారం అని కూడా పిలువబడే భారతీయ రైతు పంటలు భారతదేశంలో జుడ్ అనేది సంచులు వంటి అనేక రోజువారీ వస్తువులను తయారు చేయడానికి ఉపయోగించే ముడి పదార్థం పంట కోసిన తరువాత త్రాడులు మరియు కర్టెన్లు జ్యూట్ పైభాగంలో చెత్త పొరతో కొంతకాలం నది నీటిలో నా"""
phonemes = map_to_phonemes(telugu_text)
print(phonemes)  # Outputs: avunu
