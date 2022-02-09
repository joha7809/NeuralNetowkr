# Simple pygame program
import random

# Import and initialize the pygame library
import pygame
pygame.init()
import car
import os
fps = 60
NUM_CARS = 100

# Set up the drawing window
screen = pygame.display.set_mode([1920, 1080], flags=pygame.SCALED, vsync=1)
track = pygame.image.load(os.path.join('data', 'track2.png')).convert_alpha()
track = pygame.transform.scale(track, (1920, 1080))

biler = [car.Car(screen, size=5, startx=65, starty=800, heading=0, track_img = track) for i in range(NUM_CARS)]

def drive_cars(cars):
    #Check if car is out of bounds
    #Get input from sensor for car, and pass it on to the neural network
    #Get output from neural network and perfom the action
    #Update car position
    for bil in cars:
        if bil.is_dead():
            cars.remove(bil)
            continue
        bil.drive()
        bil.draw()
    return cars

# Run until the user asks to quit
running = True
clock = pygame.time.Clock()
while running:
    
    # Add fps to prevent lags
    clock.tick(fps)     
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((0, 0, 0))
    #Draw the track image
    screen.blit(track, (0,0))

    # Draw a solid blue circle in the center    
    biler = drive_cars(biler)
    
    # Flip the display  (Update screen??)
    pygame.display.flip()

# Done! Time bto quit.
pygame.quit()

