import json
import re
from collections import defaultdict, Counter

def build_word_followers(text, n=2):
    # Split the text into words
    words = re.findall(r'\b\w+\b', text.lower())
    word_followers = defaultdict(list)
    
    # Build a dictionary with each n-word combination and its followers
    for i in range(len(words) - n):
        current_words = ' '.join(words[i:i + n])
        next_word = words[i + n]
        word_followers[current_words].append(next_word)
    
    # For each n-word combination, get the three most common followers
    word_followers_top3 = {phrase: [f[0] for f in Counter(followers).most_common(3)]
                           for phrase, followers in word_followers.items()}
    
    return word_followers_top3

def txt_to_json(input_file, output_file, n=2):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    word_followers = build_word_followers(text, n)
    
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(word_followers, json_file, ensure_ascii=False, indent=4)

# Usage example
input_file = 'processed_biblia.txt'  # Replace with your input file path
output_file = 'output.json'  # Replace with your output file path
n = 2  # Set the desired number of words in the key
txt_to_json(input_file, output_file, n)

