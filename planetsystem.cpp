#include <iostream>
#include <array>
#include <string>
#include <cmath>
#include <vector>
#include <chrono>
#include <fstream>
#include <cstdlib>

const double G = 6.674E-11;
const double dt = 600;

class Object {
public:
	std::string name;
	std::string color;
	double mass;
	int index;
	std::array<double, 2> pos;
	std::array<double, 2> vel;
	std::array<double, 2> acc;
	std::array<double, 2000> xs = {};
	std::array<double, 2000> ys = {};

	Object(const std::string& name, const std::string& color, double mass, int index,
		const std::array<double, 2>& pos, const std::array<double, 2>& vel, const std::array<double, 2>& acc)
		: name(name), color(color), mass(mass), index(index), pos(pos), vel(vel), acc(acc) {}


};

void saveData(const int N, const std::vector<Object>& objects, const std::string& filename) {
	std::ofstream file(filename);
	if (!file.is_open()) {
		std::cerr << "Error: Could not open file.\n";
		return;
	}
	file << "name,color,x,y\n";
	for (const Object& obj : objects) {
		for (int i = 0; i < obj.xs.size(); ++i) {
			file << obj.name << "," << obj.color << "," << obj.xs[i] << "," << obj.ys[i] << "\n";

		}
	}
	file.close();
	std::cout << "Simulation data saved to " << filename << std::endl;

}

std::array<double, 2> barycenter(const std::vector<Object>& objects) {
	double total_mass = 0.0;
	std::array<double, 2> center = { 0.0, 0.0 };

	for (const Object& obj : objects) {
		total_mass += obj.mass;
		center[0] += obj.mass * obj.pos[0];
		center[1] += obj.mass * obj.pos[1];

	}

	center[0] /= total_mass;
	center[1] /= total_mass;

	return center;
}

std::array<double, 2> vel_barycenter(const std::vector<Object>& objects) {
	double total_mass = 0.0;
	std::array<double, 2> velocity = { 0.0, 0.0 };

	for (const Object& obj : objects) {
		total_mass += obj.mass;
		velocity[0] += obj.mass * obj.vel[0];
		velocity[1] += obj.mass * obj.vel[1];

	}

	velocity[0] /= total_mass;
	velocity[1] /= total_mass;

	return velocity;
}

std::array<double, 2> acceleration(const Object& current_object, const std::vector<Object>& objects) {
	std::array<double, 2> net_force = { 0.0, 0.0 };

	for (const Object& obj : objects) {
		if (obj.name != current_object.name) {
			std::array<double, 2> r_vec = { obj.pos[0] - current_object.pos[0], obj.pos[1] - current_object.pos[1] };
			double distance_sq = r_vec[0] * r_vec[0] + r_vec[1] * r_vec[1];
			double distance = std::sqrt(distance_sq);
			double force_mag = -G * current_object.mass * obj.mass / (distance_sq * distance);

			net_force[0] += force_mag * r_vec[0];
			net_force[1] += force_mag * r_vec[1];
		}
	}

	return { -net_force[0] / current_object.mass, -net_force[1] / current_object.mass };
}
void simulate(int N, std::vector<Object>& objects) {

	std::array<double, 2> barycenter_pos = barycenter(objects);
	std::array<double, 2> barycenter_vel = vel_barycenter(objects);

	for (Object& obj : objects) {
		obj.pos[0] -= barycenter_pos[0];
		obj.pos[1] -= barycenter_pos[1];
		obj.vel[0] -= barycenter_vel[0];
		obj.vel[1] -= barycenter_vel[1];

	}

	for (Object& obj : objects) {
		obj.acc = acceleration(obj, objects);

	}

	for (int i = 0; i < N; ++i) {
		for (Object& obj : objects) {
			obj.pos[0] += obj.vel[0] * dt + 0.5 * obj.acc[0] * dt * dt;
			obj.pos[1] += obj.vel[1] * dt + 0.5 * obj.acc[1] * dt * dt;

			std::array<double, 2> new_acc = acceleration(obj, objects);

			obj.vel[0] += 0.5 * (obj.acc[0] + new_acc[0]) * dt;
			obj.vel[1] += 0.5 * (obj.acc[1] + new_acc[1]) * dt;
			obj.acc = new_acc;

			if (i % (N / 2000) == 0) {
				obj.xs[obj.index] = obj.pos[0];
				obj.ys[obj.index] = obj.pos[1];
				obj.index++;

			}
		}

		if (i % (N / 10) == 0) {
			std::cout << "Simulation progress: " << (i * 100) / N << "%\n";
		}
	}

}

int main(int argc, char *argv[]) {

	int N = atoi(argv[1]);

	std::vector<Object> objects = {
		{"Sun", "yellow", 1.989e30, 0, {0.0, 0.0}, {0.0, 0.0}, {0.0, 0.0}},
		{"Mercury", "grey", 3.301e23, 0, {5.791e10, 0.0}, {0.0, 47870}, {0.0, 0.0}},
		{"Venus", "orange", 4.867e24, 0, {1.082e11, 0.0}, {0.0, 35020}, {0.0, 0.0}},
		{"Earth", "deepskyblue", 5.972e24, 0, {1.496e11, 0.0}, {0.0, 29780}, {0.0, 0.0}},
		{"Mars", "red", 6.419e23, 0, {2.279e11, 0.0}, {0.0, 24077}, {0.0, 0.0}},
		{"Jupiter", "brown", 1.898e27, 0, {7.785e11, 0.0}, {0.0, 13060}, {0.0, 0.0}},
		{"Saturn", "beige", 5.684e26, 0, {1.433e12, 0.0}, {0.0, 9680}, {0.0, 0.0}},
		{"Uranus", "aqua", 8.681e25, 0, {2.871e12, 0.0}, {0.0, 6800}, {0.0, 0.0}},
		{"Neptune", "royalblue", 1.024e26, 0, {4.5e12, 0.0}, {0.0, 5430}, {0.0, 0.0}}


	};
	auto start = std::chrono::high_resolution_clock::now();
	simulate(N, objects);
	auto end = std::chrono::high_resolution_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
	std::cout << "Simulation took: " << duration.count() << " ms using N = " << N << std::endl;

	saveData(N, objects, "cppdata.csv");

	std::cout << "Running Python script visualize.py\n"; 
	std::string pythonScript = "visualize.py";
	std::string command = "python " + pythonScript + " " + std::to_string(N);
	int result = system(command.c_str()); 
    if (result != 0) {
        std::cerr << "Error running Python script\n";
    }
    return 0;


}


