def process_bible_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Check if the line starts with one or more digits followed by a space
            if line.strip() and line.split()[0].isdigit():
                # Remove the number(s) and space at the beginning of the line
                content = ' '.join(line.split()[1:])
                outfile.write(content + '\n')

# Specify the input and output files
input_file = 'biblia-em-txt.txt'
output_file = 'processed_biblia.txt'

# Process the file
process_bible_file(input_file, output_file)

print(f"Processing complete. The output is saved in '{output_file}'.")

