#!/usr/bin/python3
import sys 
import os
import math
import numpy as np
import pygame
import pygame.camera
from pygame.locals import *

os.environ['SDL_VIDEODRIVER'] = 'dummy'

sim_w = 10.0
sim_h = 10.0
sim_depth = 2.0
screen_w = 400
screen_h = 400

w_factor = screen_w/sim_w
h_factor = screen_h/sim_h

pygame.init()
pygame.display.set_mode((1,1))
screen = pygame.Surface((400, 400), pygame.SRCALPHA, 32)
pygame.draw.rect(screen, (0,0,0), (0, 0, 400, 400), 0)

def draw(pos):

  # Fill screen with black
  screen.fill((0,0,0))

  # Draw bodies
  for i in range(len(pos)):
#    pygame.draw.circle(screen,(max(min(255,pos[i][2]*255.),0),max(min(255,pos[i][2]*255),0),max(min(255,pos[i][2]*255.),0)), (math.floor(pos[i][0]*w_factor), math.floor(pos[i][1]*h_factor)),1)
    screen.set_at((math.floor(pos[i][0]*w_factor), math.floor(pos[i][1]*h_factor)),(max(min(255,pos[i][2]*255.),0),max(min(255,pos[i][2]*255),0),max(min(255,pos[i][2]*255.),0)))

  # Flip display
  pygame.display.flip()

lines = []
pos = []
vel = []
mass = []
Ek = 0
Ug = 0
file_num = 0
with open('nbody.log','r') as f:
  for i,line in enumerate(f):
    if i%1==0:
      line_split = line.strip().split(' ')
    
      if len(line_split) == 1:
        draw(pos)
        for i in range(len(mass)):
          Ek += 0.5*mass[i]*np.linalg.norm(np.array([vel[i][0],vel[i][1],vel[i][2]]))**2
          for j in range(len(mass)):
            if i == 0 and j == 1:
              r = np.linalg.norm(np.array([pos[j][0],pos[j][1],pos[j][2]])-np.array([pos[i][0],pos[i][1],pos[i][2]]))
              Ug -= mass[j]*mass[i]/r
 #       print(Ug + Ek)
        Ek = 0
        Ug = 0
        pos = []
        mass = []
        vel = []

        file_num = file_num + 1
        filename = "./video/%04d.png" % file_num
        pygame.image.save(screen,filename)

      else:
        pos.append([float(line_split[1])+sim_w/2.,float(line_split[2])+sim_w/2.,float(line_split[3])+sim_w/2.])
        vel.append([float(line_split[4]), float(line_split[5]), float(line_split[6])])
        mass.append(float(line_split[0]))

os.system("avconv -r 100 -f image2 -i video/%04d.png -y -qscale 0 -s " + str(screen_w) + "x"     + str(screen_h) + " -aspect 1:1 result.mp4")
#os.system("rm video/*")
