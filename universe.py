from utils import distance_age
from walker import Walker
import matplotlib.pyplot as plt
from random import random
import yaml

class Universe():
  def __init__(self):
    self.walkers = []
    self.Rate_SIR = [0, 0, 0]
    self.Rate_SIR_young = [0, 0, 0]
    self.Rate_SIR_old = [0, 0, 0]
    self.load_config('config/universe_config.yaml')

  def load_config(self, file):
    with open(file, 'r') as f:
       config = yaml.safe_load(f)
    self.Days = config['Days']
    self.Population = config['Population']
    self.Initial_Infected = config['Initial_Infected']
    self.Vision = config['Vision']
    self.Boundary = config['Boundary']
    self.Infection_Rate_young = config['Infection_Rate_young']
    self.Infection_Rate_old = config['Infection_Rate_old']
    self.Infection_Period = config['Infection_Period']
    self.youngpeople_rate = config['Youngpeople_rate']
  
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
      if i < self.Population * self.youngpeople_rate:
        tmp_age = Walker(i, 1)
      else:
        tmp_age = Walker(i, 2)
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
    agt.forward(self.Boundary)
    neighbors = self.MakeAllAgeSetAroundOwn(agt)
    if agt.condition == 0:
      pass
    elif agt.condition == 1:
      agt.counter += agt.counter
      for one in neighbors:
        if one.agegroup == 1:
          Infection_Rate = self.Infection_Rate_young
        else:
          Infection_Rate = self.Infection_Rate_old
        if (one.condition == 0) & (random() < Infection_Rate):
          one.condition = 1
          one.RN = 0
          agt.RN += 1
      if (1 / self.Infection_Period > random()):
        agt.condition = 2
        agt.counter = 0
    elif agt.condition == 2:
      pass

  def univ_step_begin(self):
    for one in self.walkers:
      one.forsort = random()
    self.walkers = sorted(self.walkers, key=lambda x: x.forsort)
    # for one in self.walkers:
    #   color_adjustment(one)

  def univ_step_end(self):
    for i in range(len(self.Rate_SIR)):
      self.Rate_SIR_young[i] = 0
      self.Rate_SIR_old[i] = 0
      self.Rate_SIR[i] = 0
    for one in self.walkers:
      if one.agegroup == 1:
        self.Rate_SIR_young[one.condition] += 1
      else:
        self.Rate_SIR_old[one.condition] += 1
      self.Rate_SIR[one.condition] += 1
    # print(self.Rate_SIR)
    # for i in range(len(Rate_SIR)):
    #   Rate_SIR[i] /= len(walkers)

  def plot_data(self, data, ganma, group):
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
    plt.title(f'SIR Model ganma={ganma} {group}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'out/PNG/sirmodel_ganma{ganma}_{group}.png')
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

  def plot_hist(self, ganma):
    x = [one.speed for one in self.walkers]
    plt.hist(x, range=(0.2, 5))
    plt.xlabel('Speed')
    plt.ylabel('Number of Agents')
    plt.title(f'Speed Distribution ganma={ganma}')
    plt.grid(True)
    plt.savefig(f'speed_distribution_ganma{ganma}.png')
    plt.close()