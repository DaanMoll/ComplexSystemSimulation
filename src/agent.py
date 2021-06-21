import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import numba as nb
from utils import *


DIMS = 2
R = 1.5

CLOSE_DISTANCE = 5*R
TOUCH_DISTANCE = 2*R
COMPLETE_STOP = R
DT = 0.01

HUMAN_ATTR_FORCE = 10
HUMAN_REPULS_FORCE = 5
GATE_SWITCH_THRESHOLD = 3

#xmin, xmax, y
HWALLS = np.array([[10, 100, 100],
                     [10, 100, 0.00],
                     [0, 10, 45],
                     [0, 10, 55]])

#ymin, ymax, x
VWALLS = np.array([[10, 100, 100],
                     [0, 46, 10],
                     [54, 100, 10]])

WALL_REPULS_FORCE = 5

@nb.njit(fastmath=True)
def Dist(pos1, pos2):
    diffx = pos1[0] - pos2[0]
    diffy = pos1[1] - pos2[1]
    return np.sqrt(diffx*diffx + diffy*diffy)

class Agent(object):
    def __init__(self, environment):
        self.pos = np.zeros(DIMS)
        self.vel = np.zeros(DIMS)
        self.environment = environment

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
    def __init__(self, environment, interval=1):
        super().__init__(environment)
        self.human_attr_force = 1.05
        self.timesteps_passed = 0
        self.interval = interval
        self.type = None

    def timestep(self):
        # I'm a gate and don't need updates for now
        pass

    def update_position(self, agents):
        closest = 10000
        closest_agent = None
        # Skip if entrance of alley

        if self.type == GATE_TYPES.entrance:
            return

        if self.timesteps_passed >= self.interval:
            # get closest agent and remove it from system
            for agent in agents["humans"]:
                if agent.pos[0] < 0.1:
                    self.environment.delete_agent(agent)
                distance = Dist(self.pos, agent.pos)

                # if distance < closest:
                #     closest = distance
                #     closest_agent = agent

            # if closest < 1.2: #check 10 idk what is good.
            #     self.environment.delete_agent(closest_agent)
            #     self.timesteps_passed = 0

        self.timesteps_passed += 1
        pass

    def get_pos(self):
        return self.pos

    def set_pos(self):
        pass


class Human(Agent):
    def __init__(self, environment, pos):
        super().__init__(environment)
        self.pos = pos

        norm = np.inf
        self.goal_gate = None

        for gate in self.environment.agents["gates"]:
            direction_vec_test = np.subtract(gate.pos, self.pos)
            vec_norm = np.linalg.norm(direction_vec_test)

            # If it is the closest gate, save its normalised version
            if vec_norm < norm: # dan vec_norm altijd norm bij 1 gate
                norm = vec_norm
                self.goal_gate = gate

        self.orig_distance = vec_norm

        if self.goal_gate == None:
            print("ERROR NO CLOSEST GATE", self)

    def timestep(self):
        self.update_position()

    def forces(self, agents):
        # Create empty force/friction list
        F = np.array([0., 0.])
        friction = 1
        norm = np.inf

        # Gates "attraction force"

        # Get the direction vector between agent and gate
        direction_vec_test = np.subtract(self.goal_gate.pos, self.pos)
        #TODO linalg
        norm = np.linalg.norm(direction_vec_test)
        if norm < GATE_SWITCH_THRESHOLD and self.goal_gate.type == GATE_TYPES.entrance:
            # Select the gate which has type exit and assign to closest gate
            self.goal_gate = next((gate for gate in self.environment.agents["gates"] if gate.type == GATE_TYPES.exit), None)
        direction_vec = direction_vec_test / norm

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
                factor = CLOSE_DISTANCE / (vec_norm+1)
                norm_direction_vec = direction_vec / vec_norm
                F += HUMAN_REPULS_FORCE * norm_direction_vec * factor

            # Friction forces
            if vec_norm < TOUCH_DISTANCE:
                friction = friction*max(-TOUCH_DISTANCE + COMPLETE_STOP + vec_norm, 0.1) / R


        if self.pos[1] < 5*R or self.pos[1] > self.environment.max_y - (5*R) or self.pos[0] < 10 + 5*R or self.pos[0] < self.environment.max_x - 5*R:
            # Wall Forces
            for wall in HWALLS:

                # Check if just underneath or above a wall
                if self.pos[0] > wall[0] and self.pos[0] < wall[1] and (self.pos[1] < wall[2]
                    + CLOSE_DISTANCE  and self.pos[1] > wall[2] - CLOSE_DISTANCE):
                    # Determine distance
                    dist = wall[2] - self.pos[1]

                    F -= WALL_REPULS_FORCE/(dist) * np.array([0,1])


            for wall in VWALLS:
                # Check if just underneath or above a wall
                if self.pos[1] > wall[0] and self.pos[1] < wall[1] and (self.pos[0] < wall[2]
                    + CLOSE_DISTANCE and self.pos[0] > wall[2] - CLOSE_DISTANCE):
                    # Determine distance
                    dist = wall[2] - self.pos[0]

                    F -= WALL_REPULS_FORCE/(dist) * np.array([1,0])



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
    
