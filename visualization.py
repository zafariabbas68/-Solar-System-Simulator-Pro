import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.animation as animation
from data.constants import AU


class SolarSystemVisualizer:
    def __init__(self, solar_system):
        self.solar_system = solar_system
        self.fig = None
        self.ax = None

    def create_static_plot(self, time_index=-1):
        """Create a static plot of the solar system"""
        fig, ax = plt.subplots(1, 2, figsize=(20, 8))

        # Update bodies to specified time
        self.solar_system.update_bodies_from_solution(time_index)

        # Plot 1: Solar System View
        self._plot_solar_system_view(ax[0])

        # Plot 2: Orbital Parameters
        self._plot_orbital_parameters(ax[1])

        plt.tight_layout()
        return fig, ax

    def _plot_solar_system_view(self, ax):
        """Plot the solar system view"""
        ax.set_title('Solar System', fontsize=16, fontweight='bold')
        ax.set_xlabel('Distance (AU)')
        ax.set_ylabel('Distance (AU)')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')

        # Plot orbits and current positions
        for i, body in enumerate(self.solar_system.bodies):
            if body.type == 'planet':
                # Plot orbit trajectory
                trajectory = self.solar_system.get_body_trajectory(i)
                trajectory_au = trajectory / AU
                ax.plot(trajectory_au[:, 0], trajectory_au[:, 1],
                        color=body.color, alpha=0.5, linewidth=1)

                # Plot current position
                current_pos = body.position / AU
                ax.scatter(current_pos[0], current_pos[1],
                           color=body.color, s=100, label=body.name,
                           edgecolors='black', linewidth=0.5)

        # Plot sun
        sun = self.solar_system.get_sun()
        if sun:
            sun_pos = sun.position / AU
            ax.scatter(sun_pos[0], sun_pos[1], color=sun.color, s=300,
                       label=sun.name, edgecolors='black', linewidth=1)

        ax.legend()
        ax.set_xlim(-35, 35)
        ax.set_ylim(-35, 35)

    def _plot_orbital_parameters(self, ax):
        """Plot orbital parameters comparison"""
        planets_data = []
        for body in self.solar_system.bodies:
            if body.type == 'planet':
                planets_data.append({
                    'name': body.name,
                    'semi_major_axis': body.semi_major_axis / AU,
                    'orbital_period': body.orbital_period,
                    'eccentricity': body.eccentricity,
                    'color': body.color
                })

        names = [p['name'] for p in planets_data]
        semi_major_axes = [p['semi_major_axis'] for p in planets_data]
        orbital_periods = [p['orbital_period'] for p in planets_data]
        eccentricities = [p['eccentricity'] for p in planets_data]
        colors = [p['color'] for p in planets_data]

        bars = ax.bar(names, semi_major_axes, color=colors, alpha=0.7)
        ax.set_title('Planetary Semi-Major Axes', fontsize=16, fontweight='bold')
        ax.set_ylabel('Semi-Major Axis (AU)')
        ax.tick_params(axis='x', rotation=45)

        # Add value labels on bars
        for bar, value in zip(bars, semi_major_axes):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                    f'{value:.1f}', ha='center', va='bottom')

    def create_3d_plotly_visualization(self):
        """Create an interactive 3D visualization using Plotly"""
        fig = go.Figure()

        # Add orbits and planets
        for i, body in enumerate(self.solar_system.bodies):
            if body.type == 'planet':
                trajectory = self.solar_system.get_body_trajectory(i)
                trajectory_au = trajectory / AU

                # Add orbit trace
                fig.add_trace(go.Scatter3d(
                    x=trajectory_au[:, 0],
                    y=trajectory_au[:, 1],
                    z=trajectory_au[:, 2],
                    mode='lines',
                    line=dict(color=body.color, width=2),
                    name=f"{body.name} Orbit",
                    showlegend=False
                ))

                # Add current position
                current_pos = body.position / AU
                fig.add_trace(go.Scatter3d(
                    x=[current_pos[0]],
                    y=[current_pos[1]],
                    z=[current_pos[2]],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=body.color,
                        line=dict(color='black', width=1)
                    ),
                    name=body.name
                ))

        # Add sun
        sun = self.solar_system.get_sun()
        if sun:
            sun_pos = sun.position / AU
            fig.add_trace(go.Scatter3d(
                x=[sun_pos[0]],
                y=[sun_pos[1]],
                z=[sun_pos[2]],
                mode='markers',
                marker=dict(
                    size=15,
                    color=sun.color,
                    line=dict(color='black', width=2)
                ),
                name=sun.name
            ))

        fig.update_layout(
            title='3D Solar System Visualization',
            scene=dict(
                xaxis_title='X (AU)',
                yaxis_title='Y (AU)',
                zaxis_title='Z (AU)',
                aspectmode='cube'
            ),
            width=800,
            height=600
        )

        return fig

    def create_animation(self, save_path=None):
        """Create an animation of the solar system"""
        fig, ax = plt.subplots(figsize=(10, 10))

        def animate(frame):
            ax.clear()
            self.solar_system.update_bodies_from_solution(frame)
            self._plot_solar_system_view(ax)
            ax.set_title(f'Solar System - Time: {self.solar_system.simulation_time[frame]:.1f} days')

        n_frames = len(self.solar_system.simulation_time)
        anim = animation.FuncAnimation(
            fig, animate, frames=min(100, n_frames), interval=50, repeat=True
        )

        if save_path:
            anim.save(save_path, writer='pillow', fps=20)

        return anim

    def create_comparison_plots(self):
        """Create multiple comparison plots"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()

        planets_data = []
        for body in self.solar_system.bodies:
            if body.type == 'planet':
                planets_data.append({
                    'name': body.name,
                    'mass': body.mass,
                    'radius': body.radius,
                    'semi_major_axis': body.semi_major_axis / AU,
                    'orbital_period': body.orbital_period,
                    'eccentricity': body.eccentricity,
                    'color': body.color
                })

        names = [p['name'] for p in planets_data]

        # Mass comparison
        masses = [p['mass'] for p in planets_data]
        axes[0].bar(names, np.log10(masses), color=[p['color'] for p in planets_data])
        axes[0].set_title('Planetary Masses (log scale)')
        axes[0].set_ylabel('log10(Mass kg)')
        axes[0].tick_params(axis='x', rotation=45)

        # Radius comparison
        radii = [p['radius'] / 1000 for p in planets_data]  # Convert to km
        axes[1].bar(names, radii, color=[p['color'] for p in planets_data])
        axes[1].set_title('Planetary Radii')
        axes[1].set_ylabel('Radius (km)')
        axes[1].tick_params(axis='x', rotation=45)

        # Orbital period vs semi-major axis
        semi_major_axes = [p['semi_major_axis'] for p in planets_data]
        orbital_periods = [p['orbital_period'] for p in planets_data]
        colors = [p['color'] for p in planets_data]

        scatter = axes[2].scatter(semi_major_axes, orbital_periods, c=colors, s=100)
        axes[2].set_title("Kepler's Third Law")
        axes[2].set_xlabel('Semi-Major Axis (AU)')
        axes[2].set_ylabel('Orbital Period (days)')

        # Add labels to points
        for i, name in enumerate(names):
            axes[2].annotate(name, (semi_major_axes[i], orbital_periods[i]),
                             xytext=(5, 5), textcoords='offset points')

        # Eccentricity comparison
        eccentricities = [p['eccentricity'] for p in planets_data]
        axes[3].bar(names, eccentricities, color=colors)
        axes[3].set_title('Planetary Orbital Eccentricities')
        axes[3].set_ylabel('Eccentricity')
        axes[3].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        return fig