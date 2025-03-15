import json

class Phrase_Tokenizer:
    def __init__(self, file_path):
        self.sentences = self._read_sentences(file_path)
        self.word_details = self._generate_word_details()
        self.phrase_to_token = self._compute_tokens()
    
    def _read_sentences(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["sentences"]
    
    def _generate_word_details(self):
        sentences = self.sentences
        word_details = {}
        for sentence in sentences:
            words = sentence.split()
            for i, word in enumerate(words):
                if word not in word_details:
                    word_details[word] = {"left": [], "right": []}
                
                if i > 0:
                    left_word = words[i - 1]
                    if left_word not in word_details[word]["left"]:
                        word_details[word]["left"].append(left_word)
                
                if i < len(words) - 1:
                    right_word = words[i + 1]
                    if right_word not in word_details[word]["right"]:
                        word_details[word]["right"].append(right_word)
        return word_details
    
    def _compute_tokens(self):
        def refine_token_index(phrase_to_token):
            token_index = 0
            for token_phrase in phrase_to_token:
                phrase_to_token[token_phrase] = token_index
                token_index += 1
            return phrase_to_token

        def create_left_phrase(word):
            left_phrase = " "
            left_words = self.word_details[word]['left']

            if len(left_words) == 0:
                return left_phrase
            
            elif len(left_words) == 1:
                left_word = left_words[0]
                if len(self.word_details[left_word]['right']) == 1 and self.word_details[left_word]['right'][0] == word:
                    left_phrase = create_left_phrase(left_word) + left_word + left_phrase
                    return left_phrase
                elif len(self.word_details[left_word]['right']) > 1:
                    return left_phrase

            elif len(left_words) > 1:
                return left_phrase
        
        def create_right_phrase(word):
            right_phrase = " "
            right_words = self.word_details[word]['right']

            if len(right_words) == 0:
                return right_phrase
            
            elif len(right_words) == 1:
                right_word = right_words[0]
                if len(self.word_details[right_word]['left']) == 1 and self.word_details[right_word]['left'][0] == word:
                    right_phrase = right_phrase + right_word + create_right_phrase(right_word)
                    return right_phrase
                elif len(self.word_details[right_word]['left']) > 1:
                    return right_phrase

            elif len(right_words) > 1:
                return right_phrase

        phrase_to_token = {}
        token_index = 0
        for word in self.word_details:
            phrase_to_token[create_left_phrase(word) + word + create_right_phrase(word)] = token_index
            token_index += 1
        
        return refine_token_index(phrase_to_token)
    
    def tokenize_datasest(self):
        tokenized_sentences = []
        for sentence in self.sentences:
            tokenized_sentence = []
            words = sentence.split()
            for i, word in enumerate(words):
                if word in self.phrase_to_token:
                    tokenized_sentence.append(self.phrase_to_token[word])
                else:
                    for j in range(i, 0, -1):
                        phrase = " ".join(words[i:j+1])


    def get_tokens(self):
        return json.dumps(self.phrase_to_token, indent=4)

# Example usage
tokenizer = Phrase_Tokenizer("d.json")
print(tokenizer.get_tokens())
print()
