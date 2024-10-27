import re
import sys
from googletrans import Translator

def translate_subtitle(input_file, output_file, target_language="fa"):
    translator = Translator()
    
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    translated_lines = []
    for line in lines:
        # Check if the line is a timecode line
        if re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", line):
            translated_lines.append(line)
        elif line.strip().isdigit() or line.strip() == "":
            # Keep line numbers and empty lines unchanged
            translated_lines.append(line)
        else:
            # Translate subtitle text
            translated_text = translator.translate(line.strip(), dest=target_language).text
            translated_lines.append(translated_text + "\n")
    
    # Write translated subtitles to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(translated_lines)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python translate_subtitle.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    translate_subtitle(input_file, output_file)
