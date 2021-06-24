from Model import *
from Simulation import Simulation
import numpy as np
import sys
import argparse
from constant import R

"""
File to run the actual model.

usage: run.py [-h] [-n NUM_AGENTS] [-l] [-a] [-s] [-r R]

Crowd simulation model during evacuation.

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_AGENTS, --num_agents NUM_AGENTS
                        Set the number of agents
  -l, --logging         Enable logging
  -a, --animation       Enable storing an animation
  -s, --show_animation  Show animation during run (this enables --animation)
  -r R, -run_name R     Enter a name for this run, to save the logging file


"""


if __name__ == '__main__':
    # density is based on R
    size_agent = np.pi * R**2
    density = 0.1

    max_x=100
    min_x=10
    max_y=100
    min_y=0
    animate = True

    parser = argparse.ArgumentParser(description = "Crowd simulation model during evacuation.")
    parser.add_argument("-n", "--num_agents", help="Set the number of agents", type=int)
    parser.add_argument("-l", "--logging", help="Enable logging", action="store_true")
    parser.add_argument("-a", "--animation", help="Enable storing an animation", action="store_true")
    parser.add_argument("-s", "--show_animation", help="Show animation during run (this enables --animation)", action="store_true")
    parser.add_argument("-r", "-run_name", help="Enter a name for this run, to save the logging file", type=str)
    args = parser.parse_args()

    animate = args.animation
    show_animation = args.show_animation
    if show_animation:
        animate = True

    print(f"Simulation started... \
    \n\t Name: {args.run_name}\
    \n\t Animate: {animate}")

    # Optional CLI argument for num_agents
    if args.num_agents:
        num_agents = args.num_agents
    else:
        num_agents = int(round((((max_x-min_x)*(max_y-min_y))/size_agent) * density))
        print(f"Running simulation with density {density} meaning {num_agents} agents.")

    # num_agents=30
    env = Environment(num_agents=num_agents, max_x=max_x, min_x=min_x, max_y=max_y, min_y=min_y)
    print(str(env))
    aniclass = Simulation(env, logging=args.logging, name=args.run_name, animate = animate, show_animation = show_animation)

    print("Simulation ended")
