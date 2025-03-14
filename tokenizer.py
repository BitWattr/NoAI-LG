import json
from collections import Counter

n = 3


def read_sentences(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["sentences"]

def generate_ngrams(sentence, n):
    words = sentence.split()
    return [" ".join(words[i:i+n]) for i in range(len(words) - n + 1)]


def create_n_grams_dict():
    sentences = read_sentences("d.json")
    n_grams = {}
    for i in range(n, 0, -1):
        n_grams[i] = []
        for sentence in sentences:
            n_grams[i].extend(generate_ngrams(sentence, i))
    return n_grams



def remove_uncommoni(n_grams_dict):
    for n_gram in n_grams_dict.values():
        for n_words in n_gram:
            if n_gram.count(n_words) < 2:
                n_gram.remove(n_words)
    return n_grams_dict
            
def remove_uncommon(n_grams_dict):
    for key, n_gram in n_grams_dict.items():  # Iterate with key to modify the original dict
        to_remove = [word for word in n_gram if n_gram.count(word) < 2]  # Identify words to remove
        
        for word in to_remove:
            print(f"Removing '{word}' from {key}")
            n_gram.remove(word)  # Remove word from the original list
            
    return n_grams_dict


print(remove_uncommon(create_n_grams_dict()))