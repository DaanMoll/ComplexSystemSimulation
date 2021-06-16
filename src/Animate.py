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

        self.scat = self.ax.scatter(x[:-1],y[:-1], 'b', x[-1], y[-1], 'r')
        self.ax.axis([0, 100, 0, 100])

        #TODO not hardcodded but i dunno
        self.ax.vlines(0, 0, 49, linewidth=4, color='b')
        self.ax.vlines(0, 51, 100, linewidth=4, color='b')

        if self.env.num_gates == 2:
            self.ax.vlines(self.env.max_x, 0, 49, linewidth=4, color='b')
            self.ax.vlines(self.env.max_x, 51, 100, linewidth=4, color='b')

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
        print(data)
        # print(data)
        # Set x and y data...
        # self.scat.set_offsets(data[:-1], 'b', data[-1], 'r')
        self.scat.set_offsets(data)
        return self.scat,