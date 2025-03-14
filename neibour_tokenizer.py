import json


def read_sentences(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["sentences"]

def generate_word_details(sentences):
    # Dictionary to store word details
    word_details = {}

    # Process each sentence
    for sentence in sentences:
        words = sentence.split()
        for i, word in enumerate(words):
            if word not in word_details:
                word_details[word] = {"left": [], "right": []}
            
            # Add left word if exists
            if i > 0:
                left_word = words[i - 1]
                if left_word not in word_details[word]["left"]:
                    word_details[word]["left"].append(left_word)
            
            # Add right word if exists
            if i < len(words) - 1:
                right_word = words[i + 1]
                if right_word not in word_details[word]["right"]:
                    word_details[word]["right"].append(right_word)
    return word_details


def tokenize(word_details):
    for key, word in word_details.items():
        if word["left"].isEmpty():
            


print(tokenize(generate_word_details(read_sentences("d.json"))))