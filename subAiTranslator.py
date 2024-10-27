import re
import sys
import logging
import openai
import os
import time

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Log only to the console
        ]
    )

def translate_with_openai(chunk, client, max_retries=5):
    chunk_text = "\n".join([f"{number}: {text}" for _, text, number in chunk])
    prompt = (
        "Translate the following English subtitle lines into informal, natural Persian suitable for a Persian-speaking audience. "
        "Keep the tone conversational and human-like:\n\n"
        f"{chunk_text}"
    )
    
    retries = 0
    while retries < max_retries:
        try:
            response = client.completions.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=3000,
                temperature=0.7,
                n=1,
                stop=None
            )
            return response.choices[0].text.strip().split("\n")
        except openai.error.RateLimitError as e:
            wait_time = 2 ** retries
            logging.warning(f"Rate limit reached. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retries += 1
        except openai.error.APIError as e:
            logging.error(f"API Error: {e}")
            break
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            break
    logging.error("Max retries exceeded. Failed to translate chunk.")
    return []

def merge_subtitles_with_translation(english_file, output_file):
    setup_logging()
    logging.info(f"Starting contextual translation for: {english_file}")

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        with open(english_file, 'r', encoding='utf-8') as eng_file:
            english_lines = eng_file.readlines()
            
            english_dialogues = extract_dialogues(english_lines)
            
            chunk_size = 50
            translated_dialogues = []

            for i in range(0, len(english_dialogues), chunk_size):
                chunk = english_dialogues[i:i + chunk_size]
                translated_chunk = translate_with_openai(chunk, client)
                if translated_chunk:
                    translated_dialogues.extend(
                        [(chunk[j][0], translated_chunk[j].strip(), chunk[j][2]) for j in range(len(chunk))]
                    )
                else:
                    logging.error(f"Failed to translate chunk {i // chunk_size + 1}")
            
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
