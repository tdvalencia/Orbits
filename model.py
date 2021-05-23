import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json

class PlotTraj:
    def __init__(self, fn):
        '''reads all the data from json file'''
        
        with open(fn, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.steps = self.data['NUM_STEPS']

    def _update(self, frame):
        '''updates the position for each frame of the animation'''

        trajectories = self.data['TRAJECTORIES'][frame].split(' ')
        print(f'{trajectories[0]} | pos: ({trajectories[3]}, {trajectories[4]})')

        self.star.set_data(float(trajectories[1]), float(trajectories[2]))
        self.planet.set_data(float(trajectories[3]), float(trajectories[4]))

    def animate(self):
        '''plots the planet while it orbits sun'''

        fig, ax = plt.subplots()

        ax.set_xlim(-200000000000, 200000000000)
        ax.set_ylim(-200000000000, 200000000000)

        self.star,    = ax.plot(0, 0, 'o-', color='orange', markersize=12)
        self.planet,  = ax.plot(0, 0, 'o-', color='blue')

        animation = FuncAnimation(fig, func=self._update, frames=self.steps, interval=50)

        # Aesthetics
        plt.axis('off')
        fig.canvas.manager.set_window_title('Orbit Simulation')

        plt.show()

if __name__ == '__main__':
    plot = PlotTraj('orbits.json')
    plot.animate()