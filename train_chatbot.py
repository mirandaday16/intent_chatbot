import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random

lemmatizer = WordNetLemmatizer

words = []
classes = []
documents = []
ignore_words = ['?', '!']
data_file = open('python-project-chatbot-codes/intents.json').read()
intents = json.loads(data_file)