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
    def refine_token_index(word_to_token):
        token_index = 0
        for token_phrase in word_to_token:
            word_to_token[token_phrase] = token_index
            token_index += 1
        return word_to_token

    def create_left_phrase(word_details, word):
        left_phrase = " "
        left_words = word_details[word]['left']

        if len(left_words) == 0:
            return left_phrase
        
        elif len(left_words) == 1:
            left_word = left_words[0]
            if len(word_details[left_word]['right']) == 1 and word_details[left_word]['right'][0] == word:
                left_phrase = create_left_phrase(word_details, left_word) + left_word + left_phrase
                return left_phrase
            elif len(word_details[left_word]['right']) > 1:
                return left_phrase

        elif len(left_words) > 1:
            return left_phrase
    
    def create_right_phrase(word_details, word):
        right_phrase = " "
        right_words = word_details[word]['right']

        if len(right_words) == 0:
            return right_phrase
        
        elif len(right_words) == 1:
            right_word = right_words[0]
            if len(word_details[right_word]['left']) == 1 and word_details[right_word]['left'][0] == word:
                right_phrase = right_phrase + right_word + create_right_phrase(word_details, right_word)
                return right_phrase
            elif len(word_details[right_word]['left']) > 1:
                return right_phrase

        elif len(right_words) > 1:
            return right_phrase

    word_to_token = {}
    token_index = 0
    for word in word_details:
        word_to_token[create_left_phrase(word_details, word) + word + create_right_phrase(word_details, word)] = token_index
        token_index += 1
    
    return refine_token_index(word_to_token)

#print(json.dumps(tokenize(generate_word_details(read_sentences("d.json"))), indent=4))
print(json.dumps(tokenize(generate_word_details(read_sentences("d.json"))), indent=4))

