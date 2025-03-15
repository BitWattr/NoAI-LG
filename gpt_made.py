import numpy as np

# Given similarity dictionary
similarity_dict = {
    "0": {"0": 20},
    "1": {"1": 6, "5": 6},
    "2": {"2": 16},
    "3": {"3": 6, "6": 6},
    "4": {"4": 20},
    "5": {"1": 6, "5": 6},
    "6": {"3": 6, "6": 6}
}

# Define matrix size (assuming keys are 0 to 6)
size = max(map(int, similarity_dict.keys())) + 1
matrix = np.zeros((size, size), dtype=int)

# Populate matrix from dictionary
for i, values in similarity_dict.items():
    for j, similarity in values.items():
        matrix[int(i)][int(j)] = similarity

# Display matrix
print(matrix)
