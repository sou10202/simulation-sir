from random import randint, random
import numpy as np
from utils import power_low
import yaml

class Walker():
  def __init__(self, id):
    self.id = id
    self.counter = 0 # to count incubation period
    self.x = randint(0, 50)
    self.y = randint(0, 50)
    self.condition = 0
    self.direction = random()*360
    self.color = 0
    self.RN = 0 # RN is Reproduction Number -> to count how many other agents that agent spread the infection to
    self.forsort = 0 # Power low distribution with gamma = 2 and min value = 0.4
    self.load_config('config/walker_config.yaml')

  def load_config(self, file):
    with open(file, 'r') as f:
      config = yaml.safe_load(f)
    self.ganma = config['ganma']
    self.minspeed = config['minspeed']
    self.speed = power_low(self.ganma, self.minspeed)

  def turn(self):
    self.direction += 60*(random()*0.5)

  def forward(self, Boundary):
    self.x += self.speed * np.cos(np.radians(self.direction))
    self.y += self.speed * np.sin(np.radians(self.direction))
    # To loop the agents if its coordinate out of range
    self.x %= Boundary
    self.y %= Boundary