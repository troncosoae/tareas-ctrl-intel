import pygame
import math
import time

# @https://github.com/keychali/pendulum-simulation/blob/master/forvideo.py

pygame.init()

clock = pygame.time.Clock()
closed = False

width, height =(1000,600)
window = pygame.display.set_mode((width,height))

class bob(object):
    def __init__(self,point):
        self.x = point[0]
        self.y = point[1]
    def draw(self,bg):
        pygame.draw.lines(bg,(0,0,0),False,[(width/2,0),(self.x,self.y)],2)
        pygame.draw.circle(bg,(0,0,0),(self.x,self.y),25)
        pygame.draw.circle(bg,(255,255,255),(self.x,self.y),23)
        pygame.draw.circle(bg,(160,50,50),(self.x,self.y),10)

move =False

def move_bob():
    mapandul.x= round(width/2 + length*math.sin(angle))
    mapandul.y= round(length*math.cos(angle))
    

def angle_length():
    length =math.sqrt(math.pow(width/2-mapandul.x,2)+math.pow(mapandul.y,2))
    angle = math.asin((mapandul.x-width/2)/length)
    return (angle,length)

def refresh():
    window.fill((255,255,255))
    mapandul.draw(window)
    pygame.display.update()

mapandul = bob((150,150))

while not closed:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            closed=True
        if event.type==pygame.MOUSEBUTTONDOWN:
            move=False
            mapandul = bob(pygame.mouse.get_pos())
            angle, length = angle_length()
            start_time =time.time()
        if event.type==pygame.MOUSEBUTTONUP:
            matime = time.time() - start_time
            xx,yy= pygame.mouse.get_pos()
            hl = math.sqrt(math.pow(xx-mapandul.x,2)+math.pow(yy-mapandul.y,2))+0.01
            vel =math.asin((xx-mapandul.x)/hl)*hl/(matime*10000+1)
            move =True
    if move:
        acc = -0.000981 * math.sin(angle)
        vel +=acc
        vel *=0.999
        angle+=vel
        move_bob()
        
    refresh()
    


    
pygame.quit()