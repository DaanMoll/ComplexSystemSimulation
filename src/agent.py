import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from Utils import *
from constant import *

class Gate(Agent):
    def __init__(self, environment):
        super().__init__(environment)
        self.human_attr_force = 1.05
        self.type = None

    def timestep(self):
        # I'm a gate and don't need updates for now
        pass

    def update_position(self, agents):
        closest = np.inf
        closest_agent = None
        # Skip if entrance of alley

        if self.type == GATE_TYPES.entrance:
            return

        # get closest agent and remove it from system
        for agent in agents["humans"]:
            if agent.pos[0] < 0.1 and not agent.agent_left:
                self.environment.delete_agent(agent)

class Human(Agent):
    def __init__(self, environment, pos):
        super().__init__(environment)
        self.pos = pos
        norm = np.inf
        self.goal_gate = None

        for gate in self.environment.agents["gates"]:
            vec_norm = dist(gate.pos, self.pos)

            # If it is the closest gate, save its normalised version
            if vec_norm < norm: # dan vec_norm altijd norm bij 1 gate
                norm = vec_norm
                self.goal_gate = gate

        self.orig_distance = norm

        if self.goal_gate == None:
            raise Exception("ERROR NO CLOSEST GATE")

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
        norm = dist(self.goal_gate.pos, self.pos)
        if norm < GATE_SWITCH_THRESHOLD and self.goal_gate.type == GATE_TYPES.entrance:
            # Select the gate which has type exit and assign to closest gate
            self.goal_gate = next((gate for gate in self.environment.agents["gates"] if gate.type == GATE_TYPES.exit), None)
        direction_vec = direction_vec_test / norm

        # Add force to the total force
        F += direction_vec * HUMAN_ATTR_FORCE

        # Human Forces
        for human in agents["humans"]:
            # Skip myself
            if human == self or human.agent_left:
                continue
            # Get all directions and vector norms
            direction_vec = np.subtract(self.pos, human.pos)
            vec_norm = dist(self.pos, human.pos)

            # Repulsive Force
            if vec_norm < CLOSE_DISTANCE:

                # Determine strength of repulsion
                factor = CLOSE_DISTANCE / (vec_norm + 1)
                norm_direction_vec = direction_vec / vec_norm
                F += HUMAN_REPULS_FORCE * norm_direction_vec * factor

            # Friction forces
            if vec_norm < TOUCH_DISTANCE:
                friction = friction * max(-TOUCH_DISTANCE + COMPLETE_STOP + vec_norm, MAX_FRICTION) / R

        if self.pos[1] < 5*R or self.pos[1] > self.environment.max_y - (5*R) \
            or self.pos[0] < 10 + 5*R or self.pos[0] < self.environment.max_x - 5*R:
            # Horizontal wall forces
            for wall in HWALLS:

                # Check if just underneath or above a wall
                if self.pos[0] > wall[0] and self.pos[0] < wall[1] and (self.pos[1] < wall[2]
                    + CLOSE_DISTANCE  and self.pos[1] > wall[2] - CLOSE_DISTANCE):
                    # Determine distance
                    distance = wall[2] - self.pos[1]

                    F -= WALL_REPULS_FORCE/(distance) * np.array([0,1])

            # Vertical wall forces
            for wall in VWALLS:
                # Check if just underneath or above a wall
                if self.pos[1] > wall[0] and self.pos[1] < wall[1] and (self.pos[0] < wall[2]
                    + CLOSE_DISTANCE and self.pos[0] > wall[2] - CLOSE_DISTANCE):
                    # Determine distance
                    distance = wall[2] - self.pos[0]

                    F -= WALL_REPULS_FORCE/(distance) * np.array([1,0])

        F = friction * F
        return F

    def update_position(self, agents):
        force = self.forces(agents)
        pos_change = tuple(force * DT)
        self.pos = tuple(np.add(self.pos, pos_change))