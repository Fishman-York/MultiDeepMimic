

#this is for the output of the logs created by deepmimic
input_file = 'data/raw/multi_punch_char_2.txt'

def read_file(file_path):
    with open(file_path, 'r') as file:
        headers = file.readline().strip().split()
        for line in file:
            pass
        last_line = line.strip()
    return headers, last_line
        
def print_vertical_table(headers, values):
    max_header_length = max(len(header) for header in headers)
    for header, value in zip(headers, values):
        print(f"{header.ljust(max_header_length)} | {value}")

def main(file_path):
    headers, last_line = read_file(file_path)

    if headers and last_line:
        values = last_line.split()
        print("Agent Output:")
        print("-" * 30)
        print_vertical_table(headers, values)
    else:
        print("The file is empty or couldn't be read.")

main(input_file)