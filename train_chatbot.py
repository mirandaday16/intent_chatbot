import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
import json
import pickle
import tensorflow

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
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