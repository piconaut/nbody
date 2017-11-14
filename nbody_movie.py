#!/usr/bin/python3
import sys 
import os
import math
import numpy as np
import pygame
import pygame.camera
from pygame.locals import *

sim_w = 10.0
sim_h = 10.0
sim_depth = 2.0
screen_w = 400
screen_h = 400

w_factor = screen_w/sim_w
h_factor = screen_h/sim_h

pygame.init()
screen = pygame.display.set_mode((screen_w,screen_h))

def draw(pos):

  # Fill screen with black
  screen.fill((0,0,0))

  # Draw bodies
  for i in range(len(pos)):
    pygame.draw.circle(screen,(max(min(255,pos[i][2]*255.),0),max(min(255,pos[i][2]*255),0),max(min(255,pos[i][2]*255.),0)), (math.floor(pos[i][0]*w_factor), math.floor(pos[i][1]*h_factor)),1)

  # Flip display
  pygame.display.flip()

lines = []
with open('nbody.log','r') as f:
  for line in f:
    lines.append(line.strip().split(' '))

pos = []
vel = []
mass = []
Ek = 0
Ug = 0
for i in range(len(lines)):
  if len(lines[i]) == 1:
    draw(pos)
#    for i in range(len(mass)):
#      Ek += 0.5*mass[i]*np.linalg.norm(np.array([vel[i][0],vel[i][1],vel[i][2]]))**2
#      for j in range(len(mass)):
#        if i != j:
#          r = np.linalg.norm(np.array([pos[j][0],pos[j][1],pos[j][2]])-np.array([pos[i][0],pos[i][1],pos[i][2]]))
#          Ug -= mass[j]*mass[i]/r
#    print(Ek + Ug)
#    Ek = 0
#    Ug = 0
    pos = []
    mass = []
    vel = []

  else:
    pos.append([float(lines[i][1])+sim_w/2.,float(lines[i][2])+sim_w/2.,float(lines[i][3])+sim_w/2.])
    vel.append([float(lines[i][4]), float(lines[i][5]), float(lines[i][6])])
    mass.append(float(lines[i][0]))

file_num = 0
