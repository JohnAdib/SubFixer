import re
import sys
import logging

def setup_logging():
    # Set up the logging configuration to log only to the console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Log only to the console
        ]
    )

def merge_subtitles(english_file, persian_file, output_file):
    setup_logging()
    logging.info(f"Starting merging of subtitles: {english_file} and {persian_file}")

    try:
        with open(english_file, 'r', encoding='utf-8') as eng_file, open(persian_file, 'r', encoding='utf-8') as per_file:
            english_lines = eng_file.readlines()
            persian_lines = per_file.readlines()
            
            english_dialogues = extract_dialogues(english_lines)
            persian_dialogues = extract_dialogues(persian_lines)
            
            if len(english_dialogues) != len(persian_dialogues):
                logging.warning("The number of dialogues in English and Persian files do not match. Proceeding with minimum count.")
            
            # Open the output file to write merged subtitles
            with open(output_file, 'w', encoding='utf-8') as outfile:
                dialogue_count = min(len(english_dialogues), len(persian_dialogues))
                
                for i in range(dialogue_count):
                    timing = english_dialogues[i][0]
                    text = persian_dialogues[i][1]
                    number = english_dialogues[i][2]
                    
                    outfile.write(f"{number}\n")
                    outfile.write(f"{timing}\n")
                    outfile.write(f"{text}\n\n")
        
        logging.info(f"Subtitle merging complete. Output file saved as: {output_file}")

    except FileNotFoundError as fnf_error:
        logging.error(f"File not found. Please check the file paths.")
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
    if len(sys.argv) != 4:
        print("Usage: python merge_subtitles.py <english_file> <persian_file> <output_file>")
        sys.exit(1)

    english_file = sys.argv[1]
    persian_file = sys.argv[2]
    output_file = sys.argv[3]

    merge_subtitles(english_file, persian_file, output_file)
