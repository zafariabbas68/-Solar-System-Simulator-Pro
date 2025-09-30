#!/usr/bin/env python3
"""
ULTIMATE PROFESSIONAL SOLAR SYSTEM VISUALIZATIONS
Final enhanced version with all fixes and improvements
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import matplotlib.colors as mcolors
from solar_system import SolarSystem
from data.constants import AU, G, SOLAR_MASS
import json


class UltimateVisualizer:
    def __init__(self, solar_system):
        self.solar_system = solar_system
        self.load_ultimate_data()

    def load_ultimate_data(self):
        """Load ultimate planetary dataset"""
        with open('data/planet_data.json', 'r') as f:
            self.planet_data = json.load(f)

        # Ultimate color scheme
        self.planet_colors = {
            'mercury': '#8C7853', 'venus': '#FFC649', 'earth': '#1E90FF',
            'mars': '#CD5C5C', 'jupiter': '#C19A6B', 'saturn': '#EDD59E',
            'uranus': '#4FD0E7', 'neptune': '#4B70DD', 'sun': '#FFD700'
        }

        # Scientific data
        self.science_data = {
            'mercury': {'temp': 167, 'day_length': 1407.6, 'moons': 0},
            'venus': {'temp': 464, 'day_length': -5832.5, 'moons': 0},
            'earth': {'temp': 15, 'day_length': 24.0, 'moons': 1},
            'mars': {'temp': -65, 'day_length': 24.7, 'moons': 2},
            'jupiter': {'temp': -110, 'day_length': 9.9, 'moons': 95},
            'saturn': {'temp': -140, 'day_length': 10.7, 'moons': 146},
            'uranus': {'temp': -195, 'day_length': -17.2, 'moons': 28},
            'neptune': {'temp': -200, 'day_length': 16.1, 'moons': 16}
        }

    def create_ultimate_comparison(self):
        """Ultimate comparison dashboard"""
        fig = plt.figure(figsize=(20, 16))
        fig.patch.set_facecolor('#000033')

        gs = plt.GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.3)

        # Planetary sizes comparison
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_planetary_sizes(ax1)

        # Orbital periods
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_orbital_periods(ax2)

        # Surface temperatures
        ax3 = fig.add_subplot(gs[0, 2])
        self._plot_temperatures(ax3)

        # Day lengths
        ax4 = fig.add_subplot(gs[1, 0])
        self._plot_day_lengths(ax4)

        # Moon counts
        ax5 = fig.add_subplot(gs[1, 1])
        self._plot_moon_counts(ax5)

        # Distance from sun
        ax6 = fig.add_subplot(gs[1, 2])
        self._plot_distances(ax6)

        # Complete solar system view
        ax7 = fig.add_subplot(gs[2, :])
        self._plot_complete_system(ax7)

        plt.suptitle('SOLAR SYSTEM ULTIMATE COMPARISON DASHBOARD',
                     fontsize=24, fontweight='bold', color='white', y=0.95)

        return fig

    def _plot_planetary_sizes(self, ax):
        """Plot planetary sizes with realistic scaling"""
        planets = []
        radii = []
        colors = []

        for planet_name, planet_data in self.planet_data.items():
            if planet_data['type'] == 'planet':
                planets.append(planet_data['name'])
                radii.append(planet_data['radius'] / 1000)  # Convert to km
                colors.append(self.planet_colors[planet_name])

        # Create size comparison
        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, radii, color=colors, alpha=0.8, edgecolor='white')

        for i, (bar, radius) in enumerate(zip(bars, radii)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1000,
                    f'{radius:,.0f} km', ha='center', va='bottom', color='white', fontsize=8)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Radius (km)', color='white')
        ax.set_title('Planetary Sizes', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_orbital_periods(self, ax):
        """Plot orbital periods"""
        planets = []
        periods = []
        colors = []

        for planet_name, planet_data in self.planet_data.items():
            if planet_data['type'] == 'planet':
                planets.append(planet_data['name'])
                periods.append(planet_data['orbital_period'])
                colors.append(self.planet_colors[planet_name])

        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, periods, color=colors, alpha=0.8, edgecolor='white')

        for i, (bar, period) in enumerate(zip(bars, periods)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100,
                    f'{period:.0f} days', ha='center', va='bottom', color='white', fontsize=8)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Orbital Period (days)', color='white')
        ax.set_title('Orbital Periods', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_temperatures(self, ax):
        """Plot surface temperatures"""
        planets = []
        temps = []
        colors = []

        for planet_name, science in self.science_data.items():
            planets.append(self.planet_data[planet_name]['name'])
            temps.append(science['temp'])
            colors.append(self.planet_colors[planet_name])

        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, temps, color=colors, alpha=0.8, edgecolor='white')

        for i, (bar, temp) in enumerate(zip(bars, temps)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                    f'{temp}°C', ha='center', va='bottom', color='white', fontsize=8)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Temperature (°C)', color='white')
        ax.set_title('Surface Temperatures', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_day_lengths(self, ax):
        """Plot length of day"""
        planets = []
        day_lengths = []
        colors = []

        for planet_name, science in self.science_data.items():
            planets.append(self.planet_data[planet_name]['name'])
            day_lengths.append(abs(science['day_length']))
            colors.append(self.planet_colors[planet_name])

        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, day_lengths, color=colors, alpha=0.8, edgecolor='white')

        for i, (bar, length) in enumerate(zip(bars, day_lengths)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f'{length} hrs', ha='center', va='bottom', color='white', fontsize=8)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Day Length (hours)', color='white')
        ax.set_title('Length of Day', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_moon_counts(self, ax):
        """Plot number of moons"""
        planets = []
        moons = []
        colors = []

        for planet_name, science in self.science_data.items():
            planets.append(self.planet_data[planet_name]['name'])
            moons.append(science['moons'])
            colors.append(self.planet_colors[planet_name])

        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, moons, color=colors, alpha=0.8, edgecolor='white')

        for i, (bar, moon_count) in enumerate(zip(bars, moons)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                    f'{moon_count}', ha='center', va='bottom', color='white', fontsize=9)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Number of Moons', color='white')
        ax.set_title('Natural Satellites', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_distances(self, ax):
        """Plot distances from sun"""
        planets = []
        distances = []
        colors = []

        for planet_name, planet_data in self.planet_data.items():
            if planet_data['type'] == 'planet':
                planets.append(planet_data['name'])
                distances.append(planet_data['semi_major_axis'] / AU)
                colors.append(self.planet_colors[planet_name])

        x_pos = np.arange(len(planets))
        bars = ax.bar(x_pos, distances, color=colors, alpha=0.8, edgecolor='white')

        for i, (bar, distance) in enumerate(zip(bars, distances)):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                    f'{distance:.1f} AU', ha='center', va='bottom', color='white', fontsize=8)

        ax.set_facecolor('#000033')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(planets, rotation=45, color='white')
        ax.set_ylabel('Distance from Sun (AU)', color='white')
        ax.set_title('Orbital Distances', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='y')

    def _plot_complete_system(self, ax):
        """Plot complete solar system"""
        ax.set_facecolor('#000033')

        # Create starfield
        x_stars = np.random.uniform(-40, 40, 300)
        y_stars = np.random.uniform(-40, 40, 300)
        ax.scatter(x_stars, y_stars, s=1, c='white', alpha=0.6)

        # Plot sun
        ax.scatter(0, 0, color=self.planet_colors['sun'], s=300, label='Sun')

        # Plot planets and orbits
        for planet_name, planet_data in self.planet_data.items():
            if planet_data['type'] == 'planet':
                a = planet_data['semi_major_axis'] / AU
                e = planet_data['eccentricity']

                # Generate elliptical orbit
                theta = np.linspace(0, 2 * np.pi, 100)
                r = a * (1 - e ** 2) / (1 + e * np.cos(theta))
                x = r * np.cos(theta)
                y = r * np.sin(theta)

                ax.plot(x, y, color=self.planet_colors[planet_name], alpha=0.7, linewidth=1)
                ax.scatter(x[0], y[0], color=self.planet_colors[planet_name], s=50,
                           label=planet_data['name'])

        ax.set_xlim(-35, 35)
        ax.set_ylim(-35, 35)
        ax.set_xlabel('Distance (AU)', color='white')
        ax.set_ylabel('Distance (AU)', color='white')
        ax.set_title('Complete Solar System', color='white', fontsize=16, fontweight='bold')
        ax.legend(facecolor='#1A1A4B', edgecolor='white', labelcolor='white', fontsize=8)
        ax.grid(True, alpha=0.1, color='white')


def main():
    print("🚀 CREATING ULTIMATE SOLAR SYSTEM VISUALIZATIONS...")

    # Create solar system
    solar_system = SolarSystem()
    solar_system.simulate(time_span=365, n_steps=500)

    # Create ultimate visualizer
    ultimate_viz = UltimateVisualizer(solar_system)

    print("1. Creating Ultimate Comparison Dashboard...")
    fig = ultimate_viz.create_ultimate_comparison()
    plt.savefig('ULTIMATE_SOLAR_SYSTEM_DASHBOARD.png', dpi=300, bbox_inches='tight',
                facecolor='#000033', edgecolor='none')

    print("\n🎉 ULTIMATE VISUALIZATIONS COMPLETED! 🎉")
    print("📁 NEW FILE GENERATED:")
    print("   🌟 ULTIMATE_SOLAR_SYSTEM_DASHBOARD.png")
    print("\n📊 DASHBOARD FEATURES:")
    print("   ✅ Planetary size comparison")
    print("   ✅ Orbital period analysis")
    print("   ✅ Surface temperature mapping")
    print("   ✅ Day length comparison")
    print("   ✅ Moon count visualization")
    print("   ✅ Distance from sun analysis")
    print("   ✅ Complete solar system view")

    plt.show()


if __name__ == "__main__":
    main()