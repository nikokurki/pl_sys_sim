import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys

dt = 600
AU = 149597870691

def main():
    N = int(sys.argv[1])
    df = pd.read_csv("cppdata.csv")
    animate(N, df)


def animate(N: int, df: pd.DataFrame):


    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.set_xlim(-40, 40)  
    ax.set_ylim(-40, 40)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title("Solar System Simulation")
    ax.set_xlabel("AU")
    ax.set_ylabel("AU")
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    object_names = df["name"].unique()
    scatters = {}
    trails = {}
    years_per_step = N*dt/(2000 * 86400 * 365)

    for name in object_names:
        obj_data = df[df["name"] == name]
        color = obj_data["color"].iloc[0]
        s = 40 if name == "Sun" else 5
        scatters[name] = ax.scatter([], [], s=s, color=color, label=name)
        trails[name], = ax.plot([], [], color=color, linewidth=0.5)

    ax.legend(loc="upper right", facecolor="black", edgecolor="white", labelcolor="white", prop={'size': 7})

    def update(frame):
        for name in object_names:
            obj_data = df[df["name"] == name]
            if frame < len(obj_data): 
                x = obj_data["x"].iloc[:frame].to_numpy() / AU
                y = obj_data["y"].iloc[:frame].to_numpy() / AU
                if len(x) > 0 and len(y) > 0:
                    trails[name].set_data(x, y)
                    scatters[name].set_offsets([[x[-1], y[-1]]])

        elapsed_years = frame * years_per_step
        time_text.set_text(f'Year: {elapsed_years:.1f}')

        return [*scatters.values(), *trails.values()] + [time_text]

    ani = FuncAnimation(fig, update, frames=2000, interval=5, blit=True)
    #ani.save("system.gif", writer='imagemagick', fps=120)
    plt.show()


if __name__ == "__main__":
    main()
