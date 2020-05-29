import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

from train_chatbot import train_intents, train_patterns

# Create 3-layered model.
# Layer One: 128 neurons
# Layer Two: 64 neurons
# Layer Three: number of neurons equal to # of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape = (len(train_patterns[0]),),  activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_intents[0]), activation = 'softmax'))

# Compile model.
# Stochastic gradient descent with Nesterov accelerated gradient
sgd = SGD(lr = 0.01, decay = 1e-6, momentum = 0.9, nesterov = True)
model.compile(loss = 'categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])

# Fit model
hist = model.fit(np.array(train_patterns), np.array(train_intents), epochs = 200, batch_size = 5, verbose = 1)
model.save('chatbot_model.h5', hist)

print('Model created.')
