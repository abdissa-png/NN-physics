import time
import pygame
import pymunk.pygame_util
import pymunk
from Ball import Ball
import sys
import numpy as np
import json
import os
class Table:
    def __init__(self, screen:pygame.Surface, balls:list[Ball], space:pymunk.Space,clock:pygame.time.Clock,tick_rate:int=50):
        self.screen = screen
        self.balls = balls
        self.space = space
        self.clock = clock
        self.tick_rate = tick_rate
        self.draw_options = pymunk.pygame_util.DrawOptions(screen)
        self.iteration = 0
        self.running = True
        self.dragging = False
        self.dragged_ball = None
        self.start_pos = None
        self.end_pos = None
    def create_boundary(self,bottom_left,top_right,line_elasticity:float=0.8,line_friction:float=0.4):
        bl1,bl2 = bottom_left
        tr1,tr2 = top_right
        # bottom, top, left, right
        self.static_lines = [
        pymunk.Segment(self.space.static_body, (bl1, bl2), (tr1, bl2), 5),
        pymunk.Segment(self.space.static_body, (bl1, tr2), (tr1, tr2), 5),
        pymunk.Segment(self.space.static_body, (bl1,bl2), (bl1, tr2), 5),
        pymunk.Segment(self.space.static_body, (tr1, bl2), (tr1,tr2), 5),
        ]
        for line in self.static_lines:
            line.elasticity = line_elasticity if 0<=line_elasticity<=1 else 0.8
            line.friction = line_friction if 0<=line_friction<=1 else 0.4
            self.space.add(line)
    def run_simulation(self,enable_drag:bool=True,log_state:bool=True,num_steps:int=100000):
        state_array = []
        KE_array = []
        Momentum_array = []
        while self.running:
            self.space.step(1/self.tick_rate)
            if self.iteration >= num_steps:
                self.running = False
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if enable_drag:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not self.dragging:
                            mouse_pos = pygame.mouse.get_pos()
                            x,y = mouse_pos
                            for ball in self.balls:
                                if pymunk.Vec2d(x,y).get_distance(ball.body.position) <= ball.radius:
                                    self.dragging = True
                                    self.dragged_ball = ball
                                    self.start_pos = ball.body.position
                                    break
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.dragging:
                            self.dragging = False
                            end_pos = pygame.mouse.get_pos()
                            self.end_pos = pymunk.Vec2d(end_pos[0],end_pos[1])
                            self.dragged_ball.apply_impulse((self.start_pos[0]-self.end_pos[0],self.start_pos[1]-self.end_pos[1]),(self.end_pos[0],self.end_pos[1]))
            self.screen.fill((0, 0, 0))
            # log physics state
            if log_state and self.running:
                    state=[]
                    KE = 0
                    Momentum = (0,0)
                    for ball in self.balls:
                        state.append(ball.get_state())
                        if ball.body.torque!=0:print(ball.body.torque)
                        if ball.body.force.x!=0:print(ball.body.force.x)
                        if ball.body.force.y!=0:print(ball.body.force.y)
                        KE += ball.get_KineticEnergy()
                        ball_momentum = ball.get_Momentum()
                        Momentum = (Momentum[0]+ball_momentum[0],Momentum[1]+ball_momentum[1])
                    state_array.append(state)
                    KE_array.append(KE)
                    Momentum_array.append(Momentum)
            self.space.debug_draw(self.draw_options)
            for ball in self.balls:
                ball.draw_ball(self.screen)
             # Draw force line if dragging
            if self.dragging and self.start_pos:
                current_pos = pygame.mouse.get_pos()
                pygame.draw.line(self.screen, (255, 0, 0), self.start_pos, current_pos, 2)
            self.iteration += 1
            pygame.display.flip()
            self.clock.tick(self.tick_rate)
        if log_state:
            KE_array = np.array(KE_array)
            Momentum_array = np.array(Momentum_array)
            state_array = np.array(state_array)
            Time = int(time.time())
            # Define the directory and filename
            directory = f'./sims/{Time} simulation for {self.iteration} steps/'

            # Create the directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)
            # Get the absolute path of the directory
            directory_path = os.path.abspath(directory)
            np.save(f'{directory_path}/KE.npy',KE_array)
            np.save(f'{directory_path}/Momentum.npy',Momentum_array)
            np.save(f'{directory_path}/state.npy',state_array)
            metadata = {
                "Number of steps": self.iteration,
                "Number of balls": len(self.balls),
                "Line elasticity": self.static_lines[0].elasticity,
                "Line friction": self.static_lines[0].friction,
                "Tick rate": self.tick_rate,
                "Balls": []
            }

            for ball in self.balls:
                ball_data = {
                    "Ball number": ball.number,
                    "Mass": ball.mass,
                    "Radius": ball.radius,
                    "Elasticity": ball.elasticity,
                    "Friction": ball.friction
                }
                metadata["Balls"].append(ball_data)

            with open(f'{directory_path}/metadata.json', 'w') as file:
                json.dump(metadata, file)
        pygame.quit()
        sys.exit()

