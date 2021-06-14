import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc


DIMS = 2

class Agent(object):
    def __init__(self, environment):
        self.pos = np.zeros(DIMS)
        self.vel = np.zeros(DIMS)
        self.environment = environment
        self.active = True

    def update_position(self, neighbors):
        print("No update position defined for this class")
        pass

    def timestep(self):
        pass

    def update_posiition(self):
        pass

    def get_pos(self):
        pass

    def set_pos(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: pos: {self.pos} vel: {self.vel} active:{self.active}"
        __repr__ = __str__

class Gate(Agent):
    def __init__(self, environment):
        super().__init__(environment)
        self.human_attr_force = 1.05

    def timestep(self):
        # I'm a gate and don't need updates for now
        pass

    def update_position(self, agents):
        # I'm a gate and don't need updates for now
        pass

    def get_pos(self):
        return self.pos

    def set_pos(self):
        pass

class Human(Agent):
    def __init__(self, environment):
        super().__init__(environment)

    def timestep(self):
        update_position()

    def update_position(self, agents):
        # TODO repelling/attraction between humans
        new_x_pos = .0
        new_y_pos = .0

        # Gates "attraction force"
        for gate in agents["gates"]:
            new_x_pos = (self.pos[0] + abs((self.pos[0] - gate.pos[0] )  * gate.human_attr_force)) % 100
            new_y_pos = (self.pos[1] + abs((self.pos[1] - gate.pos[1]) * gate.human_attr_force)) % 100

        self.pos = new_x_pos, new_y_pos

    def get_pos(self):
        return self.pos

    def set_pos(self):
        pass

class Environment():
    def __init__(self, num_agents, num_gates, max_x, max_y):
        self.agents = {"humans": [], "gates": []}
        self.max_x = max_x
        self.max_y = max_y
        self.num_agents = num_agents
        self.poslist = []
        self.init_humans()
        self.init_gates(num_gates)
        for agent_type in self.agents.keys():
            for agent in self.agents[agent_type]:
                self.poslist.append(agent.get_pos())

    def timestep(self, return_positions):
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
        x = np.random.uniform(low=0, high=self.max_x)
        y = np.random.uniform(low=0, high=self.max_y)
        return (x, y)

    def init_humans(self):
        for i in range(self.num_agents):
            new_agent = Human(self)
            new_agent.pos = self.random_position()
            self.agents["humans"].append(new_agent)

    def init_gates(self, num_gates):
        for _ in range(num_gates):
            gate = Gate(self)
            gate.pos = self.random_position()
            self.agents["gates"].append(gate)


    def __str__(self):
        return f"{self.__class__.__name__}: \n\tnum_agents: {self.num_agents} \
                                            \n\tx_max: {self.max_y} \
                                            \n\ty_max: {self.max_x} \
                                            \n\tnum_gates: {len(self.agents['gates'])}"
        __repr__ = __str__


if __name__ == '__main__':
    print("File does not do anything.")
