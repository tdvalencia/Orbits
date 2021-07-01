from flask import *
from orbits import Body
import numpy as np

app = Flask(__name__, static_folder='')

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/simulate')
def visual():
    return render_template('simulate.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/watermelon', methods=['GET', 'POST'])
def confirm():
    data = request.get_json()
    content = trajectories(data)
    return jsonify(content)

def parse(data):
    arr = []
    for x in range(data['NUM_BODIES']):
        arr.append(
            Body(
                data['NAMES'][x], (data['DIST'][x], 0.0), 
                (0.0, data['VEL'][x]), data['MASSES'][x], data['RADII'][x]
            )
        )
    return arr

def trajectories(data):

    dt = 86400.0
    bodies = parse(data)

    content = {}
    content['NUM_BODIES']   = data['NUM_BODIES']
    content['NUM_STEPS']    = data['NUM_STEPS']
    content['NAMES']        = data['NAMES']
    content['COLORS']       = data['COLORS']
    content['MASSES']       = data['MASSES']
    content['RADII']        = data['RADII']
    content['TRAJECTORIES'] = []

    for x in range(data['NUM_STEPS']):
        step = f'{x} '

        for body in bodies:
            copy = bodies.copy()
            copy.remove(body)
            body.step(dt, copy)
            step += f'{body.pos[0]} {body.pos[1]} '

        content['TRAJECTORIES'].append(step)
    return content

if __name__ == '__main__':
    app.run()