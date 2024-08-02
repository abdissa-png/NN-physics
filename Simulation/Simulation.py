from Ball import Ball
from Table import Table
from Utils import circumcenter
import pygame
import pymunk
import random
from numpy.random import uniform
# Initialize Pygame and set up the display
WIDTH = 800
HEIGHT = 400
BOTTOM_LEFT = (WIDTH//16, HEIGHT//8)
TOP_RIGHT = ((WIDTH*15)//16, (HEIGHT*7)//8)
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

# Set up the physics space
space = pymunk.Space()
space.gravity = (0, 0)

NUM_BALLS = 3
BALLS = []
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 165, 0),
    (128, 0, 128),
    (255, 192, 203),
    (128, 128, 0),
    (0, 128, 128),
    (128, 128, 128),
    (192, 192, 192),
]
# Many Balls simulation
# RADIUS_RANGE = [13,18]
# MASS_RANGE = [0.8,1.5]
# ELASTICITY_RANGE = [0.6,0.9]
# FRICTION_RANGE = [0.4,0.7]
# BALL2_POS = ((WIDTH*4)//10, HEIGHT//2)
# INITIAL_VELOCITY = (1e3, 0)
# INTIALIZTION = "SAFE"
# start =1
# lane = 1
# while start<=NUM_BALLS:
#     if start!=1:
#         if lane%2==0:
#             ball_range = [i for i in range(-lane//2,lane//2+1) if i!=0]
#         else:
#             ball_range = [i for i in range(-(lane//2),lane//2+1)]
#         # print(ball_range,lane)
#         for i in ball_range:
#             if start>NUM_BALLS:
#                 break  
#             position = (BALL2_POS[0]+lane*2*RADIUS_RANGE[1],BALL2_POS[1]+i*RADIUS_RANGE[1])
#             if INTIALIZTION!="SAFE":
#                 ball = Ball(space, COLORS[start%len(COLORS)], start,uniform(*RADIUS_RANGE) , uniform(*MASS_RANGE) ,position ,uniform(*ELASTICITY_RANGE),uniform(*FRICTION_RANGE), (0, 0))
#             else:
#                 ball = Ball(space,COLORS[start%len(COLORS)], start,15,2.0,position,1.0,0.0,(0,0))
#             BALLS.append(ball)
#             start+=1
#         lane+=1
#     else:
#         if INTIALIZTION!="SAFE":
#             ball = Ball(space, COLORS[start%len(COLORS)], start,uniform(*RADIUS_RANGE) , uniform(*MASS_RANGE) , (WIDTH//8, HEIGHT//2),uniform(*ELASTICITY_RANGE),uniform(*FRICTION_RANGE), (0, 0))
#         else:
#             ball = Ball(space,COLORS[start%len(COLORS)], start,15,2.0,(WIDTH//8, HEIGHT//2),1.0,0.0,(0,0))
#         ball.apply_initial_velocity(INITIAL_VELOCITY)
#         BALLS.append(ball)
#         start+=1
# Few Ball (2 or 3) simulation
POSITIONS = []
MIDPOINT = None
VELOCITY = 3e2
if NUM_BALLS==2:
    for i in range(NUM_BALLS):
        POSITIONS.append([random.randint(WIDTH//8, 14*(WIDTH)//16),random.randint(HEIGHT//6, 4*(HEIGHT)//6)])
    MIDPOINT = [(POSITIONS[0][0]+POSITIONS[1][0])/2,(POSITIONS[0][1]+POSITIONS[1][1])/2]
    for i in range(NUM_BALLS):
        position = POSITIONS[i]
        distance = [MIDPOINT[0]-position[0],MIDPOINT[1]-position[1]]
        disMagnitude = (distance[0]**2+distance[1]**2)**0.5
        velocity = [distance[0]*VELOCITY/disMagnitude,distance[1]*VELOCITY/disMagnitude]
        ball = Ball(space, COLORS[i%len(COLORS)], i+1, 15 , 2.0 , (POSITIONS[i][0],POSITIONS[i][1]) , 1.0 , 0.0 , (0.0,0.0))
        ball.apply_initial_velocity((velocity[0],velocity[1]))
        BALLS.append(ball)
if NUM_BALLS==3:
    for i in range(NUM_BALLS):
        POSITIONS.append([random.randint(WIDTH//8, 14*(WIDTH)//16),random.randint(HEIGHT//6, 4*(HEIGHT)//6)])
    MIDPOINT = circumcenter(POSITIONS[0],POSITIONS[1],POSITIONS[2])
    for i in range(NUM_BALLS):
        position = POSITIONS[i]
        distance = [MIDPOINT[0]-position[0],MIDPOINT[1]-position[1]]
        disMagnitude = (distance[0]**2+distance[1]**2)**0.5
        velocity = [distance[0]*VELOCITY/disMagnitude,distance[1]*VELOCITY/disMagnitude]
        ball = Ball(space, COLORS[i%len(COLORS)], i+1, 15 , 2.0 , (position[0],position[1]) , 1.0 , 0.0 , (0.0,0.0))
        ball.apply_initial_velocity((velocity[0],velocity[1]))
        BALLS.append(ball)
table = Table(screen, BALLS, space, clock)
if __name__ == "__main__":
    table.create_boundary(BOTTOM_LEFT, TOP_RIGHT,line_elasticity=1.0,line_friction=0.0)
    table.run_simulation(num_steps=500)