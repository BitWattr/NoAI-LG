import re

sentences = [
    "<s> car have 4 wheels <e>",
    "<s> jeep have 4 wheels <e>",
    "<s> car have 4 cylinder engine <e>",
    "<s> jeep have 4 cylinder engine <e>"
]

tokenizer = {
    " <s> ": 0,
    " car ": 1,
    " have 4 ": 2,
    " wheels ": 3,
    " <e> ": 4,
    " jeep ": 5,
    " cylinder engine ": 6
}

# Sort tokenizer keys by length (descending order) to match longer phrases first
sorted_keys = sorted(tokenizer.keys(), key=len, reverse=True)

def split_sentence(sentence, token_keys):
    pattern = "|".join(map(re.escape, token_keys))  # Create regex pattern with tokenizer keys
    return re.findall(pattern, sentence)  # Extract matched tokens in order

# Process each sentence
split_sentences = [split_sentence(sent, sorted_keys) for sent in sentences]

# Print results
for sent, split_tokens in zip(sentences, split_sentences):
    print(f"Original: {sent}")
    print(f"Split: {split_tokens}\n")
