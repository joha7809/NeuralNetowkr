# Simple pygame program
import random

import GeneticAlgorithm as GA

# Import and initialize the pygame library
import pygame
pygame.init()
import car
import os
fps = 60
NUM_CARS = 50



# Set up the drawing window
def load():
    global screen, track, biler, next_gen
    next_gen = []
    screen = pygame.display.set_mode([1920, 1080], flags=pygame.SCALED, vsync=1)
    track = pygame.image.load(os.path.join('data', 'track2.png')).convert_alpha()
    track = pygame.transform.scale(track, (1920, 1080))
    biler = [car.Car(screen, size=5, startx=65, starty=800, heading=20, track_img = track) for i in range(NUM_CARS)]

def drive_cars(cars):
    #Check if car is out of bounds
    #Get input from sensor for car, and pass it on to the neural network
    #Get output from neural network and perfom the action
    #Update car position
    if not cars:
        print("ALLE ER DØDE")
        cars = make_next_gen()
    for bil in cars:
        if bil.is_dead():
            if bil.calc_fitness() > 0:
                next_gen.append(bil)
            cars.remove(bil)
            continue
        bil.drive()
        bil.draw()
    return cars


def make_next_gen():
    #Check if all cars are dead then perform the methods from genetic algorithm.py
    biler = [car.Car(screen, size=5, startx=65, starty=800, heading=20, track_img = track) for i in range(NUM_CARS)]
    for bil in biler:
        if len(next_gen) > 0:
            bil.brain = GA.mate(next_gen)
        for i in range(10):
            GA.mutate(bil)
    return biler
    

# Run until the user asks to quit
load()
running = True
clock = pygame.time.Clock()
while running:
    # Add fps to prevent lags
    clock.tick(fps)     
    print(len(biler))
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            load()

    # Fill the background with white
    screen.fill((0, 0, 0))
    #Draw the track image
    screen.blit(track, (0,0))

    # Draw a solid circle in the center of the car   
    biler = drive_cars(cars=biler)
    
    # Flip the display  (Update screen??)
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

