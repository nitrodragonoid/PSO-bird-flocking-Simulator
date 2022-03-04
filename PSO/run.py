import time
from random import random
import pygame
import random

GRAY = (155, 155, 155)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((700, 700))
game_over = False

#initalitizing the birds
initial = [300,300]
inertia = [-3,-4]

birds = []
velocities = []
Pbests = []
bestPos = []

food = [500,500] #food position

# Adjust these:
numberOfBirds = 30
alpha = 1
beta = 2
gamma = 0.8

def getDist(pos, food):
    # return [abs(food[0]-pos[0]), abs(food[1]-pos[1])]
    return ((food[0]-pos[0])**2 + (food[1]-pos[1])**2)**(1/2)

def Gbest(pbests,bestPos):
    return bestPos[pbests.index(min(pbests))]

for i in range(numberOfBirds):
    # birds.append(initial)
    birds.append([random.randint(0, 700),random.randint(0, 700)])
    velocities.append([random.randint(0, 11),random.randint(0, 11)])
    bestPos.append(initial)
    Pbests.append(getDist(initial,food))

#Simulation runner

while game_over == False:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    # x = input()
    #drawing the food source
    pygame.draw.rect(screen, YELLOW, [food[0], food[1], 20, 20])
       
    #PSO   
    for bird in range(len(birds)):
        #Update velocities 
        velocities[bird][0] = gamma*velocities[bird][0] + beta*(Gbest(Pbests,bestPos)[0]-birds[bird][0]) + alpha*(bestPos[bird][0]-birds[bird][0]) #+ inertia[0]#- 2*birds[bird][0]
        velocities[bird][1] = gamma*velocities[bird][1] + beta*(Gbest(Pbests,bestPos)[1]-birds[bird][1]) + alpha*(bestPos[bird][1]-birds[bird][1]) #+ inertia[1]#- 2*birds[bird][1] 
        
        #Update positions
        newpos = [velocities[bird][0] + birds[bird][0], velocities[bird][1] + birds[bird][1]]
        birds[bird] = newpos    

        #Find new distance and pdate the best fitness
        dist = getDist(newpos, food)
        if dist < Pbests[bird]:
            Pbests[bird] = dist
            bestPos[bird] = newpos
            
    #drawing all our birds
    for bird in birds:
        pygame.draw.rect(screen, GRAY, [bird[0], bird[1], 10, 10])
    
    time.sleep(0.1)
    pygame.display.flip()
