import json

class Phrase_Tokenizer:
    def __init__(self, file_path):
        self.sentences = self.read_sentences(file_path)
        self.word_details = self._generate_word_details()
        self.token_to_phrase = {}
        self.phrase_to_token = self._compute_tokens()

    
    def read_sentences(self, file_path):
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
        def refine_tokens(phrase_to_token):
            # remove unwanted space
            refined_phrase_to_token = {}
            for token_phrase in phrase_to_token:
                token_phrase_refined = token_phrase.strip()
                refined_phrase_to_token[token_phrase_refined] = phrase_to_token[token_phrase]
            
            # refine token index
            token_index = 0
            for token_phrase in refined_phrase_to_token:
                refined_phrase_to_token[token_phrase] = token_index
                token_index += 1
            
            return refined_phrase_to_token

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
            phrase = create_left_phrase(word) + word + create_right_phrase(word)
            phrase_to_token[phrase] = token_index
            #token_to_phrase[token_index] = phrase
            token_index += 1
        
        self.phrase_to_token = refine_tokens(phrase_to_token)
        self.token_to_phrase = {}

        for phrase in self.phrase_to_token:
            self.token_to_phrase[self.phrase_to_token[phrase]] = phrase
        #print(self.token_to_phrase)
        
        return self.phrase_to_token
    
    def convert_token_to_phrase(self, token):
        #print(self.token_to_phrase)
        if isinstance(token, int):
            return self.token_to_phrase[token]
        else:
            return token
    

    def tokenize_sentences(self, sentences):
        token_map = self.phrase_to_token
        tokenized_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            i = 0
            tokenized = []
            
            while i < len(words):
                matched = False
                
                # Try matching longest possible n-grams first
                for n in [6, 5, 4, 3, 2, 1]:  # 3-word, then 2-word, then 1-word
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
                    #tokenized.append(-1)
                    i += 1
            
            tokenized_sentences.append(tokenized)
        
        return tokenized_sentences


    def get_tokens(self):
        return json.dumps(self.phrase_to_token, indent=4)

# Example usage
#print(tokenizer.get_tokens())
#print(tokenizer.tokenize_sentences(tokenizer.read_sentences("d.json")))
