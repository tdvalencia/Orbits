import matplotlib.pyplot as plt
import matplotlib.animation as anime
import json

class PlotTraj:
    '''used to visualize all the data from the simulation'''
    
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

        ax.set_xlim(-3e11, 3e11)
        ax.set_ylim(-3e11, 3e11)

        self.star,    = ax.plot(0, 0, 'o-', color='orange', markersize=12)
        self.planet,  = ax.plot(0, 0, 'o-')

        animation = anime.FuncAnimation(fig, self._update, self.steps, interval=25)

        # Aesthetics
        plt.grid()
        fig.canvas.manager.set_window_title('Big Shaq Quick Maths')

        plt.show()

    def save(self, out, fn='orbits', fps=30):
        fig, ax = plt.subplots()

        ax.set_xlim(-3e11, 3e11)
        ax.set_ylim(-3e11, 3e11)

        self.star,    = ax.plot(0, 0, 'o-', color='orange', markersize=12)
        self.planet,  = ax.plot(0, 0, 'o-')

        plt.grid()
        ax.set_title('Orbit Simulation')

        if out.lower() == 'gif':
            animation = anime.FuncAnimation(fig, self._update, self.steps, interval=10)
            animation.save(f'docs/{fn}.gif', writer='imagemagick', fps=fps) 
        
        elif out.lower() == 'mp4':
            animation = anime.FuncAnimation(fig, self._update, self.steps, interval=10)
            animation.save(f'docs/{fn}.mp4', writer='ffmpeg', fps=fps)        

if __name__ == '__main__':
    plot = PlotTraj('orbits.json')
    # plot.save('gif', 'zoom', 50)
    plot.animate()
