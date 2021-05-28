# -*- coding: utf-8 -*-
# Cross compatible version

import math
import json
import sys

#TODO: 🌌 Do orbital mechanics math...

class Body:
    '''does some maths to model orbits'''

    def __init__(self, name, position, velocity, mass, radius):
        self.name = name
        self.pos = position
        self.vel = velocity
        self.mass = mass
        self.rad = radius

    def compute_acceleration(self, x, y):
        '''
            does some maths to find the acceleration of a body. 
            Newton's F=ma and Gravitational Force between two masses.
        '''

        G = 6.67408e-11
        M = self.mass

        dx = self.pos[0] - x
        dy = self.pos[1] - y

        # simple
        # ax = (G * M)/(x**2 + y**2) * (-x)/np.sqrt(x**2 + y**2)
        # ay = (G * M)/(x**2 + y**2) * (-y)/np.sqrt(x**2 + y**2)

        # less simple
        ax = (G * M)/(dx**2 + dy**2) * (dx)/math.sqrt(dx**2 + dy**2)
        ay = (G * M)/(dx**2 + dy**2) * (dy)/math.sqrt(dx**2 + dy**2)

        return ax, ay

    def step(self, dt, body):
        '''
            4th-order Runge-Kutta integrator.
            A method used to solve Ordinary Differential equations.
            More accurate than Euler method.

            In this case it solves:

                :x = Fx / m
                :y = Fy / m

            Otherwise known as the equation of motion of the planet
        '''

        # k1 params
        k1x, k1y = self.vel[0], self.vel[1]
        k1vx, k1vy = body.compute_acceleration(self.pos[0], self.pos[1])

        # k2 params
        k2x = self.vel[0] + (dt/2 * k1vx)
        k2y = self.vel[1] + (dt/2 * k1vy)
        k2vx, k2vy = body.compute_acceleration(self.pos[0] + (dt/2 * k1x), self.pos[1] + (dt/2 * k1y))

        # k3 params
        k3x = self.vel[0] + (dt/2 * k2vx)
        k3y = self.vel[1] + (dt/2 * k2vy)
        k3vx, k3vy = body.compute_acceleration(self.pos[0] + (dt/2 * k2x), self.pos[1] + (dt/2 * k2y))

        # k4 params
        k4x = self.vel[0] + (dt * k3vx)
        k4y = self.vel[1] + (dt * k3vy)
        k4vx, k4vy = body.compute_acceleration(self.pos[0] + (dt * k3x), self.pos[1] + (dt * k3y))

        # calc new pos
        # 'n' at start stands for next in recursive function
        nxn = self.pos[0] + dt/6 * (k1x + 2*k2x + 2*k3x + k4x)
        nyn = self.pos[1] + dt/6 * (k1y + 2*k2y + 2*k3y + k4y)
        self.pos = (nxn, nyn)

        # calc new vel
        nvxn = self.vel[0] + dt/6 * (k1vx + 2*k2vx + 2*k3vx + k4vx)
        nvyn = self.vel[1] + dt/6 * (k1vy + 2*k2vy + 2*k3vy + k4vy)
        self.vel = (nvxn, nvyn)

    # Helper functions

    def __str__(self):
        return '{} | {} {} {} {}'.format(self.name, self.pos, self.vel, self.mass, self.rad)

    def __repr__(self):
        return self.__str__()

def simulate(fn):

    SUN_MASS        = 1.989e30
    SUN_RADIUS      = 695700000.0

    MER_INIT_POS    = (-46000000000.0, 0.0)
    MER_INIT_VEL    = (0.0, -58980.0)
    MER_MASS        = 0.33011e24
    MER_RADIUS      = 2439700.0

    EARTH_INIT_POS  = (-147095000000.0, 0.0)
    EARTH_INIT_VEL  = (0.0, -30300.0)
    EARTH_MASS      = 5.972e24
    EARTH_RADIUS    = 6371000.0

    MARS_INIT_POS   = (-206620000000.0, 0.0)
    MARS_INIT_VEL   = (0.0, -26500.0)
    MARS_MASS       = 6.4171e23
    MARS_RADIUS     = 3389500.0

    steps = 378
    dt = 86400.0 # 1 earth day in seconds

    sun = Body('Sun', (0,0), (0,0), SUN_MASS, SUN_RADIUS)
    mercury = Body('Mercury', MER_INIT_POS, MER_INIT_VEL, MER_MASS, MER_RADIUS)
    earth = Body('Earth', EARTH_INIT_POS, EARTH_INIT_VEL, EARTH_MASS, EARTH_RADIUS)
    mars = Body('Mars', MARS_INIT_POS, MARS_INIT_VEL, MARS_MASS, MARS_RADIUS)

    with open(fn, 'w') as f:

        # add data to json
        content = {}
        content['NUM_BODIES']   = 4
        content['NUM_STEPS']    = steps
        content['NAMES']        = [sun.name, mercury.name, earth.name, mars.name]
        content['COLORS']       = ['orange', 'peru', 'lightseagreen', 'red']
        content['MASSES']       = [sun.mass, mercury.mass, earth.mass, mars.mass]
        content['RADII']        = [sun.rad, mercury.rad, earth.rad, mars.rad]
        content['TRAJECTORIES'] = []

        for x in range(steps):
            content['TRAJECTORIES'].append(
                '{} {} {} '.format(x, sun.pos[0], sun.pos[1])
                + '{} {} '.format(mercury.pos[0], mercury.pos[1])
                + '{} {} '.format(earth.pos[0], earth.pos[1])
                + '{} {} '.format(mars.pos[0], mars.pos[1])
            )
            mercury.step(dt, sun)
            earth.step(dt, sun)
            mars.step(dt, sun)

        f.seek(0)
        json.dump(content, f, indent=4)
        f.truncate()

if __name__ == '__main__':

    fn = 'orbits.json'

    for x in sys.argv:
        if '.json' in x:
            fn = x

    simulate(fn)
