import unittest
from telugu_phoneme_mapper import  process_text

class TestTeluguPhonemeMapper(unittest.TestCase):

    def test_process_text_unsupported_characters(self):
        """Test process_text with unsupported characters"""
        input_text = """
        చేతిలో పదివేల ఐదువందల రూపాయలతో ఐదుగురు స్నేహితులున్నారు.

        వారు హోటల్‌కి వెళ్లి ఏడు వందల ఎనభై తొమ్మిది రూపాయలు మాత్రమే ఖర్చు చేశారు.

        మిగిలిన రెండు వందల పదకొండు వారు తిరిగి ఇంటికి వెళ్లేందుకు ఖర్చు చేశారు."""
        result = process_text(input_text)
        print(f"Input: {input_text}, \nOutput: {result}")
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()
