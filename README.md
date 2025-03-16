# NoAI LG
 No AI Language Generalizer

# Aim
 Here we're aiming to create a language generator which generates meaningful sentences without using any neural networks

# What we've made
 currently we made a language translator. the program input a sentence and produce a similiar sentence as output(try by running infer.py)

# How it works?
 ## Tokenizer
  The tokenizer used is specifically designed. it tokenizes common phrases rather than just individual words
 ## Translation
  First a similiarity matrix(a matrix detailing how much each token is similiar to every other token in voabulary) is made by identifying patterns in training dataset(sentences). During inference(translation) this similiarity matrix is used to replace words(tokens).

# Future
 Question answering
 language generation
 summarization
