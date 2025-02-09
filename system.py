import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import sys


AU = 149597870691

dt = 600

class Object:

    def __init__(self, name: str, color: str, mass: float, pos: tuple, vel: tuple, acc: tuple):
        self.name = name
        self.mass = mass
        self.color = color
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.acc = np.array(acc, dtype=float)

        self.xs = []
        self.ys = []


def main():

    filename = sys.argv[1]
    N = int(sys.argv[2])
    objects, limit = read_data(filename)

    start = time.time()
    simulate(N, dt, objects)
    end = time.time()

    print(f"Took {(end-start):.2f} seconds to simulate using N = {N}")
    
    animate(N, objects, limit)

def read_data(file):
    limit = 0.0
    objects = []
    with open(file, 'r') as f:
        next(f)
        for line in f:
           data = line.split(";")
           name = data[0]
           color = data[1]
           mass = float(data[2])
           if max(float(data[3]), float(data[4])) > limit:
               # Makes sure the plot is big enough to visualize all planets
               limit = max(float(data[3]), float(data[4])) * 1.5
           position = (float(data[3])*AU, float(data[4])*AU)
           velocity = (float(data[5]), float(data[6]))
           # Acceleration is initialized at the start of the simulation
           acceleration = (0.0,0.0)
           obj = Object(name, color, mass, position, velocity, acceleration)
           objects.append(obj)
    return objects, limit
 

def simulate(N: int, dt: float, objects: object):

    barycenter_pos = barycenter(objects)
    barycenter_vel = vel_barycenter(objects)

    for object in objects:
        object.pos -= barycenter_pos
        object.vel -= barycenter_vel

    # Initial acceleration
    for object in objects:
        object.acc = acceleration(object, objects)

    # Velocity Verlet
    for i in range(N):
        for object in objects:
            object.pos += object.vel*dt+0.5*object.acc*dt*dt
            new_acc = acceleration(object, objects)
            object.vel += 0.5*(object.acc + new_acc)*dt
            object.acc = new_acc

            # Saves 1000 frames of data
            if i % (N/1000) == 0:
                object.xs.append(object.pos[0])
                object.ys.append(object.pos[1])

        if i%(N/10) == 0:
            print(f"Simulation progress: {i/N*100:.0f} %")

 
   
def acceleration(current_object: object, objects: object):

    G = 6.674E-11
    net_force = np.array([0.0,0.0])
    for object in objects:
        if object.name != current_object.name:
            r_vec = object.pos - current_object.pos
            distance_sq = np.dot(r_vec, r_vec)
            distance = np.sqrt(distance_sq)
            force_mag = -G * current_object.mass * object.mass / (distance_sq * distance)
            net_force += force_mag * r_vec
 
 
    return -net_force/current_object.mass


def barycenter(objects: object):

    tot_mass = sum(obj.mass for obj in objects)
    center = sum(obj.mass * obj.pos for obj in objects)/tot_mass
    return center


def vel_barycenter(objects: object):

    tot_mass = sum(obj.mass for obj in objects)
    vel = sum(obj.mass * obj.vel for obj in objects)/tot_mass
    return vel


def animate(N: int, objects: object, limit: float):

    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.set_xlim(-limit, limit)  
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title("Solar System Simulation")
    ax.set_xlabel("AU")
    ax.set_ylabel("AU")
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    scatters = {}
    trails = {}
    years_per_step = N*dt/(1000 * 86400 * 365)
    for object in objects:
        color = object.color
        s = 40 if object.name == "Sun" else 5
        scatters[object.name] = ax.scatter([], [], s=s, color=color, label=object.name)
        trails[object.name], = ax.plot([], [], color=color, linewidth=0.5)

    ax.legend(loc="upper right", facecolor="black", edgecolor="white", labelcolor="white", prop={'size': 7})

    def update(frame):
        for obj in objects:
            if frame < len(obj.xs): 
                x = np.array(obj.xs[:frame]) / AU
                y = np.array(obj.ys[:frame]) / AU
                if len(x) > 0 and len(y) > 0:
                    trails[obj.name].set_data(x, y)

                    scatters[obj.name].set_offsets([[x[-1], y[-1]]])
        elapsed_years = frame * years_per_step
        time_text.set_text(f'Year: {elapsed_years:.1f}')

        return [*scatters.values(), *trails.values()] + [time_text]

    ani = FuncAnimation(fig, update, frames=len(objects[0].xs), interval=10, blit=True)
    # Saves the animation as gif, is very resource demanding and requires imagemagick
    #ani.save("system.gif", writer='imagemagick', fps=60)
    plt.show()


if __name__ == "__main__":
    main()