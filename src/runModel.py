from Model import *
from Animate import *

if __name__ == '__main__':
    print("Simulation started...")
    env = Environment(num_agents=50, num_gates=1, max_x=100, max_y=100)
    print(str(env))
    aniclass = AnimatedScatter(env)
    plt.show()




