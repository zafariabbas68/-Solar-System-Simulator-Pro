import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from solar_system import SolarSystem
from visualization import SolarSystemVisualizer
from statistics import SolarSystemStatistics


class SolarSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solar System Simulator")
        self.root.geometry("1200x800")

        # Initialize solar system
        self.solar_system = SolarSystem()

        # Run simulation
        print("Running simulation...")
        self.solar_system.simulate(time_span=365 * 2, n_steps=1000)  # 2 years

        # Initialize visualizer and statistics
        self.visualizer = SolarSystemVisualizer(self.solar_system)
        self.statistics = SolarSystemStatistics(self.solar_system)

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab 1: Solar System View
        self.setup_solar_system_tab(notebook)

        # Tab 2: Statistics
        self.setup_statistics_tab(notebook)

        # Tab 3: 3D Visualization
        self.setup_3d_tab(notebook)

    def setup_solar_system_tab(self, notebook):
        """Setup solar system visualization tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Solar System")

        # Create matplotlib figure
        self.fig, self.ax = self.visualizer.create_static_plot()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(self.fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill='x', pady=10)

        ttk.Button(control_frame, text="Refresh",
                   command=self.refresh_plot).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Create Animation",
                   command=self.create_animation).pack(side='left', padx=5)

    def setup_statistics_tab(self, notebook):
        """Setup statistics tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Statistics")

        # Create comparison plots
        fig = self.visualizer.create_comparison_plots()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Additional statistics buttons
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill='x', pady=10)

        ttk.Button(control_frame, text="Orbital Energy Analysis",
                   command=self.show_energy_analysis).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Correlation Analysis",
                   command=self.show_correlation).pack(side='left', padx=5)

    def setup_3d_tab(self, notebook):
        """Setup 3D visualization tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="3D View")

        label = ttk.Label(frame, text="3D visualization would open in browser")
        label.pack(pady=20)

        ttk.Button(frame, text="Open 3D Visualization",
                   command=self.open_3d_visualization).pack(pady=10)

    def refresh_plot(self):
        """Refresh the solar system plot"""
        self.fig, self.ax = self.visualizer.create_static_plot()
        plt.show()

    def create_animation(self):
        """Create and save animation"""
        print("Creating animation...")
        self.visualizer.create_animation(save_path='solar_system_animation.gif')
        print("Animation saved as 'solar_system_animation.gif'")

    def show_energy_analysis(self):
        """Show orbital energy analysis"""
        self.statistics.orbital_energy_analysis()
        plt.show()

    def show_correlation(self):
        """Show correlation analysis"""
        self.statistics.correlation_analysis()
        plt.show()

    def open_3d_visualization(self):
        """Open 3D visualization in browser"""
        fig = self.visualizer.create_3d_plotly_visualization()
        fig.show()


def main():
    # Option 1: Run with GUI
    root = tk.Tk()
    app = SolarSystemApp(root)
    root.mainloop()

    # Option 2: Run without GUI (uncomment below)
    # run_demo()


def run_demo():
    """Run a demonstration without GUI"""
    print("Initializing Solar System...")
    solar_system = SolarSystem()

    print("Running simulation...")
    solar_system.simulate(time_span=365 * 2, n_steps=1000)

    print("Creating visualizations...")
    visualizer = SolarSystemVisualizer(solar_system)

    # Create static plots
    fig, ax = visualizer.create_static_plot()
    plt.savefig('solar_system_static.png', dpi=300, bbox_inches='tight')

    # Create comparison plots
    fig2 = visualizer.create_comparison_plots()
    plt.savefig('planetary_comparison.png', dpi=300, bbox_inches='tight')

    # Create 3D visualization
    fig3 = visualizer.create_3d_plotly_visualization()
    fig3.write_html('solar_system_3d.html')

    # Generate statistics
    stats = SolarSystemStatistics(solar_system)
    stats.keplers_law_verification()
    plt.savefig('keplers_law.png', dpi=300, bbox_inches='tight')

    stats.orbital_energy_analysis()
    plt.savefig('orbital_energy.png', dpi=300, bbox_inches='tight')

    print("All visualizations saved!")
    plt.show()


if __name__ == "__main__":
    main()