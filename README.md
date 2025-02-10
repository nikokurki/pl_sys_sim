# Simple Planetary System Simulator

A simple planetary system simulator using Velocity Verlet and Newton's law of universal gravitation. The objects are inputted using a file (in this case .csv, but the type does not really matter), and it is run using command line instructions. The simulation uses 600 second timestep, and its default configuration (data.csv) initializes only the first five planets of Solar System. Due to the vast distance of outer planets, it would make the inner planets' orbits too small to visualize, and also way too resource demanding because of the long orbital periods. Python is not really suitable for these types of simulations due to the fact that the running time increases very fast the more objects we have. One could improve this code by
simply writing it in C++ and then utilizing parallelization to do calculations for objects separately.


You can run the code using: python system.py data_file number_of_iterations (for example, doing 1.9 years of calculations would require N = 100 000).

Here are some visualization done using the code:

![innerplanets](https://github.com/user-attachments/assets/31866bd7-9638-4dbf-bab9-966bd86f5896)


Even though the math behind this simulation is very simple, one can still visualize interesting things like how Jupiter forces the Sun to wobble. The barycenter for Jupiter and Sun is outside the Sun's surface and it can be seen below (the size of the Sun in this is actually very close to its real size).


![sun_movement](https://github.com/user-attachments/assets/13300f4a-b1c9-4d9d-839b-b4fe45ef3165)

