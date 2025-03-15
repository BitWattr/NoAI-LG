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
    def create_left_phrase(word_details, word):
        left_phrase = ""
        if len(word_details[word]['left']) == 1:
            left_word = word_details[word]['left'][0]
            if len(word_details[left_word]['right']) == 1 and word_details[left_word]['right'][0] == word:
                return create_left_phrase(word_details, left_word) + left_word + " "
        return left_phrase

    def create_right_phrase(word_details, word):
        right_phrase = ""
        if len(word_details[word]['right']) == 1:
            right_word = word_details[word]['right'][0]
            if len(word_details[right_word]['left']) == 1 and word_details[right_word]['left'][0] == word:
                return " " + right_word + create_right_phrase(word_details, right_word)
        return right_phrase

    word_to_token = {}
    token_index = 0
    for word in word_details:
        phrase = create_left_phrase(word_details, word) + word + create_right_phrase(word_details, word)
        if phrase not in word_to_token:  # Ensure uniqueness
            word_to_token[phrase] = token_index
            token_index += 1
    
    return word_to_token

# Run the fixed code
print(tokenize(generate_word_details(read_sentences("d.json"))))
