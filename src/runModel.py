from Model import *
from Animate import *
import numpy as np

if __name__ == '__main__':
    print("Simulation started...")
    
    # density is based on R
    R = 0.5
    size_agent = np.pi * R**2
    density = 0.01

    max_x=100
    max_y=100

    num_agents = int(round(max_x*max_y * density))
    print(num_agents)


    env = Environment(num_agents=num_agents, num_gates=1, max_x=max_x, max_y=max_y)
    print(str(env))
    aniclass = AnimatedScatter(env)
    plt.show()

    print("klaar")




