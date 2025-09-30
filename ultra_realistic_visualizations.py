#!/usr/bin/env python3
"""
ULTRA-REALISTIC Solar System Visualizations with Outstanding Colors
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.colors as mcolors
from solar_system import SolarSystem
from data.constants import AU
import json


class UltraRealisticVisualizer:
    def __init__(self, solar_system):
        self.solar_system = solar_system
        self.load_enhanced_planet_data()
        self.setup_stunning_colors()

    def setup_stunning_colors(self):
        """Enhanced color scheme with gradients and realistic hues"""
        self.planet_colors = {
            'mercury': ['#8C7853', '#A69B82', '#BFB6A3'],  # Rocky gray gradients
            'venus': ['#FFC649', '#FFD573', '#FFE39E'],  # Golden yellow gradients
            'earth': ['#1E90FF', '#6B93D6', '#87CEEB'],  # Ocean blue gradients
            'mars': ['#CD5C5C', '#DC7F7F', '#E8A2A2'],  # Red planet gradients
            'jupiter': ['#C19A6B', '#D4B896', '#E7D6C1'],  # Brown storm gradients
            'saturn': ['#EDD59E', '#F5E4BE', '#FBF2DE'],  # Golden ring gradients
            'uranus': ['#4FD0E7', '#7FDCEF', '#AFE8F7'],  # Ice blue gradients
            'neptune': ['#4B70DD', '#6F8FE4', '#93AFEB'],  # Deep blue gradients
            'sun': ['#FF4500', '#FF8C00', '#FFD700']  # Fiery sun gradients
        }

        self.background_gradient = ['#0B0B3B', '#1A1A4B', '#2D2D5B']  # Space nebula

    def load_enhanced_planet_data(self):
        """Load enhanced planetary data with textures and features"""
        with open('data/planet_data.json', 'r') as f:
            self.planet_data = json.load(f)

        # Add realistic orbital inclinations (degrees)
        self.orbital_inclinations = {
            'mercury': 7.0, 'venus': 3.4, 'earth': 0.0, 'mars': 1.9,
            'jupiter': 1.3, 'saturn': 2.5, 'uranus': 0.8, 'neptune': 1.8
        }

        # Add axial tilts for realistic appearance
        self.axial_tilts = {
            'mercury': 0.034, 'venus': 177.4, 'earth': 23.4, 'mars': 25.2,
            'jupiter': 3.1, 'saturn': 26.7, 'uranus': 97.8, 'neptune': 28.3
        }

    def create_galactic_overview(self):
        """Create a stunning galactic overview with multiple sections"""
        fig = plt.figure(figsize=(25, 15))

        # Create a beautiful dark background
        fig.patch.set_facecolor('#0B0B3B')

        # Define the grid layout
        gs = plt.GridSpec(3, 4, figure=fig, hspace=0.4, wspace=0.3)

        # Section 1: Inner Solar System (Top-Left)
        ax1 = fig.add_subplot(gs[0, 0:2])
        self._plot_inner_system_artistic(ax1)

        # Section 2: Outer Solar System (Top-Right)
        ax2 = fig.add_subplot(gs[0, 2:4])
        self._plot_outer_system_artistic(ax2)

        # Section 3: Planetary Size Comparison (Middle-Left)
        ax3 = fig.add_subplot(gs[1, 0])
        self._plot_size_comparison_3d(ax3)

        # Section 4: Orbital Velocity Heatmap (Middle-Right)
        ax4 = fig.add_subplot(gs[1, 1])
        self._plot_velocity_heatmap(ax4)

        # Section 5: Temperature Gradient (Bottom-Left)
        ax5 = fig.add_subplot(gs[1, 2])
        self._plot_temperature_gradient(ax5)

        # Section 6: Planetary Composition (Bottom-Right)
        ax6 = fig.add_subplot(gs[1, 3])
        self._plot_composition_chart(ax6)

        # Section 7: Timeline of Discovery (Bottom Full Width)
        ax7 = fig.add_subplot(gs[2, :])
        self._plot_discovery_timeline(ax7)

        plt.suptitle('🌌 ULTRA-REALISTIC SOLAR SYSTEM ATLAS 🌌',
                     fontsize=24, fontweight='bold', color='white', y=0.98)

        return fig

    def _plot_inner_system_artistic(self, ax):
        """Artistic inner solar system with realistic features"""
        ax.set_facecolor('#0B0B3B')

        # Create a starfield background
        self._create_starfield(ax, 200)

        # Plot sun with glow effect
        sun_glow = plt.Circle((0, 0), 0.15, color='yellow', alpha=0.3)
        ax.add_patch(sun_glow)
        ax.scatter(0, 0, color='#FFD700', s=500, label='Sun', edgecolors='orange', linewidth=2)

        inner_planets = ['mercury', 'venus', 'earth', 'mars']

        for i, planet_name in enumerate(inner_planets):
            planet_data = self.planet_data[planet_name]
            a = planet_data['semi_major_axis'] / AU
            e = planet_data['eccentricity']

            # Create realistic elliptical orbit
            theta = np.linspace(0, 2 * np.pi, 200)
            r = a * (1 - e ** 2) / (1 + e * np.cos(theta))
            x = r * np.cos(theta)
            y = r * np.sin(theta)

            # Plot orbit with gradient
            colors = self.planet_colors[planet_name]
            ax.plot(x, y, color=colors[0], linewidth=2, alpha=0.8,
                    label=f"{planet_data['name']} Orbit")

            # Plot planet with size relative to actual scale (log for visibility)
            planet_size = max(20, np.log(planet_data['radius'] / 1e6) * 30)
            ax.scatter(x[0], y[0], color=colors[1], s=planet_size,
                       label=planet_data['name'], edgecolors=colors[2], linewidth=1.5)

        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_title('🔭 INNER SOLAR SYSTEM', color='white', fontsize=14, fontweight='bold')
        ax.legend(facecolor='#1A1A4B', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2, color='white')

    def _plot_outer_system_artistic(self, ax):
        """Artistic outer solar system with logarithmic scale"""
        ax.set_facecolor('#0B0B3B')
        self._create_starfield(ax, 300)

        outer_planets = ['jupiter', 'saturn', 'uranus', 'neptune']

        # Plot sun
        ax.scatter(0, 0, color='#FFD700', s=100, label='Sun')

        for i, planet_name in enumerate(outer_planets):
            planet_data = self.planet_data[planet_name]
            a = planet_data['semi_major_axis'] / AU
            e = planet_data['eccentricity']

            # Use logarithmic scale for outer planets
            log_a = np.log10(a)

            # Create orbit circle (simplified for outer system)
            orbit = plt.Circle((0, 0), log_a, fill=False,
                               edgecolor=self.planet_colors[planet_name][0],
                               linewidth=2, alpha=0.7,
                               label=f"{planet_data['name']} Orbit")
            ax.add_patch(orbit)

            # Plot planet
            planet_size = max(30, np.log(planet_data['radius'] / 1e7) * 40)
            angle = i * (2 * np.pi / len(outer_planets))
            x = log_a * np.cos(angle)
            y = log_a * np.sin(angle)

            ax.scatter(x, y, color=self.planet_colors[planet_name][1],
                       s=planet_size, label=planet_data['name'],
                       edgecolors=self.planet_colors[planet_name][2], linewidth=2)

        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.set_title('🪐 OUTER SOLAR SYSTEM (Log Scale)', color='white', fontsize=14, fontweight='bold')
        ax.legend(facecolor='#1A1A4B', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.2, color='white')

    def _plot_size_comparison_3d(self, ax):
        """3D-style size comparison with perspective"""
        planets = []
        sizes = []
        colors = []

        for planet_name, planet_data in self.planet_data.items():
            if planet_data['type'] == 'planet':
                planets.append(planet_data['name'])
                # Normalize sizes for better visualization
                sizes.append(np.sqrt(planet_data['radius'] / 1e6) * 50)
                colors.append(self.planet_colors[planet_name][1])

        # Create 3D-like bars with shadows
        y_pos = np.arange(len(planets))

        # Main bars
        bars = ax.barh(y_pos, sizes, color=colors, alpha=0.8, edgecolor='white', linewidth=1)

        # Add shadow effect
        for i, bar in enumerate(bars):
            ax.barh(y_pos[i], sizes[i] * 0.95, color='black', alpha=0.3, height=0.7)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(planets, color='white')
        ax.set_facecolor('#0B0B3B')
        ax.set_title('📊 PLANETARY SIZE COMPARISON', color='white', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='x')

    def _plot_velocity_heatmap(self, ax):
        """Orbital velocity visualization as heatmap"""
        planets = []
        velocities = []
        colors = []

        for planet_name, planet_data in self.planet_data.items():
            if planet_data['type'] == 'planet':
                planets.append(planet_data['name'])
                # Calculate approximate orbital velocity (km/s)
                a = planet_data['semi_major_axis']
                orbital_velocity = np.sqrt(6.67430e-11 * 1.989e30 / a) / 1000
                velocities.append(orbital_velocity)
                colors.append(self.planet_colors[planet_name][1])

        # Create heatmap-style bars
        y_pos = np.arange(len(planets))
        bars = ax.barh(y_pos, velocities, color=colors, alpha=0.8)

        # Add value labels
        for i, (bar, vel) in enumerate(zip(bars, velocities)):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                    f'{vel:.1f} km/s', ha='left', va='center', color='white', fontsize=9)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(planets, color='white')
        ax.set_facecolor('#0B0B3B')
        ax.set_title('🚀 ORBITAL VELOCITIES', color='white', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='x')

    def _plot_temperature_gradient(self, ax):
        """Temperature gradient across solar system"""
        planets = []
        temperatures = [440, 737, 288, 210, 165, 134, 76, 72]  # Average temps in Kelvin
        colors = []

        planet_names = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

        for i, planet_name in enumerate(planet_names):
            planets.append(self.planet_data[planet_name]['name'])
            colors.append(self.planet_colors[planet_name][1])

        # Create gradient bars
        y_pos = np.arange(len(planets))
        bars = ax.barh(y_pos, temperatures, color=colors, alpha=0.8)

        # Add temperature labels
        for i, (bar, temp) in enumerate(zip(bars, temperatures)):
            ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height() / 2,
                    f'{temp}K', ha='left', va='center', color='white', fontsize=9)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(planets, color='white')
        ax.set_facecolor('#0B0B3B')
        ax.set_title('🌡️ AVERAGE TEMPERATURES', color='white', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='x')

    def _plot_composition_chart(self, ax):
        """Planetary composition visualization"""
        # Simplified composition data (rock/gas/ice percentages)
        compositions = {
            'mercury': [70, 30, 0], 'venus': [65, 35, 0], 'earth': [67, 33, 0], 'mars': [60, 40, 0],
            'jupiter': [10, 90, 0], 'saturn': [15, 85, 0], 'uranus': [20, 30, 50], 'neptune': [25, 35, 40]
        }

        planets = []
        for planet_name in ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']:
            planets.append(self.planet_data[planet_name]['name'])

        # Create stacked bar chart
        rock = [comp[0] for comp in compositions.values()]
        gas = [comp[1] for comp in compositions.values()]
        ice = [comp[2] for comp in compositions.values()]

        y_pos = np.arange(len(planets))

        ax.barh(y_pos, rock, color='#8B4513', alpha=0.8, label='Rock')
        ax.barh(y_pos, gas, left=rock, color='#87CEEB', alpha=0.8, label='Gas')
        ax.barh(y_pos, ice, left=np.array(rock) + np.array(gas), color='#F0F8FF', alpha=0.8, label='Ice')

        ax.set_yticks(y_pos)
        ax.set_yticklabels(planets, color='white')
        ax.set_facecolor('#0B0B3B')
        ax.set_title('🏗️ PLANETARY COMPOSITION', color='white', fontsize=12, fontweight='bold')
        ax.legend(facecolor='#1A1A4B', edgecolor='white', labelcolor='white', fontsize=8)
        ax.grid(True, alpha=0.2, color='white', axis='x')

    def _plot_discovery_timeline(self, ax):
        """Historical timeline of planetary discoveries"""
        discoveries = {
            'Mercury': -3000, 'Venus': -3000, 'Mars': -3000, 'Jupiter': -3000, 'Saturn': -3000,
            'Uranus': 1781, 'Neptune': 1846
        }

        planets = list(discoveries.keys())
        years = list(discoveries.values())
        colors = [self.planet_colors[planet.lower()][1] for planet in planets]

        # Create timeline
        y_pos = np.arange(len(planets))
        bars = ax.barh(y_pos, years, color=colors, alpha=0.8)

        # Add year labels
        for i, (bar, year) in enumerate(zip(bars, years)):
            label_x = bar.get_width() + 100 if year > 0 else bar.get_width() - 500
            ax.text(label_x, bar.get_y() + bar.get_height() / 2,
                    f'{abs(year)} {"BCE" if year < 0 else "CE"}',
                    ha='left' if year > 0 else 'right', va='center', color='white', fontsize=10)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(planets, color='white')
        ax.set_facecolor('#0B0B3B')
        ax.set_title('📅 DISCOVERY TIMELINE', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, color='white', axis='x')
        ax.axvline(x=0, color='white', linestyle='--', alpha=0.5)
        ax.text(0, len(planets) - 0.5, 'Common Era', color='white', ha='center', fontsize=8)

    def _create_starfield(self, ax, num_stars=100):
        """Create realistic starfield background"""
        x_stars = np.random.uniform(-10, 10, num_stars)
        y_stars = np.random.uniform(-10, 10, num_stars)
        sizes = np.random.uniform(0.5, 3, num_stars)
        brightness = np.random.uniform(0.3, 1.0, num_stars)

        ax.scatter(x_stars, y_stars, s=sizes, c='white', alpha=brightness, marker='*')

    def create_interactive_3d_masterpiece(self):
        """Create an ultra-realistic interactive 3D visualization"""
        fig = go.Figure()

        # Add starfield background
        star_x = np.random.uniform(-50, 50, 1000)
        star_y = np.random.uniform(-50, 50, 1000)
        star_z = np.random.uniform(-50, 50, 1000)
        star_size = np.random.uniform(0.5, 2, 1000)

        fig.add_trace(go.Scatter3d(
            x=star_x, y=star_y, z=star_z,
            mode='markers',
            marker=dict(
                size=star_size,
                color='white',
                opacity=0.7
            ),
            name='Stars',
            showlegend=False
        ))

        # Add planets with realistic orbits
        for planet_name, planet_data in self.planet_data.items():
            if planet_data['type'] == 'planet':
                a = planet_data['semi_major_axis'] / AU
                e = planet_data['eccentricity']
                inclination = np.radians(self.orbital_inclinations.get(planet_name, 0))

                # Generate realistic elliptical orbit
                theta = np.linspace(0, 2 * np.pi, 200)
                r = a * (1 - e ** 2) / (1 + e * np.cos(theta))

                # 3D coordinates with inclination
                x = r * np.cos(theta)
                y = r * np.sin(theta) * np.cos(inclination)
                z = r * np.sin(theta) * np.sin(inclination)

                # Add orbit
                fig.add_trace(go.Scatter3d(
                    x=x, y=y, z=z,
                    mode='lines',
                    line=dict(color=self.planet_colors[planet_name][0], width=4),
                    name=f"{planet_data['name']} Orbit",
                    showlegend=True
                ))

                # Add planet with realistic size
                planet_size = max(3, np.log(planet_data['radius'] / 1e7) * 8)
                fig.add_trace(go.Scatter3d(
                    x=[x[0]], y=[y[0]], z=[z[0]],
                    mode='markers',
                    marker=dict(
                        size=planet_size,
                        color=self.planet_colors[planet_name][1],
                        line=dict(color=self.planet_colors[planet_name][2], width=2)
                    ),
                    name=planet_data['name']
                ))

        # Add spectacular sun
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(
                size=20,
                color='#FFD700',
                opacity=0.9
            ),
            name='Sun'
        ))

        fig.update_layout(
            title='🌠 ULTRA-REALISTIC 3D SOLAR SYSTEM MASTERPIECE 🌠',
            scene=dict(
                xaxis_title='X (AU)',
                yaxis_title='Y (AU)',
                zaxis_title='Z (AU)',
                bgcolor='#0B0B3B',
                xaxis=dict(color='white'),
                yaxis=dict(color='white'),
                zaxis=dict(color='white'),
            ),
            width=1200,
            height=800,
            paper_bgcolor='#0B0B3B',
            font=dict(color='white')
        )

        return fig


def main():
    print("🌌 CREATING ULTRA-REALISTIC SOLAR SYSTEM MASTERPIECES...")
    print("✨ This will create stunning visualizations with outstanding colors! ✨")

    # Create solar system
    solar_system = SolarSystem()
    solar_system.simulate(time_span=365, n_steps=500)

    # Create ultra-realistic visualizer
    ultra_viz = UltraRealisticVisualizer(solar_system)

    print("1. 🎨 Creating Galactic Overview Dashboard...")
    fig1 = ultra_viz.create_galactic_overview()
    plt.savefig('ULTRA_REALISTIC_GALACTIC_OVERVIEW.png', dpi=300, bbox_inches='tight',
                facecolor='#0B0B3B', edgecolor='none')

    print("2. 🚀 Creating Interactive 3D Masterpiece...")
    fig2 = ultra_viz.create_interactive_3d_masterpiece()
    fig2.write_html('ULTRA_REALISTIC_3D_MASTERPIECE.html')

    print("\n🎉 ULTRA-REALISTIC VISUALIZATIONS COMPLETED! 🎉")
    print("📁 SPECTACULAR FILES GENERATED:")
    print("   🌟 ULTRA_REALISTIC_GALACTIC_OVERVIEW.png")
    print("   🌟 ULTRA_REALISTIC_3D_MASTERPIECE.html")
    print("\n🎨 FEATURES INCLUDED:")
    print("   ✅ Stunning gradient color schemes")
    print("   ✅ Realistic elliptical orbits with inclinations")
    print("   ✅ Beautiful starfield backgrounds")
    print("   ✅ Professional dashboard layout")
    print("   ✅ Size, velocity, temperature comparisons")
    print("   ✅ Composition and discovery timelines")
    print("   ✅ Interactive 3D visualization")

    plt.show()


if __name__ == "__main__":
    main()
