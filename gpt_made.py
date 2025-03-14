sentences = [
    "car have 4 wheels",
    "jeep have 4 wheels",
    "car have 4 cylinder engine",
    "jeep have 4 cylinder engine"
]

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

# Print the word details
import json
print(json.dumps(word_details, indent=4))
