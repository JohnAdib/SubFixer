import re
import sys

def shift_subtitle_by_new_start(input_file, output_file, new_start_time):
    def convert_timecode_to_ms(timecode):
        hours, minutes, seconds, milliseconds = map(int, re.split('[:.,]', timecode))
        total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
        return total_ms
    
    def convert_ms_to_timecode(ms):
        hours = ms // 3600000
        minutes = (ms % 3600000) // 60000
        seconds = (ms % 60000) // 1000
        milliseconds = ms % 1000
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
    
    # Ensure the new_start_time has milliseconds, defaulting to ,000 if not provided
    if len(new_start_time.split(',')) == 1:
        new_start_time += ",000"
    
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Find the first subtitle's original start time
    for line in lines:
        match = re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", line)
        if match:
            original_start_time = match.group(1)
            break

    # Calculate the shift in milliseconds
    original_start_ms = convert_timecode_to_ms(original_start_time)
    new_start_ms = convert_timecode_to_ms(new_start_time)
    shift_ms = new_start_ms - original_start_ms
    
    # Apply the shift to all subtitles and save to the new file
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines:
            match = re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", line)
            if match:
                start_time = match.group(1)
                end_time = match.group(2)
                new_start_time = convert_ms_to_timecode(convert_timecode_to_ms(start_time) + shift_ms)
                new_end_time = convert_ms_to_timecode(convert_timecode_to_ms(end_time) + shift_ms)
                file.write(f"{new_start_time} --> {new_end_time}\n")
            else:
                file.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python subfixer.py <input_file> <output_file> <new_start_time>")
        print("Example of new start time: 00:01:20")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    new_start_time = sys.argv[3]

    shift_subtitle_by_new_start(input_file, output_file, new_start_time)
