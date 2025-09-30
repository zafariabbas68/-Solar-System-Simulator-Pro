import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from data.constants import G, AU  # Added import for G and AU

class SolarSystemStatistics:
    def __init__(self, solar_system):
        self.solar_system = solar_system
        
    def calculate_orbital_statistics(self):
        """Calculate comprehensive orbital statistics"""
        planets_data = []
        
        for body in self.solar_system.bodies:
            if body.type == 'planet':
                # Calculate orbital energy and angular momentum
                sun = self.solar_system.get_sun()
                if sun:
                    r = np.linalg.norm(body.position - sun.position)
                    v = np.linalg.norm(body.velocity)
                    
                    # Orbital energy per unit mass
                    energy = 0.5 * v**2 - G * sun.mass / r
                    
                    # Specific angular momentum
                    r_vec = body.position - sun.position
                    v_vec = body.velocity
                    angular_momentum = np.linalg.norm(np.cross(r_vec, v_vec))
                    
                    planets_data.append({
                        'name': body.name,
                        'semi_major_axis': body.semi_major_axis,
                        'eccentricity': body.eccentricity,
                        'orbital_period': body.orbital_period,
                        'mass': body.mass,
                        'radius': body.radius,
                        'orbital_energy': energy,
                        'angular_momentum': angular_momentum,
                        'orbital_speed': v
                    })
        
        return pd.DataFrame(planets_data)
    
    def keplers_law_verification(self):
        """Verify Kepler's third law"""
        df = self.calculate_orbital_statistics()
        
        # Kepler's third law: T² ∝ a³
        T = df['orbital_period']  # in days
        a = df['semi_major_axis'] / AU  # in AU
        
        # Calculate ratio T²/a³
        ratio = (T**2) / (a**3)
        
        plt.figure(figsize=(10, 6))
        plt.bar(df['name'], ratio, color='skyblue')
        plt.axhline(y=1, color='red', linestyle='--', label='Ideal ratio = 1')
        plt.title("Verification of Kepler's Third Law (T²/a³)")
        plt.ylabel('T² / a³')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        
        return ratio
    
    def orbital_energy_analysis(self):
        """Analyze orbital energies"""
        df = self.calculate_orbital_statistics()
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Orbital energy vs semi-major axis
        axes[0].scatter(df['semi_major_axis'] / AU, 
                       df['orbital_energy'], s=100, c='red')
        axes[0].set_xlabel('Semi-Major Axis (AU)')
        axes[0].set_ylabel('Orbital Energy (J/kg)')
        axes[0].set_title('Orbital Energy vs Semi-Major Axis')
        axes[0].grid(True, alpha=0.3)
        
        # Add planet labels
        for i, name in enumerate(df['name']):
            axes[0].annotate(name, 
                           (df['semi_major_axis'].iloc[i] / AU, 
                            df['orbital_energy'].iloc[i]),
                           xytext=(5, 5), textcoords='offset points')
        
        # Angular momentum distribution
        axes[1].bar(df['name'], df['angular_momentum'], color='lightgreen')
        axes[1].set_title('Specific Angular Momentum')
        axes[1].set_ylabel('Angular Momentum (m²/s)')
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig
    
    def planetary_comparison_table(self):
        """Create a comprehensive comparison table"""
        df = self.calculate_orbital_statistics()
        
        # Create normalized values for comparison
        df['mass_relative'] = df['mass'] / df['mass'].max()
        df['radius_relative'] = df['radius'] / df['radius'].max()
        df['semi_major_axis_relative'] = df['semi_major_axis'] / df['semi_major_axis'].max()
        
        # Display the table
        display_columns = ['name', 'mass', 'radius', 'semi_major_axis', 
                          'orbital_period', 'eccentricity', 'orbital_speed']
        
        styled_df = df[display_columns].style \
            .format({
                'mass': '{:.2e}',
                'radius': '{:.0f}',
                'semi_major_axis': '{:.2e}',
                'orbital_period': '{:.2f}',
                'eccentricity': '{:.3f}',
                'orbital_speed': '{:.2f}'
            }) \
            .background_gradient(subset=['mass', 'radius'], cmap='Blues') \
            .background_gradient(subset=['orbital_speed'], cmap='Reds')
        
        return styled_df
    
    def correlation_analysis(self):
        """Perform correlation analysis between planetary properties"""
        df = self.calculate_orbital_statistics()
        
        # Select numerical columns for correlation
        numerical_cols = ['mass', 'radius', 'semi_major_axis', 'orbital_period', 
                         'eccentricity', 'orbital_energy', 'angular_momentum']
        
        correlation_matrix = df[numerical_cols].corr()
        
        # Plot correlation heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)
        
        # Add correlation values as text
        for i in range(len(numerical_cols)):
            for j in range(len(numerical_cols)):
                text = ax.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}',
                              ha="center", va="center", color="black")
        
        ax.set_xticks(range(len(numerical_cols)))
        ax.set_yticks(range(len(numerical_cols)))
        ax.set_xticklabels(numerical_cols, rotation=45)
        ax.set_yticklabels(numerical_cols)
        ax.set_title('Correlation Matrix of Planetary Properties')
        
        plt.colorbar(im)
        plt.tight_layout()
        
        return correlation_matrix
