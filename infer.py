from similiarity_decoder import Similiarity_Matrix_Generator
import random

def replace_tokens(tokenized_input, similiarity_matrix_generator):
    replaced_tokens = []
    similiarity_matrix = similiarity_matrix_generator.similiarity_matrix
    for token in tokenized_input:
        if isinstance(token, int):
            #print(tokenizer.convert_token_to_phrase(token))
            similiar_tokens = list(similiarity_matrix[token].keys())
            replaced_tokens.append(random.choice(similiar_tokens))
        else:
            replaced_tokens.append(token)

    return replaced_tokens


similiarity_matrix_generator = Similiarity_Matrix_Generator()
#print(json.dumps(similiarity_matrix_generator.generate_token_details(), indent=4))
similiarity_matrix_generator.generate_token_details()
similiarity_matrix_generator.compute_matrix()
#print(similiarity_matrix_generator.similiarity_matrix)

input = "<s> car have 4 brakes <e>"

tokenizer = similiarity_matrix_generator.tokenizer
tokenized_input = tokenizer.tokenize_sentences([input])[0]
print(tokenized_input)
replaced_tokens = replace_tokens(tokenized_input, similiarity_matrix_generator)
output_phrases = []
for token in replaced_tokens:
    output_phrases.append(tokenizer.convert_token_to_phrase(token))

print(" ".join(output_phrases))


