import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np

import spacy
nlp = spacy.load('en_core_web_sm')

from keras.models import load_model
import json
import random

from weather import get_weather
from time_zones import get_time

lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
intents = json.loads(open('python-project-chatbot-codes/intents.json').read())
words = pickle.load(open('python-project-chatbot-codes/words.pkl', 'rb'))
classes = pickle.load(open('python-project-chatbot-codes/classes.pkl', 'rb'))


# Clean up a sentence (tokenize and lemmatize) and return an array of words
# Parameter: a sentence in the form of a string
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# Create a bag of words from a given sentence (string) and list of words
# Implements clean_up_sentence() function
def bag_of_words(sentence, words, show_details = True):
    sentence_words = clean_up_sentence(sentence)
    # Create vocabulary matrix of N words (will be returned as bag or words)
    bag_of_words = [0] * len(words)
    for word in sentence_words:
        for i,w in enumerate(words):
            if w == word:
                # Assign 1 if current word is in the vocabulary position, else assign 0
                bag_of_words[i] = 1
                if show_details:
                    print("Found in bag: ", w)
    return(np.array(bag_of_words))


# Predict the class of a given sentence (string) using a given model
# Implements bag_of_words() function
def predict_class(sentence, model):
    # Filter out predictions below a threshold (0.25)
    bow = bag_of_words(sentence, words, show_details = False)
    model_result = model.predict(np.array([bow]))[0]
    error_threshold = 0.25
    results = [[i, result] for i, result in enumerate(model_result) if result > error_threshold]
    # Sort by probability
    results.sort(key = lambda x: x[1], reverse = True)
    return_list = []
    for result in results:
        return_list.append({'intent': classes[result[0]], "probability": str(result[1])})
    return return_list


# Get a random response for the user based on the predicted class
# Parameters: original input sentence, a list of intent tags and a json file of intents with tags and responses
def get_response(sentence, intents, intents_json):
    if 'weather' in sentence:
        response = get_response_weather(sentence)
    elif 'time' in sentence:
        response = get_response_time(sentence)
    else:
        tag = intents[0]['intent']
        intents_list = intents_json['intents']
        for intent in intents_list:
            if intent['tag'] == tag:
                response = random.choice(intent['responses'])
                break
    return response


# Get a response to a weather-related query
# Parameters: a given sentence (string) from the user
def get_response_weather(sentence):
    labelled_sentence = nlp(sentence)
    location_name = ""
    for word in labelled_sentence.ents:
        # check for geographic places
        if word.label_ == 'GPE':
            location_name = word.text
    if len(location_name) < 1:
        response = "What city do you need the weather forecast for?"
        # TODO: Figure out how to connect following user response
    else:
        response = get_weather(location_name)
    return response


# Get a response to a time-related query
# Parameters: a given sentence (string) from the user
def get_response_time(sentence):
    labelled_sentence = nlp(sentence)
    location_name = ""
    for word in labelled_sentence.ents:
        # check for geographic places
        if word.label_ == 'GPE':
            location_name = word.text
    if len(location_name) < 1:
        response = "What city do you need the time for?"
        # TODO: Figure out how to connect following user response
    else:
        response = get_time(location_name)
    return response


# Predict the class of input and choose a response to return to the user
# Parameter: text (string) provided by the user
# Implements predict_class() and get_response() functions
def chatbot_response(text):
    ints = predict_class(text, model)
    response = get_response(text, ints, intents)
    return response

