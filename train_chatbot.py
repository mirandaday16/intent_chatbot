import nltk
from nltk.stem import WordNetLemmatizer
# nltk.download('wordnet')
import json
import pickle

import numpy as np
import random

lemmatizer = WordNetLemmatizer()

words = []
classes = []
documents = []
ignored_words = ['?', '!']
data_file = open('python-project-chatbot-codes/intents.json').read()
intents = json.loads(data_file)

# Tokenize sentences in intents file
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word
        word_tokens = nltk.word_tokenize(pattern)
        words.extend(word_tokens)
        # add to documents list (corpus)
        documents.append((word_tokens, intent['tag']))
        # add tag to class list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Cleaning data: lowercase, removing duplicates
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignored_words]
words = sorted(list(set(words)))
# Sort classes
classes = sorted(list(set(classes)))

# Save words and classes to pickle files
pickle.dump(words, open("python-project-chatbot-codes/words.pkl", 'wb'))
pickle.dump(classes, open('python-project-chatbot-codes/classes.pkl', 'wb'))

# Create training data
training = []
# Empty list for output
output_empty = [0] * len(classes)
# "Bag of Words" for each sentence
for document in documents:
    bag_of_words = []
    # list of tokenized words in the pattern
    pattern_words = document[0]
    # lemmatize pattern words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # Append 1 to bag of words if word match is found in current pattern, otherwise 0
    for word in words:
        if word in pattern_words:
            bag_of_words.append(1)
        else:
            bag_of_words.append(0)
    # Output is 0 for each tag and 1 for current tag
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag_of_words, output_row])

# Shuffle features to create numpy array
random.shuffle(training)
training = np.array(training)

# Create training and test sets
train_patterns = list(training[:,0])
train_intents = list(training[:,1])

print("Training data created.")