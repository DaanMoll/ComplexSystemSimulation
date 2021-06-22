from Model import *
from Simulation import Simulation
import numpy as np
import sys
import argparse
from constant import R


if __name__ == '__main__':
    # density is based on R
    size_agent = np.pi * R**2
    max_x=100
    min_x=10
    max_y=100
    min_y=0
    animate = True

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_agents", help="Set the number of agents", type=int)
    parser.add_argument("-l", "--logging", help="Enable logging", action="store_true")
    parser.add_argument("-a", "--no_animation", help="Disable animation (default ON)", action="store_true")
    parser.add_argument("-r", "--run_name", help="Enter a name for this run, to save the logging file (optional)", type=str)
    args = parser.parse_args()
    if args.no_animation:
        animate = False
    print(f"Simulation started... \
    \n\t Name: {args.run_name}\
    \n\t Animate: {animate}")


    density = 0.1
    attr_forces = np.linspace(10, 20, 24)
    num_agents = int(round((((max_x-min_x)*(max_y-min_y))/size_agent) * density))
    # print(f"Running simulation with density {density} meaning {num_agents} agents.")

    for attr_force in attr_forces:
        attr_force = round(attr_force, 2)
        for i in range(1):
            env = Environment(num_agents=num_agents, max_x=max_x, min_x=min_x, max_y=max_y, min_y=min_y, attr_force = attr_force)
            name = f"HUMAN_ATTR_FORCE_{attr_force}_density0.1"
            aniclass = Simulation(env, logging=args.logging, name=name, animate = animate)
            exit()

    # aniclass = Simulation(env, logging=args.logging, name=args.run_name, animate = animate)

    print("Simulation ended")






