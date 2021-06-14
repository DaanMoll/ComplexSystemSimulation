import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import numba as nb


@nb.njit(fastmath=True)
def norm(l):
    s = 0.
    for i in range(l.shape[0]):
        s += l[i]**2
    return np.sqrt(s)

DIMS = 2
R = 0.1

CLOSE_DISTANCE = 5*R
TOUCH_DISTANCE = 2*R
COMPLETE_STOP = R
DT = 0.01

HUMAN_ATTR_FORCE = 10
HUMAN_REPULS_FORCE = 10

class Agent(object):
    def __init__(self, environment):
        self.pos = np.zeros(DIMS)
        self.vel = np.zeros(DIMS)
        self.environment = environment
        self.active = True

    def update_position(self, neighbors):
        pass

    def timestep(self):
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

    def forces(self, agents):
            # Create empty force/friction list
        F = np.array([0., 0.])
        friction = 1
        norm = np.inf

        # Gates "attraction force"
        for gate in agents["gates"]:
            # Get the direction vector between agent and gate
            direction_vec_test = np.subtract(gate.pos, self.pos)
            vec_norm = np.linalg.norm(direction_vec_test)

            # If it is the closest gate, save its normalised version
            if vec_norm < norm:
                direction_vec = direction_vec_test / vec_norm
                norm = vec_norm

        # Add force to the total force
        F += direction_vec * HUMAN_ATTR_FORCE

        # Human Forces
        for human in agents["humans"]:
            # Get all directions and vector norms
            direction_vec = np.subtract(self.pos, human.pos)
            vec_norm = np.linalg.norm(direction_vec)

            # Do not include self in calculation
            if vec_norm < 0.001 * R:
                continue
            # check equals impolementation or add ID to each agent TODO

            # Repulsive Force
            if vec_norm < CLOSE_DISTANCE:

                # Determine strength of repulsion
                factor = CLOSE_DISTANCE / vec_norm
                norm_direction_vec = direction_vec / vec_norm
                F += HUMAN_REPULS_FORCE * norm_direction_vec * factor

            # Friction forces
            if vec_norm < TOUCH_DISTANCE:
                friction = friction*max(-TOUCH_DISTANCE + COMPLETE_STOP + vec_norm, 0.1) / R

        F = friction * F
        return F

    def update_position(self, agents):
        force = self.forces(agents)
        pos_change = tuple(force * DT)
        self.pos = tuple(np.add(self.pos, pos_change))

    def get_pos(self):
        return self.pos

    def set_pos(self):
        #TODO
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
            gate.pos = (0, self.max_y/2)
            self.agents["gates"].append(gate)

    def __str__(self):
        return f"{self.__class__.__name__}: \n\tnum_agents: {self.num_agents} \
                                            \n\tx_max: {self.max_y} \
                                            \n\ty_max: {self.max_x} \
                                            \n\tnum_gates: {len(self.agents['gates'])}"
        __repr__ = __str__


if __name__ == '__main__':
    print("File does not do anything.")
