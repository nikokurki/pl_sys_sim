# Simple Planetary System Simulator
## Python vs C++
### Python version
A simple planetary system simulator using Velocity Verlet and Newton's law of universal gravitation. In Python version (system.py) the objects are inputted using a file (in this case .csv with semicolon separation), and it is run using command line instructions. The simulation uses 600 second timestep, and its default configuration (data.csv) initializes only the first five planets of Solar System. Running time increases very fast if one were to calculate enough steps required for outer planets.  Python is not really suitable for these types of simulations due to the fact that the running time increases very fast the more objects we have. One could improve this code by
simply writing it in C++ (like below).

You can run the code using: python system.py data_file number_of_iterations (for example, doing 1.9 years of calculations would require N = 100 000).

Here are some visualization done using the code:

![innerplanets](https://github.com/user-attachments/assets/31866bd7-9638-4dbf-bab9-966bd86f5896)


Even though the math behind this simulation is very simple, one can still visualize interesting things like how Jupiter forces the Sun to wobble. The barycenter for Jupiter and Sun is outside the Sun's surface and it can be seen below (the size of the Sun in this is actually very close to its real size).


![sun_movement](https://github.com/user-attachments/assets/13300f4a-b1c9-4d9d-839b-b4fe45ef3165)

### C++ version

C++ version is run by compiling planetsystem.cpp using: g++ planetsystem.cpp -o sim.exe. 

Unlike the python version, the C++ version does not retrieve data via a .csv file, but the data of the planets is already included in the code. Due to the massive performance increase (~110x), you can easily calculate millions of iterations for all planets fast. 
The code also requires visualize.py, which is automatically run inside planetsystem.cpp.

You can run the code using: ./sim.exe number_of_iterations (N = 10 000 000 is enough to make Neptune do full orbit).


![all](https://github.com/user-attachments/assets/ca04dfcd-caaa-496f-a643-74bb3a1e31c8)
