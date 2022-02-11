import random
import numpy as np
from brain import Brain
from car import Car, SENSOR_LENGTH

def mutate(car: Car):
    if random.random() <= 0.1: #10% chance for mutation for each brain
        i = random.randint(0, car.brain.hidden_len-1)
        print(car.brain.hidden_len, car.brain.inputs_len)
        j = random.randint(0, car.brain.inputs_len-1)
        car.brain.weights_hidden[i][j] *= random.uniform(-100., 100.)
    return car

def mate(parent_cars): #should return a brain object

    if len(parent_cars) == 0:
        brain = Brain(SENSOR_LENGTH, 16, 4)
        return brain

    if len(parent_cars) < 2:
        return parent_cars[0].brain

    #Calc parent_cars fitness and chose two parents from the pool.
    parent_cars_fitness = [car.calc_fitness() for car in parent_cars]
    chosen_parents = random.choices(parent_cars, parent_cars_fitness, k=2)
    chosen_parents_fitness = [car.calc_fitness() for car in chosen_parents]

    #Jeg prøvede at lave ndarray??
    child_hidden_weights = np.ndarray((parent_cars[0].brain.hidden_len, parent_cars[0].brain.inputs_len))
    child_output_weights = np.ndarray((parent_cars[0].brain.outputs_len, parent_cars[0].brain.hidden_len))

    #Create a brain, and change its weights later
    child_brain = Brain(len(parent_cars[0].sensors)+1, 16, 4)

    #Iterate through range of the weights, and choose a parent each time, whose weight in that specific index should replace the child brain index
    for i in range(len(parent_cars[0].brain.weights_hidden)):
        child_gene = random.choices(chosen_parents, chosen_parents_fitness, k=1)
        child_hidden_weights[i] = child_gene[0].brain.weights_hidden[i]

    for i in range(len(parent_cars[0].brain.weights_output)):
        child_gene = random.choices(chosen_parents, chosen_parents_fitness, k=1)
        child_output_weights[i] = child_gene[0].brain.weights_output[i]
    
    child_brain.weights_hidden = child_hidden_weights
    child_brain.weights_output = child_output_weights

    return child_brain
    
    
    