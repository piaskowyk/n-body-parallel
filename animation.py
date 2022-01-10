import json
import glob
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
#
stars_data = {}
for file_name in glob.glob("simulation_data/*.json"):
    with open(file_name, 'r') as file:
        json_content = json.loads(file.read())
    for star in json_content:
        star_id = '_'.join([str(v) for v in star['id']])
        if star_id not in stars_data:
            stars_data[star_id] = [[], [], []]
        stars_data[star_id][0].append(star['star']['x'])
        stars_data[star_id][1].append(star['star']['y'])
        stars_data[star_id][2].append(star['star']['z'])

def update(num, data, line):
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])

N = 900

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_xlim3d([-100.0, 100.0])
ax.set_xlabel('X')
ax.set_ylim3d([-100.0, 100.0])
ax.set_ylabel('Y')
ax.set_zlim3d([-100.0, 100.0])
ax.set_zlabel('Z')

animations = []
for _, star_data in stars_data.items():
    line, = ax.plot([], [], [])
    animations.append(
        animation.FuncAnimation(
            fig,
            update,
            N,
            fargs=(np.array(star_data), line),
            interval=10000/N,
            blit=False
        )
    )
plt.show()
