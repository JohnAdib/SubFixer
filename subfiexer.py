import re
import sys

def shift_subtitle(input_file, output_file, shift_seconds):
    def shift_timecode(timecode, shift_ms):
        # Convert timecode to milliseconds
        hours, minutes, seconds, milliseconds = map(int, re.split('[:.,]', timecode))
        total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
        # Shift the time
        new_total_ms = total_ms + shift_ms
        
        # Prevent negative timecodes
        if new_total_ms < 0:
            new_total_ms = 0
        
        # Convert back to hours, minutes, seconds, and milliseconds
        hours = new_total_ms // 3600000
        minutes = (new_total_ms % 3600000) // 60000
        seconds = (new_total_ms % 60000) // 1000
        milliseconds = new_total_ms % 1000
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    shift_ms = shift_seconds * 1000
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines:
            match = re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", line)
            if match:
                start_time = match.group(1)
                end_time = match.group(2)
                new_start_time = shift_timecode(start_time, shift_ms)
                new_end_time = shift_timecode(end_time, shift_ms)
                file.write(f"{new_start_time} --> {new_end_time}\n")
            else:
                file.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python subfixer.py <input_file> <output_file> <shift_seconds>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    shift_seconds = int(sys.argv[3])

    shift_subtitle(input_file, output_file, shift_seconds)
