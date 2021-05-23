import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json

class PlotTraj:
    def __init__(self, fn):
        with open(fn, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.steps = self.data['NUM_STEPS']

    def _update(self, frame):

        trajectories = self.data['TRAJECTORIES'][frame].split(' ')
        print(trajectories)

        self.sun.set_data(float(trajectories[1]), float(trajectories[2]))
        self.earth.set_data(float(trajectories[3]), float(trajectories[4]))

    def animate(self):
        fig, ax = plt.subplots()

        ax.set_xlim(-200000000000, 200000000000)
        ax.set_ylim(-200000000000, 200000000000)

        self.sun,    = ax.plot(0, 0, 'o-', color='orange', markersize=12)
        self.earth,  = ax.plot(0, 0, 'o-', color='blue')

        animation = FuncAnimation(fig, func=self._update, frames=self.steps, interval=100)
        plt.show()

plot = PlotTraj('sample.json')
plot.animate()