from enum import Enum
import numpy as np
import numba as nb

# Define walls
#xmin, xmax, y
HWALLS = np.array([[10, 100, 100],
                     [10, 100, 0.00],
                     [0, 10, 47.5],
                     [0, 10, 52.5]])

#ymin, ymax, x
VWALLS = np.array([[0, 100, 100],
                     [0, 48, 10],
                     [52, 100, 10]])

@nb.njit(fastmath=True)
def dist(pos1, pos2):
    x = np.array(pos1) - np.array(pos2)
    return np.sqrt(x.dot(x))

class GATE_TYPES(Enum):
    exit = "exit"
    entrance = "entrance"

class Agent(object):
    """ Interface class agent"""
    def __init__(self, environment):
        self.pos = (0,0)
        self.environment = environment

    def update_position(self, agents):
        pass

    def timestep(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: pos: {self.pos}"
        __repr__ = __str__