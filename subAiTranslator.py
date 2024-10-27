import openai
import os
import re
import argparse

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

def read_srt_file(file_path):
    """
    Reads an SRT file and returns a list of subtitle entries.
    Each entry contains the timestamp and the text.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content into individual subtitle blocks
    entries = re.split(r'\n\n', content.strip())
    subtitles = []

    for entry in entries:
        lines = entry.splitlines()
        if len(lines) >= 3:
            index = lines[0].strip()
            timestamp = lines[1].strip()
            text = ' '.join(line.strip() for line in lines[2:])
            subtitles.append((index, timestamp, text))
    
    return subtitles

def translate_subtitles(subtitles, target_language="Persian", chunk_size=5):
    """
    Translates subtitles using OpenAI API in chunks to minimize API calls.
    Returns a list of translated subtitles.
    """
    translated_subtitles = []
    for i in range(0, len(subtitles), chunk_size):
        # Collect a chunk of subtitles
        chunk = subtitles[i:i + chunk_size]
        chunk_text = "\n".join([f"{idx}: {text}" for idx, _, text in chunk])
        
        # Create the prompt for the API
        prompt = f"Translate the following movie subtitles to {target_language} in a human-readable way, understanding the movie context:\n{chunk_text}\n"

        # Call the OpenAI API
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7,
            )

            # Extract the translated text
            translated_text = response.choices[0].message['content'].strip()

            # Split translated_text into lines and match them to the original subtitles
            translated_lines = translated_text.split('\n')
            for j, line in enumerate(translated_lines):
                translated_subtitles.append((subtitles[i + j][0], subtitles[i + j][1], line))

        except Exception as e:
            print(f"Error occurred during translation: {e}")
            break
    
    return translated_subtitles

def save_translated_subtitles(file_path, translated_subtitles):
    """
    Saves the translated subtitles to a new SRT file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for idx, timestamp, text in translated_subtitles:
            file.write(f"{idx}\n{timestamp}\n{text}\n\n")

def main():
    # Set up argument parser for CLI usage
    parser = argparse.ArgumentParser(description="Translate movie subtitles to Persian.")
    parser.add_argument('input_file', type=str, help='Path to the input SRT file')
    parser.add_argument('output_file', type=str, help='Path to save the translated SRT file')
    args = parser.parse_args()

    # Read the original subtitles
    subtitles = read_srt_file(args.input_file)

    # Translate the subtitles
    translated_subtitles = translate_subtitles(subtitles)

    # Save the translated subtitles to a new file
    save_translated_subtitles(args.output_file, translated_subtitles)
    print(f"Translated subtitles saved to {args.output_file}")

if __name__ == "__main__":
    main()
