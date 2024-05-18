from random import random, randint
import numpy as np
import matplotlib.pyplot as plt
import os
import imageio

# Setting global variable
# Infection_Rate = 0.3
# Population = 100
# Boundary = 50
# Vision = 1
# Infection_Period = 10
# Initial_Infected = 0.4
# Rate_SIR = [0]*3
# walkers = []
# speed = 0.4
# Days = 5

def distance_age(x1, y1, x2, y2):
  return (np.sqrt((x1 - x2)**2 + (y1 - y2)**2))

def color_adjustment(self):
  if self.condition == 0:
      self.color = "green"
  elif self.condition == 1:
      self.color = "red"
  elif self.condition == 2:
      self.color = "blue"

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
    self.forsort = 0

  def turn(self):
    self.direction += 60*(random()*0.5)

  def forward(self, speed, Boundary):
    self.x += speed * np.cos(np.radians(self.direction))
    self.y += speed * np.sin(np.radians(self.direction))
    # To loop the agents if its coordinate out of range
    self.x %= Boundary
    self.y %= Boundary

class Universe():
  def __init__(self):
    self.walkers = []
    self.speed = 0.4
    self.Days = 150
    self.Rate_SIR = [0]*3
    self.Infection_Rate = 0.5
    self.Population = 1000
    self.Boundary = 50
    self.Vision = 1.5
    self.Infection_Period = 30
    self.Initial_Infected = 3
  
  def MakeAllAgeSetAroundOwn(self, agt):
    neighbors = []
    for one in self.walkers:
      if one.id == agt.id:
        continue
      distance = distance_age(agt.x, agt.y, one.x, one.y)
      if distance <= self.Vision:
        neighbors.append(one)
        # print(f"Agent {agt.id} checking Agent {one.id}: Distance = {distance}, Vision = {self.Vision}")
    return (neighbors)
  
  def univ_init(self):
    for i in range(self.Population):
      tmp_age = Walker(i)
      self.walkers.append(tmp_age)

    if self.Initial_Infected < 1:
      for one in self.walkers:
        if random() < self.Initial_Infected:
          one.condition = 1
          one.RN = 0
        else:
          one.condition = 0
    else:
      counter = 0
      for one in self.walkers:
        if counter < self.Initial_Infected:
          one.condition = 1
          one.RN = 0
          counter+=1

  def agt_step(self, agt):
    agt.turn()
    agt.forward(self.speed, self.Boundary)
    neighbors = self.MakeAllAgeSetAroundOwn(agt)
    # print(neighbors)
    if agt.condition == 0:
      pass
    elif agt.condition == 1:
      agt.counter += agt.counter
      for one in neighbors:
        if (one.condition == 0) & (random() < self.Infection_Rate):
          one.condition = 1
          one.RN = 0
          agt.RN += 1
      if (1 / self.Infection_Period > random()):
        agt.condition = 2
        agt.counter = 0
    elif agt.condition == 2:
      pass
    # color_adjustment(self)

  def univ_step_begin(self):
    for one in self.walkers:
      one.forsort = random()
    self.walkers = sorted(self.walkers, key=lambda x: x.forsort)
    # for one in self.walkers:
    #   color_adjustment(one)

  def univ_step_end(self):
    for i in range(len(self.Rate_SIR)):
      self.Rate_SIR[i] = 0
    for one in self.walkers:
      self.Rate_SIR[one.condition] += 1
    # print(self.Rate_SIR)
    # for i in range(len(Rate_SIR)):
    #   Rate_SIR[i] /= len(walkers)

  def plot_data(self, data):
    days = list(range(self.Days))
    s = [day[0] for day in data]
    i = [day[1] for day in data]
    r = [day[2] for day in data]

    plt.figure(figsize=(10, 6))
    plt.plot(days, s, label='Susceptible', color='green')
    plt.plot(days, i, label='Infected', color='red')
    plt.plot(days, r, label='Recovered', color='blue')

    plt.xlabel('Days')
    plt.ylabel('Number')
    plt.title('SIR Model')
    plt.legend()
    plt.grid(True)
    plt.savefig('sirmodel.png')
    plt.show

  def plot_walkers(self, day):
    colors = {0: 'green', 1: 'red', 2: 'blue'}
    plt.figure(figsize=(10, 10))
    for one in self.walkers:
        plt.scatter(one.x, one.y, color=colors[one.condition], s=10)
    plt.xlim(0, self.Boundary)
    plt.ylim(0, self.Boundary)
    plt.title(f'Day {day}')
    plt.savefig(f'frames/frame_{day}.png')
    plt.close()

def main():
  data = []
  universe = Universe()
  universe.univ_init()
  for day in range(universe.Days):
    universe.univ_step_begin()
    for one in universe.walkers:
      universe.agt_step(one)
    universe.univ_step_end()
    data.append(universe.Rate_SIR[:])
    universe.plot_walkers(day)
  universe.plot_data(data)

    # Create GIF
  with imageio.get_writer('simulation.gif', mode='I', duration=0.5) as writer:
      for day in range(universe.Days):
          filename = f'frames/frame_{day}.png'
          image = imageio.imread(filename)
          writer.append_data(image)

  # Clean up frames directory
  for day in range(universe.Days):
      os.remove(f'frames/frame_{day}.png')

if __name__ == "__main__":
  main()