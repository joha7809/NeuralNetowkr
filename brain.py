import numpy as np
from typing import List


class Brain:
    def __init__(self, inputs_len: int, hidden_layer_len: int, outputs_len: int):
        #Creates a list of lists, that containst output_len og hidden_layer_len number of lists with each list containing inputs_len items.
        self.inputs_len = inputs_len
        self.hidden_len = hidden_layer_len
        self.outputs_len = outputs_len
        

        self.weights_hidden = np.random.uniform(-1, 1, (hidden_layer_len, inputs_len)) 
        self.weights_output = np.random.uniform(-1, 1, (outputs_len, hidden_layer_len))
    def input_processing(self, inputs:List[float], velocity):
        """
        Inputs are the sensor values / pixel values

        The function then returns values ready to be fed to the neural network
        """

        for idx in range(len(inputs)):
            inputs[idx] = inputs[idx][:3]

        inputs.append([velocity]*3) #Add the velocity of the car to the nueral network

        # Turn inputs into numpy array
        inputs =  np.array(inputs)
        inputs = inputs.astype(np.float32)

        # Normalize pixel values between 0 and 1, 1 for white and 0 for black
        inputs /= 255.0

        # Turn the inputs into single value floats like:
        #etc.
        inputs = inputs.sum(1)
        inputs /= 3.0
        

        return inputs

    def neuralnet(self, inputs: np.array):
        """
        This function makes all the necessary calculations to the neural network and returns whether the car should drive, break, turn left or turn right
        """
        hidden_neurons = []
        for i in range(self.weights_hidden.shape[0]):
            l_ = 0
            for j in range(len(inputs)):
                l_ += inputs[j] * self.weights_hidden[i][j]
            hidden_neurons.append(l_)
        hidden_neurons = np.array(hidden_neurons)
        hidden_neurons = self.sigmoid(hidden_neurons)
        
        output_neurons = []
        for i in range(self.weights_output.shape[0]):
            l_ = 0
            for j in range(hidden_neurons.shape[0]):
                l_ += hidden_neurons[j] * self.weights_output[i][j]
            output_neurons.append(l_)
        output_neurons = np.array(output_neurons)
        output_neurons = self.sigmoid(output_neurons)

        return output_neurons.round().tolist() # Cast numpy array to python array

    def sigmoid(self, x):
        # 1 / 1 + e^-x
        return 1 / (1 + np.exp(-x))
