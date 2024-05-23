import os
import imageio
from universe import Universe
import yaml

def main():
  with open('config/walker_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
  ganma = config['ganma']
  data = []
  universe = Universe()
  universe.univ_init()
  universe.plot_hist(ganma)
  for day in range(universe.Days):
    universe.univ_step_begin()
    for one in universe.walkers:
      universe.agt_step(one)
    universe.univ_step_end()
    data.append(universe.Rate_SIR[:])
    universe.plot_walkers(day)
  universe.plot_data(data,ganma)

    # Create GIF
  with imageio.get_writer(f'/out/GIF/simulation_ganma{ganma}.gif', mode='I', duration=0.5) as writer:
      for day in range(universe.Days):
          filename = f'frames/frame_{day}.png'
          image = imageio.imread(filename)
          writer.append_data(image)

  # Clean up frames directory
  for day in range(universe.Days):
      os.remove(f'frames/frame_{day}.png')

if __name__ == "__main__":
  main()