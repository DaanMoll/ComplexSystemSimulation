from Model import *
from Animate import *
import numpy as np
import sys
if __name__ == '__main__':
    print("Simulation started...")
    # density is based on R
    R = 1
    size_agent = np.pi * R**2
    density = 0.1

    max_x=90
    max_y=100


    # Optional CLI argument
    if len(sys.argv) > 1:
        num_agents = int(sys.argv[1])
    else:
        num_agents = int(round(((max_x*max_y)/size_agent) * density))
        print(f"Running simulation with density {density} meaning {num_agents} agents.")

    # num_agen  ts=30
    env = Environment(num_agents=num_agents, max_x=max_x, max_y=max_y)
    print(str(env))
    aniclass = AnimatedScatter(env)
    # plt.show()
    """
    meegeven:
    walls, locaties
    """

    print("Simulation ended")




