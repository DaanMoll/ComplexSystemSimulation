import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import numba as nb

from agent import Gate, Human

class Environment():
    def __init__(self, num_agents, num_gates, max_x, max_y):
        self.agents = {"humans": [], "gates": []}
        self.max_x = max_x
        self.max_y = max_y
        self.num_agents = num_agents
        self.num_gates = num_gates
        self.poslist = []

        self.init_humans()
        self.init_gates()

        for agent_type in self.agents.keys():
            for agent in self.agents[agent_type]:
                self.poslist.append(agent.get_pos())

    def timestep(self, return_positions):
        # print("amount of agents:", len(self.agents["humans"]), self.num_agents)
        self.poslist = []

        for agent_type in self.agents.keys():
            for agent in self.agents[agent_type]:
                agent.update_position(self.agents)
                if return_positions:
                    self.poslist.append(agent.get_pos())
        if return_positions:
            # print(self.poslist)
            return self.poslist

    def random_position(self):
        x = np.random.uniform(low=11, high=99)
        y = np.random.uniform(low=1, high=99)
        return (x, y)

    def init_humans(self):
        for i in range(self.num_agents):
            new_agent = Human(self)
            new_agent.pos = self.random_position()
            self.agents["humans"].append(new_agent)

    def init_gates(self):
        # for _ in range(num_gates):
        #     gate = Gate(self)
        #     gate.pos = (0, self.max_y/2)
        #     self.agents["gates"].append(gate)

        gate = Gate(self)
        gate.pos = (3, self.max_y/2)
        self.agents["gates"].append(gate)

        if self.num_gates == 2:
            gate = Gate(self)
            gate.pos = (self.max_x, self.max_y/2)
            self.agents["gates"].append(gate)

    def delete_agent(self, agent):
        self.agents["humans"].remove(agent)
        self.num_agents -= 1

    def __str__(self):
        return f"{self.__class__.__name__}: \n\tnum_agents: {self.num_agents} \
                                            \n\tx_max: {self.max_y} \
                                            \n\ty_max: {self.max_x} \
                                            \n\tnum_gates: {len(self.agents['gates'])}"
        __repr__ = __str__


if __name__ == '__main__':
    print("File does not do anything.")
