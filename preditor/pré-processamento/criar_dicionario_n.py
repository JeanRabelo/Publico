import json
import re
from collections import defaultdict, Counter

def build_word_followers(text, n=2, max_predictions=3):
    # Split the text into words, allowing apostrophes within words
    words = re.findall(r"\b[\w']+\b", text.lower())
    word_followers = defaultdict(list)
    
    # Build a dictionary with each n-word combination and its followers
    for i in range(len(words) - n):
        current_words = ' '.join(words[i:i + n])
        next_word = words[i + n]
        word_followers[current_words].append(next_word)
    
    # For each n-word combination, get the most common followers up to max_predictions
    word_followers_top = {phrase: [f[0] for f in Counter(followers).most_common(max_predictions)]
                          for phrase, followers in word_followers.items()}
    
    return word_followers_top

def txt_to_json(input_file, output_file, n=2, max_predictions=3):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    word_followers = build_word_followers(text, n, max_predictions)
    
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(word_followers, json_file, ensure_ascii=False, indent=4)

# Usage example
input_file = 'constituição_americana.txt'  # Replace with your input file path
n = 3  # Set the desired number of words in the key
max_predictions = 5  # Set the maximum number of predictions
output_file = f'output_{n}_{max_predictions}.json'  # Replace with your output file path
txt_to_json(input_file, output_file, n, max_predictions)

