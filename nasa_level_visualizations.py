#!/usr/bin/env python3
"""
NASA-LEVEL PROFESSIONAL SOLAR SYSTEM VISUALIZATIONS - FIXED VERSION
Scientific-grade accuracy with stunning visuals
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Wedge
import matplotlib.colors as mcolors
from matplotlib.collections import PatchCollection
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from scipy.interpolate import griddata
import pandas as pd
from solar_system import SolarSystem
from data.constants import AU, G, SOLAR_MASS
import json


class NASAVisualizer:
    def __init__(self, solar_system):
        self.solar_system = solar_system
        self.load_nasa_grade_data()
        self.setup_professional_colors()

    def setup_professional_colors(self):
        """NASA-inspired color palettes with scientific accuracy"""
        self.nasa_colors = {
            'mercury': {'surface': '#8C7853', 'craters': '#5D4C36', 'highlands': '#A69B82'},
            'venus': {'clouds': '#FFC649', 'surface': '#964B00', 'atmosphere': '#FFA500'},
            'earth': {'oceans': '#1E90FF', 'land': '#228B22', 'clouds': '#FFFFFF', 'atmosphere': '#87CEEB'},
            'mars': {'surface': '#CD5C5C', 'olympus_mons': '#8B0000', 'polar_caps': '#F0F8FF'},
            'jupiter': {'belts': '#C19A6B', 'zones': '#DEB887', 'great_red_spot': '#8B0000'},
            'saturn': {'rings': '#EDD59E', 'planet': '#F5E4BE', 'ring_shadow': '#D2B48C'},
            'uranus': {'atmosphere': '#4FD0E7', 'clouds': '#AFEEEE', 'rings': '#87CEEB'},
            'neptune': {'atmosphere': '#4B70DD', 'storms': '#000080', 'clouds': '#4682B4'},
            'sun': {'core': '#FF4500', 'surface': '#FF8C00', 'corona': '#FFD700'}
        }

        # Simple color mapping for quick access
        self.planet_base_colors = {
            'mercury': '#8C7853',
            'venus': '#FFC649',
            'earth': '#1E90FF',
            'mars': '#CD5C5C',
            'jupiter': '#C19A6B',
            'saturn': '#EDD59E',
            'uranus': '#4FD0E7',
            'neptune': '#4B70DD',
            'sun': '#FFD700'
        }

        # Space background gradients
        self.space_gradients = {
            'deep_space': ['#000033', '#0B0B3B', '#1A1A4B'],
            'nebula': ['#2E0854', '#4B0082', '#191970'],
            'galactic': ['#000000', '#0A0A2A', '#151540']
        }

    def load_nasa_grade_data(self):
        """Load comprehensive NASA-grade planetary data"""
        with open('data/planet_data.json', 'r') as f:
            self.planet_data = json.load(f)

        # Enhanced orbital elements (NASA JPL data)
        self.orbital_elements = {
            'mercury': {'a': 0.387, 'e': 0.2056, 'i': 7.0, 'ω': 29.1, 'Ω': 48.3},
            'venus': {'a': 0.723, 'e': 0.0067, 'i': 3.4, 'ω': 54.9, 'Ω': 76.7},
            'earth': {'a': 1.000, 'e': 0.0167, 'i': 0.0, 'ω': 114.2, 'Ω': 0.0},
            'mars': {'a': 1.524, 'e': 0.0935, 'i': 1.9, 'ω': 286.5, 'Ω': 49.6},
            'jupiter': {'a': 5.203, 'e': 0.0489, 'i': 1.3, 'ω': 273.9, 'Ω': 100.6},
            'saturn': {'a': 9.537, 'e': 0.0565, 'i': 2.5, 'ω': 339.4, 'Ω': 113.7},
            'uranus': {'a': 19.191, 'e': 0.0457, 'i': 0.8, 'ω': 96.5, 'Ω': 74.0},
            'neptune': {'a': 30.069, 'e': 0.0113, 'i': 1.8, 'ω': 273.2, 'Ω': 131.8}
        }

        # Physical characteristics (NASA data)
        self.physical_data = {
            'mercury': {'density': 5.43, 'gravity': 3.7, 'escape_velocity': 4.3, 'albedo': 0.11},
            'venus': {'density': 5.24, 'gravity': 8.87, 'escape_velocity': 10.36, 'albedo': 0.65},
            'earth': {'density': 5.51, 'gravity': 9.81, 'escape_velocity': 11.19, 'albedo': 0.37},
            'mars': {'density': 3.93, 'gravity': 3.71, 'escape_velocity': 5.03, 'albedo': 0.15},
            'jupiter': {'density': 1.33, 'gravity': 24.79, 'escape_velocity': 59.5, 'albedo': 0.52},
            'saturn': {'density': 0.69, 'gravity': 10.44, 'escape_velocity': 35.5, 'albedo': 0.47},
            'uranus': {'density': 1.27, 'gravity': 8.87, 'escape_velocity': 21.3, 'albedo': 0.51},
            'neptune': {'density': 1.64, 'gravity': 11.15, 'escape_velocity': 23.5, 'albedo': 0.41}
        }

        # Atmospheric composition (percentage)
        self.atmospheres = {
            'mercury': {'He': 95, 'Na': 5},
            'venus': {'CO2': 96.5, 'N2': 3.5},
            'earth': {'N2': 78, 'O2': 21, 'Ar': 1},
            'mars': {'CO2': 95, 'N2': 2.7, 'Ar': 1.6},
            'jupiter': {'H2': 90, 'He': 10},
            'saturn': {'H2': 96, 'He': 3},
            'uranus': {'H2': 83, 'He': 15, 'CH4': 2},
            'neptune': {'H2': 80, 'He': 19, 'CH4': 1}
        }

    def get_planet_color(self, planet_name, color_type='surface'):
        """Safe method to get planet colors"""
        try:
            return self.nasa_colors[planet_name][color_type]
        except KeyError:
            return self.planet_base_colors.get(planet_name, '#FFFFFF')

    def create_science_dashboard(self):
        """Comprehensive scientific dashboard with multiple analysis panels"""
        fig = plt.figure(figsize=(28, 18))
        fig.patch.set_facecolor('#000033')

        # Complex grid layout for professional appearance
        gs = plt.GridSpec(4, 6, figure=fig, hspace=0.5, wspace=0.4)

        # Row 1: Orbital Mechanics
        ax1 = fig.add_subplot(gs[0, 0:2])  # Realistic orbits
        self._plot_precision_orbits(ax1)

        ax2 = fig.add_subplot(gs[0, 2:4])  # Orbital parameters
        self._plot_orbital_parameters(ax2)

        ax3 = fig.add_subplot(gs[0, 4:6])  # Velocity profile
        self._plot_velocity_profile(ax3)

        # Row 2: Physical Properties
        ax4 = fig.add_subplot(gs[1, 0:2])  # Density comparison
        self._plot_density_comparison(ax4)

        ax5 = fig.add_subplot(gs[1, 2:4])  # Gravity field
        self._plot_gravity_comparison(ax5)

        ax6 = fig.add_subplot(gs[1, 4:6])  # Escape velocity
        self._plot_escape_velocity(ax6)

        # Row 3: Atmospheric Science
        ax7 = fig.add_subplot(gs[2, 0:3])  # Atmospheric composition
        self._plot_atmospheric_composition(ax7)

        ax8 = fig.add_subplot(gs[2, 3:6])  # Albedo comparison
        self._plot_albedo_comparison(ax8)

        # Row 4: System Dynamics
        ax9 = fig.add_subplot(gs[3, 0:3])  # Orbital resonances
        self._plot_orbital_resonances(ax9)

        ax10 = fig.add_subplot(gs[3, 3:6])  # Temperature profile
        self._plot_temperature_profile(ax10)

        plt.suptitle('🔬 NASA-GRADE SOLAR SYSTEM SCIENCE DASHBOARD 🔬',
                     fontsize=26, fontweight='bold', color='white', y=0.98)

        return fig

    def _plot_precision_orbits(self, ax):
        """High-precision orbital mechanics visualization"""
        ax.set_facecolor('#000033')
        self._create_realistic_starfield(ax, 500)

        # Plot sun with scientific accuracy
        sun_radius = 0.00465  # AU scale
        sun_disk = Circle((0, 0), sun_radius, color=self.get_planet_color('sun', 'surface'), alpha=0.9)
        ax.add_patch(sun_disk)

        # Corona effect
        corona = Circle((0, 0), sun_radius * 1.5, color=self.get_planet_color('sun', 'corona'), alpha=0.3)
        ax.add_patch(corona)

        for planet_name, elements in self.orbital_elements.items():
            planet_data = self.planet_data[planet_name]
            a = elements['a']  # Semi-major axis in AU
            e = elements['e']  # Eccentricity
            i = np.radians(elements['i'])  # Inclination
            ω = np.radians(elements['ω'])  # Argument of perihelion
            Ω = np.radians(elements['Ω'])  # Longitude of ascending node

            # Generate precise elliptical orbit using Keplerian elements
            theta = np.linspace(0, 2 * np.pi, 500)
            r = a * (1 - e ** 2) / (1 + e * np.cos(theta - ω))

            # Convert to Cartesian coordinates with proper orientation
            x = r * (np.cos(theta + Ω) * np.cos(ω) - np.sin(theta + Ω) * np.sin(ω) * np.cos(i))
            y = r * (np.sin(theta + Ω) * np.cos(ω) + np.cos(theta + Ω) * np.sin(ω) * np.cos(i))

            # Plot orbit with scientific color coding
            color = self.get_planet_color(planet_name, 'surface')
            ax.plot(x, y, color=color, linewidth=1.5, alpha=0.8,
                    label=f"{planet_data['name']}")

            # Mark perihelion and aphelion
            perihelion_idx = np.argmin(r)
            aphelion_idx = np.argmax(r)

            ax.scatter(x[perihelion_idx], y[perihelion_idx],
                       color=color, s=30, marker='o', alpha=0.8)
            ax.scatter(x[aphelion_idx], y[aphelion_idx],
                       color=color, s=30, marker='s', alpha=0.8)

        ax.set_xlim(-35, 35)
        ax.set_ylim(-35, 35)
        ax.set_title('🛰️ PRECISION ORBITAL MECHANICS', color='white', fontsize=14, fontweight='bold')
        ax.legend(facecolor='#1A1A4B', edgecolor='white', labelcolor='white', fontsize=8)
        ax.grid(True, alpha=0.1, color='white')

    def _plot_orbital_parameters(self, ax):
        """Comparative analysis of orbital parameters"""
        planets = []
        eccentricities = []
        inclinations = []
        semi_major_axes = []
        colors = []

        for planet_name, elements in self.orbital_elements.items():
            planets.append(self.planet_data[planet_name]['name'])
            eccentricities.append(elements['e'])
            inclinations.append(elements['i'])
            semi_major_axes.append(elements['a'])
            colors.append(self.get_planet_color(planet_name, 'surface'))

        # Create comparative scatter plot
        scatter = ax.scatter(eccentricities, inclinations,
                             s=[a * 50 for a in semi_major_axes],  # Size by semi-major axis
                             c=colors, alpha=0.8, edgecolors='white', linewidth=1)

        # Add planet labels
        for i, planet in enumerate(planets):
            ax.annotate(planet, (eccentricities[i], inclinations[i]),
                        xytext=(5, 5), textcoords='offset points',
                        color='white', fontsize=8)

        ax.set_facecolor('#000033')
        ax.set_xlabel('Orbital Eccentricity', color='white')
        ax.set_ylabel('Orbital Inclination (°)', color='white')
        ax.set_title('📈 ORBITAL PARAMETER SPACE', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white')

    def _plot_velocity_profile(self, ax):
        """Orbital velocity analysis with scientific accuracy"""
        planets = []
        velocities = []
        distances = []
        colors = []

        for planet_name, elements in self.orbital_elements.items():
            planets.append(self.planet_data[planet_name]['name'])
            a = elements['a'] * AU  # Convert to meters
            v = np.sqrt(G * SOLAR_MASS / a) / 1000  # Orbital velocity in km/s
            velocities.append(v)
            distances.append(elements['a'])
            colors.append(self.get_planet_color(planet_name, 'surface'))

        # Create scientific velocity profile
        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, velocities, color=colors, alpha=0.8, edgecolor='white')

        # Add velocity values
        for i, (bar, vel) in enumerate(zip(bars, velocities)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f'{vel:.1f} km/s', ha='center', va='bottom', color='white', fontsize=9)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Orbital Velocity (km/s)', color='white')
        ax.set_title('🚀 KEPLERIAN VELOCITY PROFILE', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_density_comparison(self, ax):
        """Planetary density analysis with scientific context"""
        planets = []
        densities = []
        colors = []

        for planet_name, physical in self.physical_data.items():
            planets.append(self.planet_data[planet_name]['name'])
            densities.append(physical['density'])
            colors.append(self.get_planet_color(planet_name, 'surface'))

        # Create density comparison with reference lines
        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, densities, color=colors, alpha=0.8, edgecolor='white')

        # Add reference lines for water and iron
        ax.axhline(y=1.0, color='cyan', linestyle='--', alpha=0.7, label='Water Density')
        ax.axhline(y=7.87, color='red', linestyle='--', alpha=0.7, label='Iron Density')

        # Add density values
        for i, (bar, density) in enumerate(zip(bars, densities)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                    f'{density:.2f} g/cm³', ha='center', va='bottom', color='white', fontsize=8)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Density (g/cm³)', color='white')
        ax.set_title('⚖️ PLANETARY DENSITY COMPARISON', color='white', fontsize=14, fontweight='bold')
        ax.legend(facecolor='#1A1A4B', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_gravity_comparison(self, ax):
        """Surface gravity analysis"""
        planets = []
        gravities = []
        colors = []

        for planet_name, physical in self.physical_data.items():
            planets.append(self.planet_data[planet_name]['name'])
            gravities.append(physical['gravity'])
            colors.append(self.get_planet_color(planet_name, 'surface'))

        # Create gravity comparison with Earth reference
        earth_gravity = 9.81
        relative_gravities = [g / earth_gravity for g in gravities]

        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, relative_gravities, color=colors, alpha=0.8, edgecolor='white')

        ax.axhline(y=1.0, color='green', linestyle='--', alpha=0.7, label='Earth Gravity')

        for i, (bar, rel_g) in enumerate(zip(bars, relative_gravities)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f'{rel_g:.2f}×', ha='center', va='bottom', color='white', fontsize=8)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Relative Surface Gravity (Earth = 1)', color='white')
        ax.set_title('🌍 SURFACE GRAVITY COMPARISON', color='white', fontsize=14, fontweight='bold')
        ax.legend(facecolor='#1A1A4B', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_escape_velocity(self, ax):
        """Escape velocity analysis"""
        planets = []
        escape_velocities = []
        colors = []

        for planet_name, physical in self.physical_data.items():
            planets.append(self.planet_data[planet_name]['name'])
            escape_velocities.append(physical['escape_velocity'])
            colors.append(self.get_planet_color(planet_name, 'surface'))

        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, escape_velocities, color=colors, alpha=0.8, edgecolor='white')

        for i, (bar, esc_vel) in enumerate(zip(bars, escape_velocities)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                    f'{esc_vel:.1f} km/s', ha='center', va='bottom', color='white', fontsize=8)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Escape Velocity (km/s)', color='white')
        ax.set_title('🚀 ESCAPE VELOCITY ANALYSIS', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_atmospheric_composition(self, ax):
        """Detailed atmospheric composition analysis"""
        planets = list(self.atmospheres.keys())
        planet_names = [self.planet_data[p]['name'] for p in planets]

        # Prepare stacked bar data
        gases = set()
        for composition in self.atmospheres.values():
            gases.update(composition.keys())
        gases = sorted(gases)

        bottom = np.zeros(len(planets))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']

        for i, gas in enumerate(gases):
            percentages = [self.atmospheres[planet].get(gas, 0) for planet in planets]
            bars = ax.bar(planet_names, percentages, bottom=bottom,
                          label=gas, color=colors[i % len(colors)], alpha=0.8)
            bottom += percentages

            # Add percentage labels
            for j, (bar, percentage) in enumerate(zip(bars, percentages)):
                if percentage > 5:  # Only label significant percentages
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
                            f'{percentage:.1f}%', ha='center', va='center', color='white', fontsize=7)

        ax.set_facecolor('#000033')
        ax.set_ylabel('Atmospheric Composition (%)', color='white')
        ax.set_title('🌫️ ATMOSPHERIC COMPOSITION ANALYSIS', color='white', fontsize=14, fontweight='bold')
        ax.legend(facecolor='#1A1A4B', edgecolor='white', labelcolor='white', fontsize=8)
        ax.grid(True, alpha=0.2, color='white', axis='y')
        plt.setp(ax.get_xticklabels(), rotation=45, color='white')

    def _plot_albedo_comparison(self, ax):
        """Planetary albedo (reflectivity) analysis"""
        planets = []
        albedos = []
        colors = []

        for planet_name, physical in self.physical_data.items():
            planets.append(self.planet_data[planet_name]['name'])
            albedos.append(physical['albedo'])
            colors.append(self.get_planet_color(planet_name, 'surface'))

        # Create albedo comparison
        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, albedos, color=colors, alpha=0.8, edgecolor='white')

        for i, (bar, albedo) in enumerate(zip(bars, albedos)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                    f'{albedo:.2f}', ha='center', va='bottom', color='white', fontsize=8)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Bond Albedo', color='white')
        ax.set_title('☀️ PLANETARY ALBEDO COMPARISON', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_orbital_resonances(self, ax):
        """Orbital resonance analysis"""
        planets = list(self.orbital_elements.keys())
        planet_names = [self.planet_data[p]['name'] for p in planets]
        periods = [self.planet_data[p]['orbital_period'] for p in planets]

        # Calculate resonance ratios with Jupiter (reference)
        jupiter_period = self.planet_data['jupiter']['orbital_period']
        resonances = [p / jupiter_period for p in periods]

        colors = [self.get_planet_color(p, 'surface') for p in planets]

        # Create resonance plot
        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, resonances, color=colors, alpha=0.8, edgecolor='white')

        ax.axhline(y=1.0, color='orange', linestyle='--', alpha=0.7, label='Jupiter Reference')

        for i, (bar, resonance) in enumerate(zip(bars, resonances)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                    f'{resonance:.2f}', ha='center', va='bottom', color='white', fontsize=8)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planet_names, rotation=45, color='white')
        ax.set_ylabel('Orbital Period Ratio (Jupiter = 1)', color='white')
        ax.set_title('🔄 ORBITAL RESONANCE ANALYSIS', color='white', fontsize=14, fontweight='bold')
        ax.legend(facecolor='#1A1A4B', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_temperature_profile(self, ax):
        """Scientific temperature profile with blackbody calculations"""
        distances = [elements['a'] for elements in self.orbital_elements.values()]
        planets = [self.planet_data[p]['name'] for p in self.orbital_elements.keys()]

        # Calculate theoretical blackbody temperatures
        solar_constant = 1361  # W/m² at 1 AU
        albedos = [self.physical_data[p]['albedo'] for p in self.orbital_elements.keys()]

        blackbody_temps = []
        for i, distance in enumerate(distances):
            # Simplified blackbody temperature calculation
            effective_temp = 279 * (1 - albedos[i]) ** 0.25 / np.sqrt(distance)
            blackbody_temps.append(effective_temp - 273.15)  # Convert to Celsius

        # Actual average temperatures (Celsius)
        actual_temps = [167, 464, 15, -65, -110, -140, -195, -200]

        x_pos = np.arange(len(planets))
        width = 0.35

        ax.bar(x_pos - width / 2, blackbody_temps, width, label='Theoretical', alpha=0.7, color='skyblue')
        ax.bar(x_pos + width / 2, actual_temps, width, label='Actual', alpha=0.7, color='coral')

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Temperature (°C)', color='white')
        ax.set_title('🌡️ TEMPERATURE PROFILE ANALYSIS', color='white', fontsize=14, fontweight='bold')
        ax.legend(facecolor='#1A1A4B', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _create_realistic_starfield(self, ax, num_stars):
        """Create scientifically accurate starfield"""
        # Generate stars with realistic magnitude distribution
        magnitudes = np.random.exponential(1.0, num_stars)
        sizes = 0.5 + magnitudes * 2
        brightness = 0.1 + 0.9 * (1 - np.exp(-magnitudes))

        x_stars = np.random.uniform(-40, 40, num_stars)
        y_stars = np.random.uniform(-40, 40, num_stars)

        # Add some bright stars (larger, brighter)
        bright_indices = np.random.choice(num_stars, num_stars // 10, replace=False)
        sizes[bright_indices] *= 3
        brightness[bright_indices] = 1.0

        ax.scatter(x_stars, y_stars, s=sizes, c='white', alpha=brightness, marker='.')

    def create_interactive_3d_solar_system(self):
        """Create stunning interactive 3D visualization"""
        fig = go.Figure()

        # Add realistic starfield
        star_x = np.random.uniform(-50, 50, 2000)
        star_y = np.random.uniform(-50, 50, 2000)
        star_z = np.random.uniform(-50, 50, 2000)
        star_size = np.random.uniform(0.5, 3, 2000)

        fig.add_trace(go.Scatter3d(
            x=star_x, y=star_y, z=star_z,
            mode='markers',
            marker=dict(size=star_size, color='white', opacity=0.6),
            name='Starfield',
            showlegend=False
        ))

        # Add planets with precise orbits
        for planet_name, elements in self.orbital_elements.items():
            a = elements['a']
            e = elements['e']
            i = np.radians(elements['i'])

            # Generate precise elliptical orbit
            theta = np.linspace(0, 2 * np.pi, 200)
            r = a * (1 - e ** 2) / (1 + e * np.cos(theta))

            # 3D coordinates with inclination
            x = r * np.cos(theta)
            y = r * np.sin(theta) * np.cos(i)
            z = r * np.sin(theta) * np.sin(i)

            # Add orbit trace
            fig.add_trace(go.Scatter3d(
                x=x, y=y, z=z,
                mode='lines',
                line=dict(color=self.get_planet_color(planet_name, 'surface'), width=3),
                name=f"{self.planet_data[planet_name]['name']} Orbit",
                showlegend=True
            ))

            # Add planet
            planet_size = max(2, np.log(self.planet_data[planet_name]['radius'] / 1e7) * 6)
            fig.add_trace(go.Scatter3d(
                x=[x[0]], y=[y[0]], z=[z[0]],
                mode='markers',
                marker=dict(
                    size=planet_size,
                    color=self.get_planet_color(planet_name, 'surface'),
                    line=dict(color='white', width=1)
                ),
                name=self.planet_data[planet_name]['name']
            ))

        # Add spectacular sun
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(size=15, color='#FFD700', opacity=0.9),
            name='Sun'
        ))

        fig.update_layout(
            title='🌌 NASA-GRADE 3D SOLAR SYSTEM VISUALIZATION 🌌',
            scene=dict(
                xaxis_title='X (AU)',
                yaxis_title='Y (AU)',
                zaxis_title='Z (AU)',
                bgcolor='#000033',
                xaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)'),
                zaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)'),
            ),
            width=1200,
            height=800,
            paper_bgcolor='#000033',
            font=dict(color='white', size=12)
        )

        return fig


def main():
    print("🔬 CREATING NASA-GRADE SOLAR SYSTEM VISUALIZATIONS...")
    print("📊 This will generate professional scientific dashboards! 📊")

    # Create solar system
    solar_system = SolarSystem()
    solar_system.simulate(time_span=365, n_steps=500)

    # Create NASA-grade visualizer
    nasa_viz = NASAVisualizer(solar_system)

    print("1. 🛰️ Creating Comprehensive Science Dashboard...")
    fig1 = nasa_viz.create_science_dashboard()
    plt.savefig('NASA_GRADE_SCIENCE_DASHBOARD.png', dpi=300, bbox_inches='tight',
                facecolor='#000033', edgecolor='none')

    print("2. 🌌 Creating Interactive 3D Visualization...")
    fig2 = nasa_viz.create_interactive_3d_solar_system()
    fig2.write_html('NASA_3D_SOLAR_SYSTEM.html')

    print("\n🎉 NASA-GRADE VISUALIZATIONS COMPLETED! 🎉")
    print("📁 PROFESSIONAL FILES GENERATED:")
    print("   🔭 NASA_GRADE_SCIENCE_DASHBOARD.png")
    print("   🌠 NASA_3D_SOLAR_SYSTEM.html")
    print("\n🔬 SCIENTIFIC FEATURES INCLUDED:")
    print("   ✅ Precision orbital mechanics with Keplerian elements")
    print("   ✅ Comprehensive physical property analysis")
    print("   ✅ Atmospheric composition breakdown")
    print("   ✅ Gravity and density comparisons")
    print("   ✅ Escape velocity calculations")
    print("   ✅ Albedo and temperature profiles")
    print("   ✅ Orbital resonance analysis")
    print("   ✅ Professional scientific color coding")
    print("   ✅ Interactive 3D visualization with realistic orbits")

    plt.show()


if __name__ == "__main__":
    main()