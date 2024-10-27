import re
import sys
import logging
from googletrans import Translator

def setup_logging():
    # Set up the logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("translation.log"),  # Log to a file
            logging.StreamHandler()  # Log to the console
        ]
    )

def translate_subtitle(input_file, output_file, target_language="fa"):
    translator = Translator()
    setup_logging()
    logging.info(f"Starting translation for file: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        line_count = len(lines)
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for idx, line in enumerate(lines):
                # Log the progress every 10 lines
                if idx % 10 == 0:
                    logging.info(f"Translating line {idx + 1}/{line_count}")
                
                # Check if the line is a timecode line
                if re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", line):
                    outfile.write(line)
                elif line.strip().isdigit() or line.strip() == "":
                    # Keep line numbers and empty lines unchanged
                    outfile.write(line)
                else:
                    try:
                        # Translate subtitle text
                        translated_text = translator.translate(line.strip(), dest=target_language).text
                        outfile.write(translated_text + "\n")
                    except Exception as e:
                        logging.error(f"Error translating line {idx + 1}: {line.strip()}")
                        logging.error(f"Exception: {e}")
                        outfile.write(line)  # Add the original line if translation fails
        
        logging.info(f"Translation complete. Translated file saved as: {output_file}")

    except Exception as e:
        logging.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python translate_subtitle.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    translate_subtitle(input_file, output_file)
