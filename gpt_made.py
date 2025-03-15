def tokenize_sentences(sentences, token_map):
    tokenized_sentences = []
    
    for sentence in sentences:
        words = sentence.split()
        i = 0
        tokenized = []
        
        while i < len(words):
            matched = False
            
            # Try matching longest possible n-grams first
            for n in [3, 2, 1]:  # 3-word, then 2-word, then 1-word
                if i + n <= len(words):
                    phrase = " ".join(words[i:i + n])
                    if phrase in token_map:
                        tokenized.append(token_map[phrase])
                        i += n
                        matched = True
                        break
            
            if not matched:
                # Just append the word if no match (should not happen if mapping is correct)
                tokenized.append(words[i])
                i += 1
        
        tokenized_sentences.append(tokenized)
    
    return tokenized_sentences

# Sample Data
sentences = [
    "<s> car have 4 wheels <e>",
    "<s> jeep have 4 wheels <e>",
    "<s> car have 4 cylinder engine <e>",
    "<s> jeep have 4 cylinder engine <e>"
]

token_map = {
    "<s>": 0,
    "car": 1,
    "have 4": 2,
    "wheels": 3,
    "<e>": 4,
    "jeep": 5,
    "cylinder engine": 6
}

# Tokenize the sentences
tokenized_output = tokenize_sentences(sentences, token_map)

# Print result
for sent in tokenized_output:
    print(sent)
