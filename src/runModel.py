from Model import *
from Animate import *

if __name__ == '__main__':
    print("Simulation started...")
    env = Environment(num_agents=20, num_gates=1, max_x=50, max_y=50)

    aniclass = AnimatedScatter(env)
    plt.show()

    print(str(env))




