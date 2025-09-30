import numpy as np
import json
from data.constants import *
from scipy.integrate import solve_ivp


class CelestialBody:
    def __init__(self, name, mass, radius, color, body_type):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.color = color
        self.type = body_type
        self.position = np.zeros(3)
        self.velocity = np.zeros(3)
        self.orbit_history = []

    def set_orbital_parameters(self, semi_major_axis, eccentricity, orbital_period):
        """Set initial orbital parameters"""
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.orbital_period = orbital_period

        # Calculate initial position and velocity (simplified circular orbit)
        orbital_speed = np.sqrt(G * SOLAR_MASS / semi_major_axis)
        self.position = np.array([semi_major_axis, 0, 0])
        self.velocity = np.array([0, orbital_speed, 0])

    def gravitational_force(self, other_body):
        """Calculate gravitational force between two bodies"""
        r_vec = other_body.position - self.position
        r_mag = np.linalg.norm(r_vec)

        if r_mag == 0:
            return np.zeros(3)

        force_mag = G * self.mass * other_body.mass / (r_mag ** 2)
        force_vec = force_mag * r_vec / r_mag

        return force_vec


class SolarSystem:
    def __init__(self):
        self.bodies = []
        self.time = 0
        self.load_planet_data()

    def load_planet_data(self):
        """Load planetary data from JSON file"""
        with open('data/planet_data.json', 'r') as f:
            data = json.load(f)

        for body_name, body_data in data.items():
            body = CelestialBody(
                name=body_data['name'],
                mass=body_data['mass'],
                radius=body_data['radius'],
                color=body_data['color'],
                body_type=body_data['type']  # Fixed: using body_data['type']
            )

            # FIXED: Changed 'body_type' to 'body_data['type']'
            if body_data['type'] == 'planet':
                body.set_orbital_parameters(
                    body_data['semi_major_axis'],
                    body_data['eccentricity'],
                    body_data['orbital_period']
                )

            self.bodies.append(body)

    def derivatives(self, t, y):
        """Calculate derivatives for the ODE solver"""
        n_bodies = len(self.bodies)
        derivatives = np.zeros(6 * n_bodies)

        # Unpack positions and velocities
        positions = y[:3 * n_bodies].reshape(n_bodies, 3)
        velocities = y[3 * n_bodies:].reshape(n_bodies, 3)

        # Calculate accelerations
        accelerations = np.zeros((n_bodies, 3))

        for i in range(n_bodies):
            for j in range(n_bodies):
                if i != j:
                    r_vec = positions[j] - positions[i]
                    r_mag = np.linalg.norm(r_vec)

                    if r_mag > 0:
                        accelerations[i] += (G * self.bodies[j].mass /
                                             (r_mag ** 3)) * r_vec

        # Pack derivatives
        derivatives[:3 * n_bodies] = velocities.flatten()
        derivatives[3 * n_bodies:] = accelerations.flatten()

        return derivatives

    def simulate(self, time_span, n_steps=1000):
        """Run the simulation"""
        # Initial state vector
        y0 = np.zeros(6 * len(self.bodies))

        for i, body in enumerate(self.bodies):
            y0[3 * i:3 * i + 3] = body.position
            y0[3 * len(self.bodies) + 3 * i:3 * len(self.bodies) + 3 * i + 3] = body.velocity

        # Time points
        t_eval = np.linspace(0, time_span, n_steps)

        # Solve ODE
        solution = solve_ivp(
            self.derivatives,
            [0, time_span],
            y0,
            t_eval=t_eval,
            method='RK45',
            rtol=1e-8
        )

        # Store results
        self.simulation_time = solution.t
        self.simulation_results = solution.y

        # Update bodies with final positions
        self.update_bodies_from_solution(-1)

    def update_bodies_from_solution(self, time_index):
        """Update body positions and velocities from simulation results"""
        n_bodies = len(self.bodies)

        for i in range(n_bodies):
            self.bodies[i].position = self.simulation_results[3 * i:3 * i + 3, time_index]
            self.bodies[i].velocity = self.simulation_results[3 * n_bodies + 3 * i:3 * n_bodies + 3 * i + 3, time_index]

    def get_body_trajectory(self, body_index):
        """Get trajectory for a specific body"""
        n_bodies = len(self.bodies)
        trajectory = self.simulation_results[3 * body_index:3 * body_index + 3, :]
        return trajectory.T

    def get_sun(self):
        """Get the sun object"""
        for body in self.bodies:
            if body.type == 'star':
                return body
        return None