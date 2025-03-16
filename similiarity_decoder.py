from neibour_tokenizer import Phrase_Tokenizer
import json
import numpy as np

import csv

class Similiarity_Matrix_Generator:
    def __init__(self):
        self.tokenizer = Phrase_Tokenizer("d.json")
        self.tokenized_dataset = self.tokenizer.tokenize_sentences(self.tokenizer.read_sentences('d.json'))
        self.token_details = None
        self.normalize = True
    
    def generate_token_details(self):
        token_details = {}
        for tokenized_sentence in self.tokenized_dataset:
            for token in tokenized_sentence:
                if token not in token_details:
                    token_details[token] = {'left': [], 'right': []}
                token_details[token]['left'].append(tokenized_sentence[:tokenized_sentence.index(token)]) 
                token_details[token]['right'].append(tokenized_sentence[tokenized_sentence.index(token) + 1:])
        self.token_details = token_details
        #print(token_details)
        return token_details

    def compute_matrix(self):
        similiarity_matrix = {}

        # left
        for token in self.token_details:
            left_tokens = self.token_details[token]['left']

            for compare_token in self.token_details:
                for each_left_of_compare in self.token_details[compare_token]['left']:
                    for each_left_of_token in left_tokens:
                        if each_left_of_compare == each_left_of_token:
                            if not token in similiarity_matrix:
                                similiarity_matrix[token] = {}
                            if not compare_token in similiarity_matrix[token]:
                                similiarity_matrix[token][compare_token] = 0
                            similiarity_matrix[token][compare_token] += 1
        
        # right
        for token in similiarity_matrix:
            right_tokens = self.token_details[token]['right']

            for compare_token in self.token_details:
                for each_right_of_compare in self.token_details[compare_token]['right']:
                    for each_right_of_token in right_tokens:
                        if each_right_of_compare == each_right_of_token and (len(each_right_of_compare) > 0 and len(each_right_of_token) > 0):
                            if not token in similiarity_matrix:
                                similiarity_matrix[token] = {}
                            if not compare_token in similiarity_matrix[token]:
                                similiarity_matrix[token][compare_token] = 0
                            similiarity_matrix[token][compare_token] += 1

        # Normalize
        if self.normalize:
            for token in similiarity_matrix:
                factor = 1
                for each in similiarity_matrix[token]:
                    if factor < similiarity_matrix[token][each]:
                        factor = similiarity_matrix[token][each]
            
                for compare_token in similiarity_matrix[token]:
                    #pass
                    similiarity_matrix[token][compare_token] = similiarity_matrix[token][compare_token] / factor


        self.similiarity_matrix = similiarity_matrix
        return similiarity_matrix

    def print_matrix(self):
        # Define matrix size (assuming keys are 0 to 6)
        size = max(map(int, self.similiarity_matrix.keys())) + 1
        matrix = np.zeros((size, size), dtype=int)

        # Populate matrix from dictionary
        for i, values in self.similiarity_matrix.items():
            for j, similarity in values.items():
                matrix[int(i)][int(j)] = similarity

        # Display matrix
        print(matrix)

    def print_phrase_matrix(self):
        tokens = list(self.similiarity_matrix.keys())
        phrases = {token: self.tokenizer.convert_token_to_phrase(token) for token in tokens}
        
        # Print header row
        print("\t" + "\t".join(phrases[token] for token in tokens))
        
        # Print matrix rows
        for i in tokens:
            row = [f"{round(self.similiarity_matrix[i].get(j, 0), 2):.2f}" for j in tokens]
            print(f"{phrases[i]}\t" + "\t".join(row))


    def print_similiar_tokens(self):
        for token in self.similiarity_matrix:
            print(f"{self.tokenizer.convert_token_to_phrase(token)} is similiar to: ", end="")
            for compare_token in self.similiarity_matrix[token]:
                print(f"{self.tokenizer.convert_token_to_phrase(compare_token)}({self.similiarity_matrix[token][compare_token]}), ", end="")
            print()
        
    def export_matrix_to_csv(self, filename="similarity_matrix.csv"):
        tokens = list(self.similiarity_matrix.keys())
        phrases = {token: self.tokenizer.convert_token_to_phrase(token) for token in tokens}

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write header row
            writer.writerow([""] + [phrases[token] for token in tokens])

            # Write matrix rows
            for i in tokens:
                row = [phrases[i]] + [round(self.similiarity_matrix[i].get(j, 0), 2) for j in tokens]
                writer.writerow(row)

        print(f"Matrix exported to {filename}")

if __name__ == "__main__":
    similiarity_matrix_generator = Similiarity_Matrix_Generator()
    #print(json.dumps(similiarity_matrix_generator.generate_token_details(), indent=4))
    similiarity_matrix_generator.generate_token_details()
    similiarity_matrix_generator.compute_matrix()
    print(similiarity_matrix_generator.tokenizer.get_tokens())
    #print()
    print(json.dumps(similiarity_matrix_generator.similiarity_matrix, indent=4))

    similiarity_matrix_generator.export_matrix_to_csv()

