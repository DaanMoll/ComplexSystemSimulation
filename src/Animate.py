import matplotlib.pyplot as plt
from matplotlib import animation, rc
import numpy as np

class AnimatedScatter(object):
    def __init__(self, env):
        self.env = env
        self.stream = self.data_stream()

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=20,
                                          init_func=self.setup_plot, blit=True)
        self.ani.to_html5_video()

    def setup_plot(self):
        x = [x[0] for x in self.env.poslist]
        y = [x[1] for x in self.env.poslist]

        self.scat = self.ax.scatter(x,y)
        self.ax.axis([0, 100, 0, 100])

        #TODO not hardcodded but i dunno
        self.ax.vlines(0, 0, 48, linewidth=4, color='b')
        self.ax.vlines(0, 52, 100, linewidth=4, color='b')
        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,

    def data_stream(self):
        while True:
            self.env.timestep(True)
            yield self.env.poslist

    def update(self, i):
        """Update the scatter plot."""
        data = next(self.stream)
        # print(data)
        # Set x and y data...
        self.scat.set_offsets(data)
        return self.scat,