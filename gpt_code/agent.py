from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import random
import matplotlib.pyplot as plt

class SIRAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "S"  # 初期状態は感受性者（Susceptible）
        self.infection_duration = 0

    def step(self):
        if self.state == "I":
            self.infection_duration += 1
            if self.infection_duration > self.model.recovery_time:
                self.state = "R"
            else:
                self.infect_others()

        if self.state == "S":
            self.move()
            self.check_infection()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def check_infection(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if agent.state == "I":
                if random.random() < self.model.infection_rate:
                    self.state = "I"
                    break

    def infect_others(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if agent.state == "S":
                if random.random() < self.model.infection_rate:
                    agent.state = "I"

class SIRModel(Model):
    def __init__(self, width, height, N, infection_rate, recovery_time, initial_infected, ):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.infection_rate = infection_rate
        self.recovery_time = recovery_time

        # エージェントの作成
        for i in range(self.num_agents):
            agent = SIRAgent(i, self)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        # 初期感染者の設定
        infected_agents = self.random.sample(self.schedule.agents, initial_infected)
        for agent in infected_agents:
            agent.state = "I"

        self.datacollector = DataCollector(
            model_reporters={
                "Susceptible": lambda m: self.count_state(m, "S"),
                "Infected": lambda m: self.count_state(m, "I"),
                "Recovered": lambda m: self.count_state(m, "R"),
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    @staticmethod
    def count_state(model, state):
        count = 0
        for agent in model.schedule.agents:
            if agent.state == state:
                count += 1
        return count

# 結果のプロット
def plot_results(model):
    results = model.datacollector.get_model_vars_dataframe()
    results.plot()
    plt.xlabel('Step')
    plt.ylabel('Number of Agents')
    plt.title('SIR Model with Age Groups')
    plt.show()

# シミュレーションの実行
model = SIRModel(width=20, height=20, N=200, infection_rate=0.05, recovery_time=10, initial_infected=5)
for i in range(100):
    model.step()

# plot_results(model)

from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, Choice

# エージェント描画関数
def agent_portrayal(agent):
    if agent.state == "S":
        portrayal = {"Shape": "circle", "Color": "blue", "Filled": True, "r": 0.8}
    elif agent.state == "I":
        portrayal = {"Shape": "circle", "Color": "red", "Filled": True, "r": 0.8}
    elif agent.state == "R":
        portrayal = {"Shape": "circle", "Color": "green", "Filled": True, "r": 0.8}
    return portrayal

# グリッドの描画設定
grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

# チャートの設定
chart = ChartModule([
    {"Label": "Susceptible", "Color": "Blue"},
    {"Label": "Infected", "Color": "Red"},
    {"Label": "Recovered", "Color": "Green"}
])

# モデルパラメータの設定
model_params = {
    "width": 20,
    "height": 20,
    "N": Slider("Number of agents", 200, 1, 300, 1),
    "infection_rate": Slider("Infection rate", 0.05, 0.01, 1.0, 0.01),
    "recovery_time": Slider("Recovery time", 10, 1, 50, 1),
    "initial_infected": Slider("Initial infected", 5, 1, 50, 1)
}

# サーバーの設定と起動
server = ModularServer(SIRModel, [grid, chart], "SIR Model", model_params)
server.port = 8521
server.launch()
