import pygame
import sys
import math

class Spike:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.update_vertices()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.update_vertices()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.update_vertices()

    def update_vertices(self):
        self.vertices = [(self._x, self._y), (self._x +40 , self._y ), (self._x + 20, self._y - 40)]

        
    def collide_detection(self, player_rect):
        for vertex in self.vertices:
            if player_rect.collidepoint(vertex):
                return True
        return False

class Ground:
    def __init__(self,x,y,width,height,spike_num) -> None:
        self._x=x
        self._y=y
        self.width=width
        self.height=height
        self.spike_num =spike_num
        self.spikes=[
            Spike(self._x + i*100,self._y) for i in range(self.spike_num)
        ]   
        self.rect=pygame.Rect(self._x,self._y,self.width,self.height) 
   
def check_quarter(angle):
    angle=angle%6
    angle*= 57.32
    if angle>0 and angle<=45:
        return 0
    if angle>45 and angle<=90:
        return 1.570796326794
    if angle>90 and angle<=135:
        return 1.570796326794
    if angle>135 and angle<=180:
        return 1.570796326794*2
    if angle>180 and angle<=225:
        return 1.570796326794*2
    if angle>225 and angle<=270:
        return 1.570796326794*3
    if angle>270 and angle<=315:
        return 1.570796326794*3
    return 0

def rotate_point(point, angle, origin):
    s, c = math.sin(angle), math.cos(angle)
    x, y = point[0] - origin[0], point[1] - origin[1]
    new_x = c * x - s * y + origin[0]
    new_y = s * x + c * y + origin[1]
    return new_x, new_y

def rotate_rect(rect, angle):
    rotated_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    rotated_surface.blit(pygame.transform.rotate(pygame.Surface(rect.size, pygame.SRCALPHA), angle), (0, 0))
    new_rect = rotated_surface.get_rect(center=rect.center)
    return new_rect

pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Geometry Dash Clone")

#region Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
BLUE=(0,0,255)
#endregion
#region Player properties
player_x = 100
player_y = 300
player_speed = 10
player_angle=0
player_jump_power = -22  # Negative value for jumping upwards
player_y_velocity = 0
player_size = 50
player_rect=pygame.Rect(player_x, player_y, player_size, player_size)
image = pygame.image.load('player.jpg')
image = pygame.transform.scale(image, (player_size, player_size))
#endregion
#region Grounds
ground_height = 20
base_ground=pygame.Rect(0, 580, 1600, ground_height)

grounds = [
    Ground(400,400,600,ground_height,3),
    Ground(200,200,400,ground_height,2)
    
]
#endregion

obstacle_speed = 7

bgimage = pygame.image.load('bg.jpeg')
bgimage = pygame.transform.scale(bgimage, (800, 600))

gravity = 0.9

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #region extra code for rotate rect
    '''
    center = player_rect.center
    corners = [
        (player_rect.topleft[0], player_rect.topleft[1]),
        (player_rect.topright[0], player_rect.topright[1]),
        (player_rect.bottomright[0], player_rect.bottomright[1]),
        (player_rect.bottomleft[0], player_rect.bottomleft[1])
        
    ]
    rotated_corners = [rotate_point(corner, player_angle, center) for corner in corners]
    '''
    #endregion
    
    player_angle+=0.025
    # Player movement and gravity
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and gravity==0:  # Allow jump on ground or obstacle tops
        player_y_velocity = player_jump_power
        gravity=0.9
    #player_rect=rotate_rect(player_rect,20)    
    player_y_velocity += gravity
    player_rect.y += player_y_velocity
    #print(obstacles[0])

    

    for ground in grounds:
        # move obstacles and grounds
        
        for i,spike in enumerate(ground.spikes):
            spike.x =ground.rect.x +i*200
        ground.rect.x-=obstacle_speed
        # return obstacles and grounds to end of screen
        if ground.rect.x+ground.rect.width<0:
            ground.rect.x=800
        for spike in ground.spikes:
            if spike.collide_detection(player_rect):
                sys.exit()  # Handle collision here    
        if ground.rect.colliderect(player_rect):
            if player_rect.topleft[1]<ground.rect.y:
                player_rect.y=ground.rect.y-player_size
                gravity=0
                
                player_angle=check_quarter(player_angle)
            else:
                player_y_velocity=-player_y_velocity   

    if base_ground.colliderect(player_rect):
            if player_rect.y-player_size<base_ground.y:
                player_rect.y=base_ground.y-player_size
                gravity=0
                # check which face to land on
                player_angle=check_quarter(player_angle)
    # Clear the screen
    
    screen.fill(BLUE)  # Set background color

    screen.blit(bgimage, (0, 0))

    rotated_image = pygame.transform.rotate(image, math.degrees(-player_angle))  # Rotate the resized image
    rotated_rect = rotated_image.get_rect(center=player_rect.center)
    screen.blit(rotated_image, rotated_rect)

    for ground in grounds:
        pygame.draw.rect(screen, MAGENTA, ground.rect)
        for spike in ground.spikes:
            pygame.draw.polygon(screen, RED, spike.vertices)
    # Draw obstacles

    

    pygame.draw.rect(screen, MAGENTA, base_ground)
    
    # Draw player
    #pygame.draw.polygon(screen, GREEN, rotated_corners)
    pygame.display.flip()
    clock.tick(60)  # Cap the frame rate

pygame.quit()
sys.exit()



    