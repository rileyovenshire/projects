This repository contains a deep learning model trained on the MNIST dataset for handwritten digit recognition.
The model is implemented using TensorFlow and Keras.

Model Architecture
The model architecture consists of a convolutional neural network that primarily focuses on accurate and efficient image classification. The model follows a general outline of:

1. Input Layer:
  Input shape: (28, 28, 1) for grayscale images.

2. Convolutional Layers:
  First Convolutional Layer:
    Number of filters: 32
    Kernel size: (5, 5)
    Activation function: ReLU
    Padding: 'valid'
    Input shape: (28, 28, 1)
  Second Convolutional Layer:
    Number of filters: 32
    Kernel size: (3, 3)
    Activation function: ReLU
    Padding: 'same'
    Input shape: (24, 24, 32) from the previous layer

3. Pooling Layer:
  MaxPooling2D
  Pool size: (2, 2)

4. Dropout Layer:
  Dropout rate: 0.2 (to reduce overfitting)

5. Flatten Layer:
  Flattens the 3D output to 1D (for feeding into fully connected layers).

6. Fully Connected Layers:
  First Dense Layer:
    Number of units: 519
    Activation function: ReLU
  Dropout Layer:
    Dropout rate: 0.5
  Output Layer:
    Number of units: 10 (for the 10 digits)
    Activation function: Softmax (since it's a multi-class classification problem).

Training
  The model was trained on the Kaggle MNIST dataset, which contains 60,000 training images and 10,000 test images of handwritten digits. The training process involved a first glance of the original dataset, then the model
  continued to generate future training data depending on accuracy or losses from the previous iteration.

Acknowledgments
  Special thanks to the following sources for providing inspiration, guidance, and resources for this project:

- Pulled the project from this list: https://github.com/practical-tutorials/project-based-learning
- Used Leandro Arruda's Medium tutorial here: https://medium.com/@lvarruda/how-to-get-top-2-position-on-kaggles-mnist-digit-recognizer-48185d80a2d4
- Kaggle MNIST Dataset of handwritten digits: https://www.kaggle.com/datasets/hojjatk/mnist-dataset
- Learned much more about machine learning and technicalities through fast.ai - https://www.fast.ai/
- Keras - https://keras.io/
- TensorFlow - https://www.tensorflow.org/
