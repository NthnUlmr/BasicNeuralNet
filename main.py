# <GPLv3_Header>
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# \copyright
#                    Copyright (c) 2024 Nathan Ulmer.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# <\GPLv3_Header>

##
# \mainpage Procedural Music Generator
#
# \copydoc main.py

##
# \file main.py
#
# \author Nathan Ulmer
#
# \date \showdate "%A %d-%m-%Y"
#

from BasicNeuralNetwork import *
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt



def load_data(path: str):

    # Data is assumed to be formatted as follows:
    # 0. All data is ascii
    # 1. Each image consists of consecutive rows starting with a number
    # 2. Only image data rows start with a number
    # 3. Data Labels for the image follow the corresponding block of image data and their lines start with a space
    # 4. Image data is either 0 or 1 for each pixel in a 32 by 32 grid

    with open(path,'r+') as inFile:
        lines = inFile.readlines()

    data = []
    labels = []
    numIdx = 0

    for line in lines:
        line = line.strip('\n')
        if line.isnumeric():
            # Row of Image Data
            if len(data) <= numIdx:
                data.append([])
            for dig in line:
                data[numIdx].append(int(dig))
        elif line[1:].isnumeric():
            # Row of Label Data
            digimon = [0.0]*10
            digimon[int(line[1:])] = 1.0
            labels.append(digimon)
            numIdx = numIdx + 1
        else:
            pass # ignore other lines

    data2 = []
    for line in data:
        tmpND = np.ndarray((1,len(line)-1), buffer=np.array(line),
           offset=np.int_().itemsize,
           dtype=int)
        data2.append(tmpND)

    assert(len(data) == len(labels))

    return (data2, labels)





def generate_data(num_samples: int, num_points: int, freq_range) -> npt.ArrayLike:
    X = np.zeros((num_samples, num_points))
    y = np.zeros(num_samples)

    for i in range(num_samples):
        freq = np.random.uniform(*freq_range)
        y[i] = freq
        t = np.linspace(0.0, 1.0, num_points)
        X[i] = np.sin(2.0 * np.pi * freq * t)

    return X, y



def main():

    training_data_path = 'optical_recognition_of_handwritten_digits/optdigits-orig.tra'
    (training_data, training_labels) = load_data(training_data_path)

    print(training_data[0][0])
    input_size = len(training_data[0][0])
    hidden_size = len(training_data[0][0])
    output_size = 10
    nn = BasicNeuralNetwork(input_size, hidden_size, output_size)
    learning_rate = 0.01

    # Train
    losses = []
    epochs = len(training_data)
    print_freq = 100
    for epoch in range(epochs):
        loss = nn.train(training_data[epoch], training_labels[epoch], learning_rate)
        losses.append(loss)
        if epoch % print_freq == 0:
            print(f"Epoch {epoch}, Loss: {loss:.4f}")

    # Plot the loss
    plt.figure()
    plt.plot(losses)
    plt.title("Training Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")


    test_data_path = 'optical_recognition_of_handwritten_digits/optdigits-orig.cv'
    (test_data, test_labels) = load_data(test_data_path)

    print(type(test_data))
    predictions = nn.forward(test_data)

    # Plot predictions vs true values
    plt.figure()
    plt.scatter(np.argmax(test_labels,axis=1), np.argmax(predictions,axis=2))
    plt.xlabel("Labels")
    plt.ylabel("Prediction")
    plt.title("True vs Predicted Numbers")

    plt.figure()
    test_errs = []
    test_ids = []
    for ii in range(len(test_labels)):
        tmp = np.argmax(test_labels[ii]) - (np.argmax(predictions[ii]))
        test_errs.append(tmp)
        test_ids.append(ii)

    plt.scatter(test_ids,test_errs)
    plt.xlabel("Labels")
    plt.ylabel("Prediction")
    plt.title("True vs Predicted Numbers")


    plt.figure()
    plt.hist(test_errs)
    plt.title("Histogram of Testing Error")
    plt.xlabel("Error in Prediction")
    plt.ylabel("Count")
    plt.show()



if __name__ == '__main__':
    main()

# <GPLv3_Footer>
################################################################################
#                      Copyright (c) 2024 Nathan Ulmer.
################################################################################
# <\GPLv3_Footer>