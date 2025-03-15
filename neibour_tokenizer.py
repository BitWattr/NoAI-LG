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

    def create_best_phrase_combination_for_word(key, word_details):

        def create_left_phrase(key, word_details):
            left_word = word_details[key]["left"][0]
            left_phrase = ""
            if len(word_details[left_word]['right']) == 1 and len(word_details[left_word]['right'][0] == key):
                left_phrase = left_word + " "
                return left_phrase

            elif len(word_details[left_word]['right']) > 1:
                left_phrase = ""
                return left_phrase


        left_words = word_details[key]["left"]
        right_words = word_details[key]["right"]

        if (left_words.isEmpty() or len(left_words) > 1) and (right_words.isEmpty() or len(right_words) > 1):
            # individual word is the token
            return key

        elif len(left_words) == 1:
            # there is left dependency
            create_left_phrase(key, word_details)


    word_to_token = {}
    token_index = 0
    for key in word_details.items():
        word_to_token[create_best_phrase_combination_for_word(key, word_details)] = token_index
        token_index += 1




print(tokenize(generate_word_details(read_sentences("d.json"))))