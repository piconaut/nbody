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
screen_w = 200
screen_h = 200

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
for i in range(len(lines)):
  if len(lines[i]) == 1:
    draw(pos)
    pos = []
  else:
    pos.append([float(lines[i][0])+sim_w/2.,float(lines[i][1])+sim_w/2.,float(lines[i][2])+sim_w/2.])
    

file_num = 0
