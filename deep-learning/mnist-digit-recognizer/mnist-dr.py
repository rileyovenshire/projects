# Author: Riley Ovenshire
# GitHub username: rileyovenshire
# Date: 9/18/23
# Description: Main program for the digit recognizer, trained on the Kaggle dataset. Uses the model that has been configured in model.py.

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import model as md
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import accuracy_score, confusion_matrix
from keras.utils import to_categorical

import time

start_time = time.time()

# -------------------------------------Load and Prepare Training Data------------------------------------------
data = pd.read_csv('./input/train.csv')
print(data.shape)

y = data['label']
X = data.drop('label', axis=1)

print(y.value_counts().to_dict())
y = to_categorical(y, num_classes=10)

del data  # free up memory

# set to grayscale values
X = X / 255.0
X = X.values.reshape(-1, 28, 28, 1)

# -------------------------------------Shuffle Split Train and Test from OG Dataset------------------------------------------
seed = 2  # reproduce at this value

# generate training and validation indices:
#   - training set (90%) / validation set (10%)
train_index, valid_index = next(ShuffleSplit(n_splits=1,
                                             train_size=0.9,
                                             test_size=None,
                                             random_state=seed).split(
    X))  # ensures the split will be the same each time

# training
x_train = X[train_index]
Y_train = y[train_index]

# validation
x_test = X[valid_index]
Y_test = y[valid_index]

# params
training_epochs = 3
batch_size = 64
validation_steps = 10000

# -------------------------------------Init Model, Learning Rate Scheduler and Data------------------------------------------
model, lrs, data = md.config_model()

# -------------------------------------Begin Training------------------------------------------

# flow from ImageDataGenerator: https://keras.io/api/data_loading/image/
#   generate batches of data on the fly
training_generator = data.flow(x_train, Y_train, batch_size=batch_size)
test_generator = data.flow(x_test, Y_test, batch_size=batch_size)

# train the model using the generator data
history = model.fit(training_generator,
                    steps_per_epoch=x_train.shape[0] // batch_size,
                    epochs=training_epochs,
                    validation_data=test_generator,
                    validation_steps=validation_steps // batch_size,
                    callbacks=[lrs])

# -------------------------------------Display Results------------------------------------------
score = model.evaluate(x_test, Y_test)
print('Test accuracy: ', score[1])

# save model for future API (pulled from medium.com source - see readme)
model.save('mnist-testing.keras')
print('Saved!')

# check log for accuracy, plot the data
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('MNIST Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='lower right')
plt.show()

# check log for losses, plot data
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('MNIST Model Losses/Inaccuracies')
plt.ylabel('Losses')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

# -------------------------------------Use Trained Model to Make Predictions on Test Data------------------------------------------
test = pd.read_csv('./input/test.csv')
print(test.shape)
test = test / 255  # RGB vals
test = test.values.reshape(-1, 28, 28, 1)  # 28x28 px

# model.predict() method returns a probability distribution for each digit
# np.argmax() is used to find the class with the highest probability for each sample
prediction = np.argmax(model.predict(x_test), axis=1)

print('Base model scores: ')
valid_loss, valid_acc = model.evaluate(x_test, Y_test, verbose=0)  # evaluate performance on validation data
valid_predict = np.argmax(model.predict(test), axis=1)

target = np.argmax(Y_test, axis=1)

# calculate and print confusion matrix
#   - https://www.sciencedirect.com/topics/engineering/confusion-matrix#:~:text=A%20confusion%20matrix%20represents%20the,by%20model%20as%20other%20class.
confusion_matrix = confusion_matrix(target, valid_predict)
print(confusion_matrix)

# -------------------------------------File to CSV for Submission (Kaggle)------------------------------------------
submit = pd.DataFrame(pd.Series(range(1, prediction.shape[0] + 1), name='ImageID'))
submit['Label'] = prediction
filename = 'keras-nums-{0}.csv'.format(str(int(score[1] * 10000)))
submit.to_csv(filename, index=False)

total_time = time.time() - start_time
print('Elapsed time: {0}'.format(time.strftime("%H:%M:%S", time.gmtime(total_time))))
