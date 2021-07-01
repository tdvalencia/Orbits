import requests
import json

content = {}
content['NUM_BODIES']   = 3
content['NUM_STEPS']    = 378
content['NAMES']	= ['sun', 'mercury', 'earth']
content['COLORS']   = ['orange', 'peru', 'lightseagreen']
content['DIST']		= [0.0, -46000000000.0, -147095000000.0]
content['VEL']		= [0.0, -58980.0, -30300.0]
content['MASSES']	= [1.989e30, 0.33011e24, 5.972e24]
content['RADII']	= [695700000.0, 2439700.0, 6371000.0]
content['TRAJECTORIES'] = []

def make_file(res):
    print(res)
    with open('orbits.json', 'w', encoding='utf-8') as f:
        json.dump(res.json(), f, indent=4)

def print_json(res):
    print(res.json())

res = requests.post('http://localhost:5000/watermelon', json=content)
if res.ok:
    make_file(res)
