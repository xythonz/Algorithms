import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, RadioButtons, Slider
import numpy as np
import os
import importlib
import time

class InteractiveSearchEditor:
    def __init__(self):
        self.data = []
        self.target = None
        self.dark_mode = False
        self.array_size = 15
        self.max_value = 100
        self.is_sorted = False
        self.search_result = None
        self.highlighted_indices = []

        # Setup figure and axes
        self.fig = plt.figure(figsize=(14, 10))
        self.array_ax = plt.axes([0.22, 0.25, 0.73, 0.65])

        # Setup controls
        self.setup_controls()

        # Apply theme
        self.apply_theme()

        # Generate initial random array
        self.generate_random_array(None)

        # Draw initial visualization
        self.draw_array()

        plt.show()

    def setup_controls(self):
        left_margin = 0.02
        control_width = 0.16
        start_y = 0.90
        control_height = 0.04
        spacing = 0.06

        # Title
        self.fig.text(left_margin + control_width/2, 0.96, 'SEARCH VISUALIZER', fontsize=14, fontweight='bold', ha='center')

        # Array size slider
        self.fig.text(left_margin, start_y, 'Array Size:', fontsize=10, ha='left')
        self.size_slider_ax = plt.axes([left_margin, start_y - 0.05, control_width, 0.03])
        self.size_slider = Slider(self.size_slider_ax, '', 5, 50, valinit=self.array_size, valstep=1)
        self.size_slider.on_changed(self.update_array_size)

        # Max value slider
        self.fig.text(left_margin, start_y - 0.10, 'Max Value:', fontsize=10, ha='left')
        self.max_slider_ax = plt.axes([left_margin, start_y - 0.15, control_width, 0.03])
        self.max_slider = Slider(self.max_slider_ax, '', 10, 200, valinit=self.max_value, valstep=10)
        self.max_slider.on_changed(self.update_max_value)

        # Generate random array button
        self.btn_random = Button(plt.axes([left_margin, start_y - 0.21, control_width, control_height]), 'Random Array')
        self.btn_random.on_clicked(self.generate_random_array)

        # Sort array button
        self.btn_sort = Button(plt.axes([left_margin, start_y - 0.27, control_width, control_height]), 'Sort Array')
        self.btn_sort.on_clicked(self.sort_array)

        # Clear array button
        self.btn_clear = Button(plt.axes([left_margin, start_y - 0.33, control_width, control_height]), 'Clear Array')
        self.btn_clear.on_clicked(self.clear_array)

        # Target value input
        self.fig.text(left_margin, start_y - 0.40, 'Target Value:', fontsize=10, ha='left')
        self.target_input = TextBox(plt.axes([left_margin, start_y - 0.45, control_width, control_height]), '', initial='')
        self.target_input.on_submit(self.update_target)

        # Add value button
        self.fig.text(left_margin, start_y - 0.52, 'Add Value:', fontsize=10, ha='left')
        self.value_input = TextBox(plt.axes([left_margin, start_y - 0.57, control_width, control_height]), '', initial='')
        self.btn_add_value = Button(plt.axes([left_margin, start_y - 0.63, control_width, control_height]), 'Add to Array')
        self.btn_add_value.on_clicked(self.add_value)

        # Dark mode toggle
        self.btn_toggle_dark = Button(plt.axes([left_margin, start_y - 0.69, control_width, control_height]), 'Dark Mode')
        self.btn_toggle_dark.on_clicked(self.toggle_dark_mode)

        # Load search algorithms dynamically
        self.search_functions = {}
        script_dir = os.path.dirname(os.path.abspath(__file__))

        name_mappings = {
            'linear': 'Linear Search',
            'binary': 'Binary Search',
            'jump': 'Jump Search',
            'interpolation': 'Interpolation Search',
            'exponential': 'Exponential Search',
        }

        for filename in os.listdir(script_dir):
            if filename.endswith('.py') and filename != 'editor.py' and not filename.startswith('_'):
                module_name = filename[:-3]
                try:
                    # Try importing with 'search.' prefix first, then without
                    try:
                        module = importlib.import_module(f'search.{module_name}')
                    except (ImportError, ModuleNotFoundError):
                        module = importlib.import_module(module_name)

                    if hasattr(module, 'search'):
                        display_name = name_mappings.get(module_name, module_name.title() + ' Search')
                        self.search_functions[display_name] = module
                except Exception as e:
                    print(f"Failed to import {module_name}: {e}")

        # Radio buttons for algorithm selection
        radio_left = left_margin + control_width + 0.02
        self.algo_radio_ax = plt.axes([radio_left, 0.70, control_width, 0.25])
        sorted_algorithms = sorted(self.search_functions.keys())
        self.algo_radio = RadioButtons(self.algo_radio_ax, tuple(sorted_algorithms) if sorted_algorithms else ('No algorithms',), active=0)

        # Run search button
        self.btn_run_search = Button(plt.axes([radio_left, 0.64, control_width, control_height]), 'Run Search')
        self.btn_run_search.on_clicked(self.run_search)

        # Status text
        self.status_text = self.fig.text((left_margin + control_width/2)+0.5, 0.01, 'Ready', fontsize=10, ha='center', va='bottom', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))

        # Algorithm info text
        self.algo_info_text = self.fig.text(0.59, 0.18, '', fontsize=9, ha='center', va='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    def update_array_size(self, val):
        self.array_size = int(val)
        self.update_status(f"Array size set to {self.array_size}")

    def update_max_value(self, val):
        self.max_value = int(val)
        self.update_status(f"Max value set to {self.max_value}")

    def generate_random_array(self, event):
        self.data = [np.random.randint(1, self.max_value + 1) for _ in range(self.array_size)]
        self.search_result = None
        self.highlighted_indices = []
        self.is_sorted = False
        self.update_status(f"Generated random array of {self.array_size} elements")
        self.draw_array()

    def sort_array(self, event):
        if not self.data:
            self.update_status("Array is empty")
            return
        self.data.sort()
        self.is_sorted = True
        self.search_result = None
        self.highlighted_indices = []
        self.update_status("Array sorted")
        self.draw_array()

    def clear_array(self, event):
        self.data = []
        self.search_result = None
        self.highlighted_indices = []
        self.is_sorted = False
        self.update_status("Array cleared")
        self.draw_array()

    def update_target(self, text):
        try:
            self.target = int(text.strip())
            self.update_status(f"Target set to {self.target}")
        except ValueError:
            self.update_status("Invalid target value")
            self.target = None

    def add_value(self, event):
        try:
            value = int(self.value_input.text.strip())
            self.data.append(value)
            self.search_result = None
            self.highlighted_indices = []
            self.is_sorted = False
            self.update_status(f"Added {value} to array")
            self.value_input.set_val('')
            self.draw_array()
        except ValueError:
            self.update_status("Invalid value")

    def toggle_dark_mode(self, event):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.draw_array()

    def apply_theme(self):
        if self.dark_mode:
            self.fig.patch.set_facecolor('#121212')
            self.array_ax.set_facecolor('#1e1e1e')

            # Update all text elements
            for text in self.fig.texts:
                text.set_color('white')

            # Update input boxes
            for widget in [self.target_input, self.value_input]:
                widget.ax.set_facecolor('#2d2d2d')
                widget.label.set_color('white')

            # Update buttons
            for btn in [self.btn_random, self.btn_sort, self.btn_clear, self.btn_add_value, self.btn_toggle_dark, self.btn_run_search]:
                btn.color = '#2d2d2d'
                btn.hovercolor = '#3d3d3d'
                btn.label.set_color('white')

            self.btn_toggle_dark.label.set_text('Light Mode')

            # Update radio buttons
            self.algo_radio_ax.set_facecolor('#2d2d2d')
            for label in self.algo_radio.labels:
                label.set_color('white')

            # Update sliders
            self.size_slider_ax.set_facecolor('#2d2d2d')
            self.max_slider_ax.set_facecolor('#2d2d2d')

        else:
            self.fig.patch.set_facecolor('white')
            self.array_ax.set_facecolor('#f8f9fa')

            # Update all text elements
            for text in self.fig.texts:
                text.set_color('black')

            # Update input boxes
            for widget in [self.target_input, self.value_input]:
                widget.ax.set_facecolor('white')
                widget.label.set_color('black')

            # Update buttons
            for btn in [self.btn_random, self.btn_sort, self.btn_clear, self.btn_add_value, self.btn_toggle_dark, self.btn_run_search]:
                btn.color = '0.85'
                btn.hovercolor = '0.95'
                btn.label.set_color('black')

            self.btn_toggle_dark.label.set_text('Dark Mode')

            # Update radio buttons
            self.algo_radio_ax.set_facecolor('white')
            for label in self.algo_radio.labels:
                label.set_color('black')

            # Update sliders
            self.size_slider_ax.set_facecolor('white')
            self.max_slider_ax.set_facecolor('white')

        self.fig.canvas.draw_idle()

    def run_search(self, event):
        if not self.data:
            self.update_status("Array is empty")
            return

        if self.target is None:
            self.update_status("Please set a target value")
            return

        selected_algo = self.algo_radio.value_selected
        if selected_algo == 'No algorithms':
            self.update_status("No search algorithms available")
            return

        algo_module = self.search_functions[selected_algo]

        # Check if algorithm requires sorted array
        algorithms_requiring_sorted = ['Binary Search', 'Jump Search', 'Interpolation Search', 'Exponential Search']
        if selected_algo in algorithms_requiring_sorted and not self.is_sorted:
            self.update_status(f"{selected_algo} needs array to be sorted")
            return

        try:
            # Run the search
            result = algo_module.search(self.data.copy(), self.target)
            self.search_result = result

            if result != -1:
                self.highlighted_indices = [result]
                self.update_status(f"{selected_algo}: Found {self.target} at index {result}")
            else:
                self.highlighted_indices = []
                self.update_status(f"{selected_algo}: {self.target} not found in array")

            # Display algorithm info
            time_complexity = getattr(algo_module, 'timeComplexity', 'N/A')
            space_complexity = getattr(algo_module, 'spaceComplexity', 'N/A')
            info_text = f"{selected_algo}\nTime: {time_complexity}\nSpace: {space_complexity}"
            self.algo_info_text.set_text(info_text)

            self.draw_array()

        except Exception as e:
            self.update_status(f"Error during search: {str(e)}")

    def update_status(self, message):
        self.status_text.set_text(message)
        if self.dark_mode:
            self.status_text.set_bbox(dict(boxstyle='round', facecolor='#2d2d2d', edgecolor='#444', alpha=0.8))
            self.status_text.set_color('white')
        else:
            self.status_text.set_bbox(dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
            self.status_text.set_color('black')
        self.fig.canvas.draw_idle()

    def draw_array(self):
        self.array_ax.clear()

        # Set theme colors
        if self.dark_mode:
            self.array_ax.set_facecolor('#1e1e1e')
            text_color = 'white'
            bar_color = '#4dabf7'
            highlight_color = '#ff0000'
            target_color = '#00ff00'
        else:
            self.array_ax.set_facecolor('#f8f9fa')
            text_color = 'black'
            bar_color = '#007bff'
            highlight_color = '#ff0000'
            target_color = '#00ff00'

        if not self.data:
            self.array_ax.set_title('Array Visualization (Empty)', fontsize=14, color=text_color)
            self.array_ax.set_xlim(0, 1)
            self.array_ax.set_ylim(0, 1)
            self.array_ax.text(0.5, 0.5, 'Array is empty\nGenerate or add values', ha='center', va='center', fontsize=12, color=text_color)
        else:
            # Create bar chart
            indices = range(len(self.data))
            colors = []

            for i in indices:
                if i in self.highlighted_indices:
                    colors.append(highlight_color)
                elif self.target is not None and self.data[i] == self.target:
                    colors.append(target_color)
                else:
                    colors.append(bar_color)

            bars = self.array_ax.bar(indices, self.data, color=colors, edgecolor=text_color, linewidth=1)

            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, self.data)):
                height = bar.get_height()
                self.array_ax.text(bar.get_x() + bar.get_width()/2., height,
                                 f'{value}',
                                 ha='center', va='bottom', fontsize=8, color=text_color)

                # Add index labels below bars
                self.array_ax.text(bar.get_x() + bar.get_width()/2., -max(self.data) * 0.05,
                                 f'[{i}]',
                                 ha='center', va='top', fontsize=7, color=text_color, alpha=0.7)

            # Set labels and title
            sorted_status = " (SORTED)" if self.is_sorted else ""
            title = f'Array Visualization{sorted_status} - Size: {len(self.data)}'
            if self.target is not None:
                title += f' | Target: {self.target}'

            self.array_ax.set_title(title, fontsize=14, color=text_color, pad=10)
            self.array_ax.set_xlabel('Index', fontsize=10, color=text_color)
            self.array_ax.set_ylabel('Value', fontsize=10, color=text_color)

            # Style
            self.array_ax.tick_params(colors=text_color)
            for spine in self.array_ax.spines.values():
                spine.set_color(text_color)

            # Set y-axis to start from 0
            self.array_ax.set_ylim(bottom=-max(self.data) * 0.1, top=max(self.data) * 1.15)

        # Update algorithm info box theme
        if self.dark_mode:
            self.algo_info_text.set_bbox(dict(boxstyle='round', facecolor='#2d2d2d', edgecolor='#444', alpha=0.8))
            self.algo_info_text.set_color('white')
        else:
            self.algo_info_text.set_bbox(dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            self.algo_info_text.set_color('black')

        self.fig.canvas.draw_idle()

if __name__ == "__main__":
    editor = InteractiveSearchEditor()
