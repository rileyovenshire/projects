# Author: Riley Ovenshire --- following Leandro Arruda's tutorial, see readme
# GitHub username: rileyovenshire
# Date: 9/18/2023
# Description: Model configuration file. Reads a 28x28 px image (784px) with a specific brightness value - higher numbers are darker. Ranked on a standard RGB scale (0, 255).

from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.optimizers import Adam, RMSprop
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau


def config_model():
    """
    Configuration for the model, completed with general definitions from KERAS library.

    Consulted:
    - https://medium.com/@lvarruda/how-to-get-top-2-position-on-kaggles-mnist-digit-recognizer-48185d80a2d4
    - https://keras.io/guides/sequential_model/
    - Convolution layer guide: https://keras.io/api/layers/convolution_layers/convolution2d/
    - convolution: function expressing how the shape of one function is modified by another. A blending of functions.
    """

    # -------------------------------------Initialize the Model------------------------------------------

    model = Sequential()

    # first convolutional layer with 32 filters, each 5x5 in size
    # activation function is Rectified Linear Unit (relu)
    # input shape is 28x28 pixels with 1 channel (grayscale)
    model.add(Conv2D(filters=32,
                     kernel_size=(5, 5),
                     padding='valid',  # no padding
                     activation='relu',
                     input_shape=(28, 28, 1)))

    # second convolutional layer with 32 filters, each 3x3 in size
    # padding is set to 'same' to add zeros around the input to maintain output size
    model.add(Conv2D(filters=32,
                     kernel_size=(3, 3),
                     padding='same',  # padding with zeros to evenly distributed to left/right or up/down of input
                     activation='relu'))

    # adding in a max pooling layer of size 2x2: it reduces the number of parameters to learn and the amount of computation performed in the network
    model.add(MaxPool2D(pool_size=(2, 2)))

    # dropout layer at 20%: prevents overfitting (the learning of training data, instead of new data)
    model.add(Dropout(0.2))

    # flatten output to connect layers
    model.add(Flatten())

    # fully connected layer, 519 units and relu activation
    model.add(Dense(519, activation='relu'))

    # another dropout at 50% rate
    model.add(Dropout(0.5))

    # add final layer with 10 units - one for each digit to be recognized/learned
    model.add(Dense(10, activation="softmax"))

    # -------------------------------------Prepare for Training------------------------------------------

    # loss function: quantifies the error between the predicted output and the actual target values
    model.compile(loss='categorical_crossentropy',  # for multi-class problems
                  optimizer=Adam(lr=1e-3),  # 0.001 learning rate, Adam optimizer
                  metrics=["accuracy"])

    # -------------------------------------Learning Rate Scheduler------------------------------------------

    lrs = ReduceLROnPlateau(monitor='val_acc',
                            patience=1,
                            # number of epochs with no improvement, will reduce if validation accuracy doesn't improve for one epoch
                            verbose=2,  # print message when learning rate changes
                            factor=0.5,
                            min_lr=0.0000001)  # abs minimum learning rate

    # -------------------------------------Data Generator------------------------------------------
    data = ImageDataGenerator(
        featurewise_center=False,
        samplewise_center=False,
        featurewise_std_normalization=False,
        samplewise_std_normalization=False,
        zca_whitening=False,
        rotation_range=10,
        zoom_range=0.1,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=False,
        vertical_flip=False)

    return model, lrs, data
