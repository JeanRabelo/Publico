import json
import re
from collections import defaultdict, Counter

def build_word_followers(text):
    # Split the text into words
    words = re.findall(r'\b\w+\b', text.lower())
    word_followers = defaultdict(list)
    
    # Build a dictionary with each two-word combination and its followers
    for i in range(len(words) - 2):
        current_words = f"{words[i]} {words[i + 1]}"
        next_word = words[i + 2]
        word_followers[current_words].append(next_word)
    
    # For each two-word combination, get the three most common followers
    word_followers_top3 = {phrase: [f[0] for f in Counter(followers).most_common(3)]
                           for phrase, followers in word_followers.items()}
    
    return word_followers_top3

def txt_to_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    word_followers = build_word_followers(text)
    
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(word_followers, json_file, ensure_ascii=False, indent=4)

# Usage example
input_file = 'processed_biblia.txt'  # Replace with your input file path
output_file = 'output2.json'  # Replace with your output file path
txt_to_json(input_file, output_file)

