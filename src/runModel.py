from Model import *
from Animate import *
import numpy as np

if __name__ == '__main__':
    print("Simulation started...")
    
    # density is based on R
    R = 1
    size_agent = np.pi * R**2
    density = 0.1

    max_x=100
    max_y=100

    num_agents = int(round(((max_x*max_y)/size_agent) * density))
    print(num_agents)

    num_agents=50
    env = Environment(num_agents=num_agents, num_gates=1, max_x=max_x, max_y=max_y)
    print(str(env))
    aniclass = AnimatedScatter(env)
    plt.show()
    """
    meegeven:
    walls, locaties
    """

    print("klaar")




