from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import matplotlib.pyplot as plt
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer, UserParam
from mesa.visualization import Slider

class SIRAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "S"  # All agents start as susceptible

    def step(self):
        if self.state == "I":
            self.infect_others()
            self.recover()

    def infect_others(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)
        for neighbor in neighbors:
            if neighbor.state == "S":
                if np.random.random() < self.model.infection_prob:
                    neighbor.state = "I"

    def recover(self):
        if np.random.random() < self.model.recovery_prob:
            self.state = "R"

class SIRModel(Model):
    def __init__(self, width, height, density, infection_prob, recovery_prob, initial_infected=1):
        self.num_agents = width * height * density
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.infection_prob = infection_prob
        self.recovery_prob = recovery_prob

        # Create agents
        for i in range(int(self.num_agents)):
            agent = SIRAgent(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

        # Infect some agents initially
        for i in range(initial_infected):
            agent = self.random.choice(self.schedule.agents)
            agent.state = "I"

        self.datacollector = DataCollector(
            agent_reporters={"State": "state"},
            model_reporters={"Susceptible": self.count_susceptible,
                             "Infected": self.count_infected,
                             "Recovered": self.count_recovered}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def count_susceptible(self):
        return sum([1 for a in self.schedule.agents if a.state == "S"])

    def count_infected(self):
        return sum([1 for a in self.schedule.agents if a.state == "I"])

    def count_recovered(self):
        return sum([1 for a in self.schedule.agents if a.state == "R"])

def agent_portrayal(agent):
    if agent.state == "S":
        portrayal = {"Shape": "circle",
                     "Color": "blue",
                     "Filled": "true",
                     "r": 0.8}
    elif agent.state == "I":
        portrayal = {"Shape": "circle",
                     "Color": "red",
                     "Filled": "true",
                     "r": 0.8}
    else:  # agent.state == "R"
        portrayal = {"Shape": "circle",
                     "Color": "green",
                     "Filled": "true",
                     "r": 0.8}
    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

chart = ChartModule([{"Label": "Susceptible", "Color": "blue"},
                     {"Label": "Infected", "Color": "red"},
                     {"Label": "Recovered", "Color": "green"}],
                    data_collector_name='datacollector')

server = ModularServer(SIRModel,
                       [grid, chart],
                       "SIR Model",
                       {"width": 20,
                        "height": 20,
                        "density": Slider("Density", 0.8, 0.1, 1.0, 0.1),
                        "infection_prob": Slider("Infection Probability", 0.2, 0.01, 1.0, 0.01),
                        "recovery_prob": Slider("Recovery Probability", 0.05, 0.01, 1.0, 0.01),
                        "initial_infected": Slider("Initial Infected", 5, 1, 20, 1)
                       })

server.port = 8521  # Default port
server.launch()
