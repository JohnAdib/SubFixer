import re
import sys
import logging
import openai
import os

def setup_logging():
    # Set up the logging configuration to log only to the console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Log only to the console
        ]
    )

def translate_with_openai(chunk):
    """
    Translates a chunk of subtitles using OpenAI's GPT-4 API.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Prepare the input text for the API
    chunk_text = "\n".join([f"{number}: {text}" for _, text, number in chunk])
    prompt = (
        "You are a Persian translator. Translate the following subtitle lines into informal, "
        "natural Persian that is suitable for a Persian-speaking audience. "
        "Keep the formatting intact, but make sure the tone feels conversational and human-like:\n\n"
        f"{chunk_text}"
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful and creative Persian translator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    
    translated_text = response.choices[0].message['content']
    
    # Split the translated text back into individual lines corresponding to the chunk
    translated_lines = translated_text.split("\n")
    translations = []
    for i, line in enumerate(translated_lines):
        if i < len(chunk):
            timing, _, number = chunk[i]
            translations.append((timing, line.strip(), number))
    
    return translations

def merge_subtitles_with_translation(english_file, output_file):
    setup_logging()
    logging.info(f"Starting contextual translation for: {english_file}")

    try:
        with open(english_file, 'r', encoding='utf-8') as eng_file:
            english_lines = eng_file.readlines()
            
            english_dialogues = extract_dialogues(english_lines)
            
            chunk_size = 50  # A manageable chunk size for API processing
            translated_dialogues = []

            # Process the file in chunks
            for i in range(0, len(english_dialogues), chunk_size):
                chunk = english_dialogues[i:i + chunk_size]
                translated_chunk = translate_with_openai(chunk)
                translated_dialogues.extend(translated_chunk)
            
            # Open the output file to write merged subtitles
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for timing, text, number in translated_dialogues:
                    outfile.write(f"{number}\n")
                    outfile.write(f"{timing}\n")
                    outfile.write(f"{text}\n\n")
        
        logging.info(f"Subtitle translation complete. Output file saved as: {output_file}")

    except FileNotFoundError:
        logging.error(f"File not found. Please check the file path: {english_file}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def extract_dialogues(lines):
    """
    Extracts dialogues with their corresponding numbers and timings.
    Returns a list of tuples (timing, text, number).
    """
    dialogues = []
    number = None
    timing = None
    text = []
    
    for line in lines:
        line = line.strip()
        if line.isdigit():
            number = line
        elif re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", line):
            timing = line
        elif line:
            text.append(line)
        else:
            if number and timing and text:
                dialogues.append((timing, ' '.join(text), number))
                number = None
                timing = None
                text = []
    
    # Handle the last block in the file if there's no trailing newline
    if number and timing and text:
        dialogues.append((timing, ' '.join(text), number))
    
    return dialogues

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_subtitles_with_translation.py <english_file> <output_file>")
        sys.exit(1)

    english_file = sys.argv[1]
    output_file = sys.argv[2]

    merge_subtitles_with_translation(english_file, output_file)
