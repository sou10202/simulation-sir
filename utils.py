import numpy as np

def distance_age(x1, y1, x2, y2):
  return (np.sqrt((x1 - x2)**2 + (y1 - y2)**2))

def power_low(ganma, min_value):
  r = np.random.uniform(0, 1)
  return min_value * (1 - r)**(-1 / (ganma-1))