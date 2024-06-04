import os
import imageio
from universe import Universe
import yaml

def main():
  data = []
  data_young = []
  data_old = []
  universe = Universe()
  universe.univ_init()
  # universe.plot_hist(ganma) # Plot histogram of speed
  for day in range(universe.Days):
    universe.univ_step_begin()
    for one in universe.walkers:
      universe.agt_step(one)
    universe.univ_step_end()
    data.append(universe.Rate_SIR[:])
    data_young.append(universe.Rate_SIR_young[:])
    data_old.append(universe.Rate_SIR_old[:])
    universe.plot_walkers(day)
  universe.plot_data(data, "all")
  universe.plot_data(data_young, "young")
  universe.plot_data(data_old, "old")

    # Create GIF
  with imageio.get_writer(f'out/GIF/simulation_age.gif', mode='I', duration=0.5) as writer:
      for day in range(universe.Days):
          filename = f'frames/frame_{day}.png'
          image = imageio.imread(filename)
          writer.append_data(image)

  # Clean up frames directory
  for day in range(universe.Days):
      os.remove(f'frames/frame_{day}.png')

if __name__ == "__main__":
  main()