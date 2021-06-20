import matplotlib.pyplot as plt
from matplotlib import animation, rc
import numpy as np
from Utils import HWALLS, VWALLS
from Logger import Logger
from constant import LOGGING_PATH
import os
import math
from extended_int import int_inf

# Based on https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot
class Simulation(object):
    def __init__(self, env, logging=False, name=None, animate=True):
        self.logger = None
        if logging:
            if not os.path.exists(LOGGING_PATH):
                os.mkdir(LOGGING_PATH)
            self.logger = Logger(LOGGING_PATH, filename=name)
            print(f"Logging enabled for file: {self.logger.filename}")

        self.env = env
        self.stream = self.data_stream()

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots(figsize=(32, 32))
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=20,
                                          init_func=self.setup_plot, blit=True, save_count=20)
        # put save count on 2k if we want to save
        if animate:
            self.ani.save("../../test2.mp4")

    def setup_plot(self):
        x = [x[0] for x in self.env.poslist]
        y = [x[1] for x in self.env.poslist]

        self.title = self.ax.text(0.02, 0.95, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5},
                transform=self.ax.transAxes, ha="center", fontsize="large")

        # Define
        self.scat = self.ax.scatter(x[:-1], y[:-1], s = 500)
        self.ax.axis([0, 101, -1, 101])
        self.ax.axis("off")

        for a, b, c in HWALLS:
            self.ax.hlines(c, a, b,linewidth=4, color='black')

        for a, b, c in VWALLS:
            self.ax.vlines(c, a, b,linewidth=4, color='black')

        return self.scat,

    def data_stream(self):
        # TODO might be better to just return the positions
        while True:
            self.env.timestep(True)
            if self.logger != None:
                self.logger.save_position_step(self.env.poslist)
            yield self.env.poslist

    def update(self, i):
        """Update the scatter plot."""

        data = next(self.stream)
        self.title.set_text(f"Agents = {self.env.num_agents}")

        self.scat.set_offsets(data[:-2])
        return self.scat, self.title,