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

    # Optional CLI argument for num_agents

    # num_agents=30

    CLOSE_DISTANCES = np.linspace(int(2*R), int(10*R), 40)
    print(CLOSE_DISTANCES)
    density = 0.1
    density = round(density, 2)
    num_agents = int(round((((max_x-min_x)*(max_y-min_y))/size_agent) * density))

    for CLOSE_DISTANCE in CLOSE_DISTANCES:
        for i in range(10):
            print(f"CLOSE_DISTANCE2 = {CLOSE_DISTANCE:4f} run no. {i}")
            env = Environment(num_agents=num_agents, max_x=max_x, min_x=min_x, max_y=max_y, min_y=min_y, CLOSE_DISTANCE=CLOSE_DISTANCE)
            name = f"CLOSE_DISTANCE2_{CLOSE_DISTANCE:4f}_{i}"
            aniclass = Simulation(env, logging=args.logging, name=name, animate = animate)

    # aniclass = Simulation(env, logging=args.logging, name=args.run_name, animate = animate)

    print("Simulation ended")




