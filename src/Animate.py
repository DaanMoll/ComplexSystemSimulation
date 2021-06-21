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
                                          init_func=self.setup_plot, blit=True, save_count=20)
        # put save count on 2k if we want to save
        self.ani.save("data/test.mp4")

    def setup_plot(self):
        x = [x[0] for x in self.env.poslist]
        y = [x[1] for x in self.env.poslist]
        c = [0 for _ in range(len(x))]
        c[-1] = 1

        # self.scat = self.ax.scatter(x[:-1],y[:-1], 'b', x[-1], y[-1], 'r')
        # self.ax.set_title(f"hoi {self.env.num_agents}")
        self.title = self.ax.text(0.5,0.85, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5},
                transform=self.ax.transAxes, ha="center")

        self.scat = self.ax.scatter(x[:-1], y[:-1], c=c[:-1], cmap='winter',  s = 500)
        self.ax.scatter(x[-1], y[-1], c=c[-1], marker='s', cmap='winter', s = 100)
        # self.scat(x[-1], y[-1], 'b')
        self.ax.axis([5, 100, 0, 100])

        #TODO not hardcodded but i dunno
        self.ax.vlines(100, 0, 100, linewidth=4, color='black')
        self.ax.vlines(10, 0, 46, linewidth=4, color='black')
        self.ax.vlines(10, 54, 100, linewidth=4, color='black')
        
        self.ax.hlines(0, 10, 100, linewidth=4, color='black')
        self.ax.hlines(100, 10, 100, linewidth=4, color='black')
        self.ax.hlines(45, 0, 10, linewidth=4, color='black')
        self.ax.hlines(55, 0, 10, linewidth=4, color='black')

        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,

    def data_stream(self):
        while True:
            # self.ax.set_title(f"hoi {self.env.num_agents}")
            self.env.timestep(True)
            yield self.env.poslist

    def update(self, i):
        """Update the scatter plot."""
        
        data = next(self.stream)
        # self.ax.text(0.5,0.85, "hoi", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, transform=self.ax.transAxes, ha="center")
        self.title.set_text(f"Agents = {self.env.num_agents}")
        # print(self.env.num_agents)
        
        # c = [5 for _ in range(len(data))]
        # c[-1] = 2

        self.scat.set_offsets(data[:-1])
        # self.scat.set_array(np.array(c))
        return self.scat, self.title,