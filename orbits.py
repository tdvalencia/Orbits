import numpy as np
import json

#TODO: Do orbital mechanics math...

class Body:
    def __init__(self, name, position, velocity, mass, radius):
        self.name = name
        self.pos = position
        self.vel = velocity
        self.mass = mass
        self.rad = radius

    def compute_acceleration(self, x, y):
        '''does some maths to find the acceleration of a body. Newton's F=ma and Gravitational Force between two bodies.'''

        G = 6.67408 * (10**-11)
        m = self.mass

        dx = x - self.pos[0]
        dy = y - self.pos[1]

        # simple
        # ax = (G * m)/(dx**2 + dy**2) * (-x)/np.sqrt(dx**2 + dy**2)
        # ay = (G * m)/(dx**2 + dy**2) * (-y)/np.sqrt(dx**2 + dy**2)

        # less simple
        ax = (G * m)/(dx**2 + dy**2) * -(dx)/np.sqrt(dx**2 + dy**2)
        ay = (G * m)/(dx**2 + dy**2) * -(dy)/np.sqrt(dx**2 + dy**2)

        return ax, ay

    def step(self, dt, body):
        '''4th-order Runge-Kutta integrator. <<< idk what this means'''

        # k1 params
        k1x, k1y = self.vel[0], self.vel[1]
        k1vx, k1vy = body.compute_acceleration(self.pos[0], self.pos[1])

        # k2 params
        k2x = self.vel[0]  + (dt/2 * k1vx)
        k2y = self.vel[1] + (dt/2 * k1vy)
        k2vx, k2vy = body.compute_acceleration(self.pos[0] + (dt/2 * k1x), self.pos[1] + (dt/2 * k1y))

        # k3 params
        k3x = self.vel[0] + (dt/2 * k2vx)
        k3y = self.vel[1] + (dt/2 * k2vy)
        k3vx, k3vy = body.compute_acceleration(self.pos[0] + (dt/2 * k2x), self.pos[1] + (dt/2 * k2y))

        # k4 params
        k4x = self.vel[0] + (dt/2 * k3vx)
        k4y = self.vel[1] + (dt/2 * k3vy)
        k4vx, k4vy = body.compute_acceleration(self.pos[0] + (dt/2 * k3x), self.pos[1] + (dt/2 * k3y))

        # calc new pos
        xn = self.pos[0] + dt/6 * (k1x + 2*k2x + 2*k3x + k4x)
        yn = self.pos[1] + dt/6 * (k1y + 2*k2y + 2*k3y + k4y)
        self.pos = (xn, yn)

        #calc new vel
        vxn = self.vel[0] + dt/6 * (k1vx + 2*k2vx + 2*k3vx + k4vx)
        vyn = self.vel[1] + dt/6 * (k1vy + 2*k2vy + 2*k3vy + k4vy)
        self.vel = (vxn, vyn)


def example1():
    SUN_MASS = 1.989e30
    SUN_RADIUS = 695700000.0

    sun = Body('Sun', (0,0), (0,0), SUN_MASS, SUN_RADIUS)

    ax, ay = sun.compute_acceleration(1000000000.0, 500000000.0)

    print(f'ax: {ax}')
    print(f'ay: {ay}')

def example2():
    SUN_MASS        = 1.989e30
    SUN_RADIUS      = 695700000.0

    EARTH_INIT_POS  = (-147095000000.0, 0.0)
    EARTH_INIT_VEL  = (0.0, -30300.0)
    EARTH_MASS      = 5.972e24
    EARTH_RADIUS    = 6371000.0

    dt = 86400.0 # earth day in seconds

    sun = Body('Sun', (0,0), (0,0), SUN_MASS, SUN_RADIUS)
    earth = Body('Earth', EARTH_INIT_POS, EARTH_INIT_VEL, EARTH_MASS, EARTH_RADIUS)

    earth.step(dt, sun)

    print(f'pos: {earth.pos}')
    print(f'vel: {earth.vel}')

def simulate():

    SUN_MASS        = 1.989e30
    SUN_RADIUS      = 695700000.0

    EARTH_INIT_POS  = (-147095000000.0, 0.0)
    EARTH_INIT_VEL  = (0.0, -30300.0)
    EARTH_MASS      = 5.972e24
    EARTH_RADIUS    = 6371000.0

    steps = 368
    dt = 86400.0 # earth day in seconds

    sun = Body('Sun', (0,0), (0,0), SUN_MASS, SUN_RADIUS)
    earth = Body('Earth', EARTH_INIT_POS, EARTH_INIT_VEL, EARTH_MASS, EARTH_RADIUS)

    print(f'0 | init_pos: {EARTH_INIT_POS}, init_vel: {EARTH_INIT_VEL}')

    with open('orbits.json', 'w', encoding='utf-8') as f:

        # add data to json
        content = {}
        content['NUM_BODIES']   = 2
        content['NUM_STEPS']    = steps
        content['NAMES']        = [sun.name, earth.name]
        content['MASSES']       = [sun.mass, earth.mass]
        content['RADII']        = [sun.rad, earth.rad]
        content['TRAJECTORIES'] = []

        for x in range(steps):
            earth.step(dt, sun)
            print(f'{x} | pos: {earth.pos}, vel: {earth.vel}')
            content['TRAJECTORIES'].append(f'{x} {sun.pos[0]} {sun.pos[1]} {earth.pos[0]} {earth.pos[1]}')

        f.seek(0)
        json.dump(content, f, indent=4)
        f.truncate()

if __name__ == '__main__':
    simulate()