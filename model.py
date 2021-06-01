# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.animation as anime
import json, sys

class PlotTraj:
    '''used to visualize all the data from the simulation'''

    def __init__(self, fn):
        '''reads all the data from json file'''

        with open(fn, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.steps  = self.data['NUM_STEPS']
        self.planets = []

    def _update(self, frame):
        '''updates the position for each frame of the animation'''

        trajectories = self.data['TRAJECTORIES'][frame].split(' ')

        def recursive(idx):
            return 2*idx+1, 2*idx+2

        for idx in range(len(self.planets)):
            x, y = recursive(idx)
            self.planets[idx].set_data(float(trajectories[x]), float(trajectories[y]))

    def animate(self):
        '''plots the planet while it orbits sun'''

        fig, ax = plt.subplots()

        ax.set_xlim(-3e11, 3e11)
        ax.set_ylim(-3e11, 3e11)

        for x in range(self.data['NUM_BODIES']):
            color = self.data['COLORS'][x]
            name = self.data['NAMES'][x]
            radius = 0

            if name == 'Sun':
                radius = 15
            else:
                radius = self.data['RADII'][x]/1e6

            body, = ax.plot(0, 0, 'o-', color=color, markersize=radius)
            self.planets.append(body)

        animation = anime.FuncAnimation(fig, self._update, self.steps, interval=25)

        # Aesthetics
        plt.grid()
        fig.canvas.manager.set_window_title('Big Shaq Quick Maths')

        plt.show()

    def save(self, out, fn='orbits', fps=30):
        fig, ax = plt.subplots()

        ax.set_xlim(-3e11, 3e11)
        ax.set_ylim(-3e11, 3e11)

        for x in range(self.data['NUM_BODIES']):
            color = self.data['COLORS'][x]
            name = self.data['NAMES'][x]
            radius = 0

            if name == 'Sun':
                radius = 15
            else:
                radius = self.data['RADII'][x]/1e6

            body, = ax.plot(0, 0, 'o-', color=color, markersize=radius)
            self.planets.append(body)

        plt.grid()
        ax.set_title('Orbit Simulation')

        if out.lower() == 'gif':
            animation = anime.FuncAnimation(fig, self._update, self.steps, interval=10)
            animation.save(f'{fn}.gif', writer='imagemagick', fps=fps)

        elif out.lower() == 'mp4':
            animation = anime.FuncAnimation(fig, self._update, self.steps, interval=10)
            animation.save(f'{fn}.mp4', writer='ffmpeg', fps=fps)

if __name__ == '__main__':

    fn = 'orbits.json'

    for x in sys.argv:
        if '.json' in x:
            fn = x

    plot = PlotTraj(fn)
    # plot.save('gif', 'orbits', 50)
    plot.animate()
