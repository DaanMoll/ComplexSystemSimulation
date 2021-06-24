import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import numba as nb
from Agent import *
from Utils import *
from tqdm import tqdm
from constant import *

class Environment():
    """
    The main environment class.
    """
    def __init__(self, num_agents, max_x, min_x, max_y, min_y):
        self.agents = {"humans": [], "gates": []}
        self.max_x = max_x
        self.min_x = min_x
        self.max_y = max_y
        self.min_y = min_y
        self.num_agents = num_agents
        self.poslist = []

        self.timesteps = 0

        # Initialize gates and humans
        self.init_gates()
        self.init_humans()

        for agent_type in reversed(self.agents.keys()):
            for agent in self.agents[agent_type]:
                self.poslist.append(agent.pos)

    def timestep(self, return_positions=False):
        self.timesteps += 1
        self.poslist = []

        for agent_type in reversed(self.agents.keys()):
            for agent in self.agents[agent_type]:
                if not agent.agent_left:
                    agent.update_position(self.agents)
                self.poslist.append(agent.pos)
        if return_positions:
            return self.poslist

    def random_position(self):
        x = np.random.uniform(low=self.min_x+1, high=self.max_x-1)
        y = np.random.uniform(low=self.min_y+1, high=self.max_y-1)
        return (x, y)

    def init_humans(self):
        print("Initializing agents...")
        current_positions = []
        for i in tqdm(range(self.num_agents)):
            new_agent = Human(self, self.random_position())
            while any(dist(new_agent.pos, pos) < 2*R for pos in current_positions):
                new_agent = Human(self, self.random_position())
            current_positions.append(new_agent.pos)
            self.agents["humans"].append(new_agent)

    def init_gates(self):
        # Init exit of "alley"
        exit = Gate(self)
        exit.pos = (-10, self.max_y/2)
        exit.type = GATE_TYPES.exit
        self.agents["gates"].append(exit)

        # Init entrance of "alley"
        entrance = Gate(self)
        entrance.pos = (self.min_x, self.max_y/2)
        entrance.type = GATE_TYPES.entrance
        self.agents["gates"].append(entrance)


    def delete_agent(self, agent):
        print("agent left, original distance: ", agent.orig_distance, "| timesteps:", self.timesteps, "| dist/time: ", agent.orig_distance / self.timesteps)
        
        # self.agents["humans"].remove(agent)
        agent.agent_left = True
        agent.pos = (NaN, NaN)
        self.num_agents -= 1

    def __str__(self):
        return f"{self.__class__.__name__}: \n\tnum_agents: {self.num_agents} \
                                            \n\tx_max: {self.max_x} \
                                            \n\ty_max: {self.max_y}"
        __repr__ = __str__


if __name__ == '__main__':
    print("Running this file does not do anything.")   
