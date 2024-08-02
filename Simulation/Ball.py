import pymunk
import pygame
import math
class Ball:
    def __init__(self, space:pymunk.Space, color:tuple[int,int,int],number:int, radius:float, mass:float, position:tuple[float,float],elasticity:float=0.75,friction:float=0.6, velocity:tuple[float,float]=(0,0),font_size:int=24):
        self.radius = radius
        self.mass = mass
        self.body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
        self.body.position = position
        self.body.velocity = velocity
        self.shape = pymunk.Circle(self.body, radius)
        self.elasticity = elasticity if 0<=elasticity<=1 else 0.75
        self.shape.elasticity = self.elasticity
        self.friction = friction if 0<=friction<=1 else 0.6
        self.shape.friction = self.friction
        self.color = color + (255,)
        self.number = number  # Add number to the shape
        self.font = pygame.font.Font(None, 24)
        space.add(self.body, self.shape)
    def apply_force(self, force:tuple[float,float],position:tuple[float,float]=(0.,0.)):
        self.body.apply_force_at_local_point(force, position)
    def apply_initial_velocity(self,velocity:tuple[float,float]):
        self.body.velocity = velocity
    def draw_ball(self,screen:pygame.Surface):
        pygame.draw.circle(screen, self.color, self.get_position(), self.radius, 0)
        # Draw the number with rotation
        text = self.font.render(str(self.number), True, (255, 255, 255))
        text = pygame.transform.rotate(text, -math.degrees(self.body.angle))  # Rotate the text
        text_rect = text.get_rect(center=self.get_position())
        screen.blit(text, text_rect)
    def get_position(self):
        return (self.body.position.x,self.body.position.y)
    def get_state(self,rounded:bool=True):
        # x-position, y-position, x-velocity, y-velocity, angle, angular-velocity
        state = [self.body.position[0],self.body.position[1],self.body.velocity[0],self.body.velocity[1],self.body.angle,self.body.angular_velocity]
        if rounded:
            state = [round(i,4) for i in state]
        return state
    def get_KineticEnergy(self):
        return 0.5*self.mass*(self.body.velocity.x**2+self.body.velocity.y**2)    
    def get_Momentum(self):
        return (self.mass*self.body.velocity.x,self.mass*self.body.velocity.y)
    def get_AngularMomentum(self):
        return self.body.moment*self.body.angular_velocity
    def apply_impulse(self,impulse:tuple[float,float],position:tuple[float,float]=(0.,0.)):
        self.body.apply_impulse_at_world_point(impulse, position)