import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive window
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, RadioButtons, Slider
import numpy as np
import os
import importlib
import time

class InteractiveSortEditor:
    def __init__(self):
        self.data = []
        self.dark_mode = False
        self.array_size = 15
        self.max_value = 100
        self.sort_result = None

        # Setup figure and axes
        self.fig = plt.figure(figsize=(14, 10))
        self.array_ax = plt.axes([0.22, 0.23, 0.76, 0.70])

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
        # Position controls at the bottom now
        bottom_margin = 0.02
        control_height = 0.04
        control_width = 0.10
        spacing = 0.005

        # Calculate positions for bottom controls (left to right)
        x_start = 0.02

        # Title
        self.fig.text(0.60, 0.97, 'SORTING VISUALIZER', fontsize=14, fontweight='bold', ha='center')

        # Array size slider
        self.fig.text(x_start, bottom_margin + 0.11, 'Array Size:', fontsize=9, ha='left')
        self.size_slider_ax = plt.axes([x_start, bottom_margin + 0.07, control_width, 0.025])
        self.size_slider = Slider(self.size_slider_ax, '', 5, 50, valinit=self.array_size, valstep=1)
        self.size_slider.on_changed(self.update_array_size)

        # Max value slider
        x_pos = x_start + control_width + spacing
        self.fig.text(x_pos, bottom_margin + 0.11, 'Max Value:', fontsize=9, ha='left')
        self.max_slider_ax = plt.axes([x_pos, bottom_margin + 0.07, control_width, 0.025])
        self.max_slider = Slider(self.max_slider_ax, '', 10, 200, valinit=self.max_value, valstep=10)
        self.max_slider.on_changed(self.update_max_value)

        # Generate random array button
        x_pos = x_start + 2 * (control_width + spacing)
        self.btn_random = Button(plt.axes([x_pos, bottom_margin + 0.07, control_width, control_height]), 'Random Array')
        self.btn_random.on_clicked(self.generate_random_array)

        # Clear array button
        x_pos = x_start + 3 * (control_width + spacing)
        self.btn_clear = Button(plt.axes([x_pos, bottom_margin + 0.07, control_width, control_height]), 'Clear Array')
        self.btn_clear.on_clicked(self.clear_array)

        # Add value section
        x_pos = x_start + 4 * (control_width + spacing)
        self.fig.text(x_pos, bottom_margin + 0.12, 'Add Value:', fontsize=9, ha='left')
        self.value_input = TextBox(plt.axes([x_pos, bottom_margin + 0.07, control_width * 0.8, control_height]), '', initial='')

        x_pos = x_start + 4.8 * (control_width + spacing)
        self.btn_add_value = Button(plt.axes([x_pos, bottom_margin + 0.07, control_width * 0.6, control_height]), 'Add')
        self.btn_add_value.on_clicked(self.add_value)

        # Dark mode toggle
        x_pos = x_start + 5.6 * (control_width + spacing)
        self.btn_toggle_dark = Button(plt.axes([x_pos, bottom_margin + 0.07, control_width, control_height]), 'Dark Mode')
        self.btn_toggle_dark.on_clicked(self.toggle_dark_mode)

        # Load sorting algorithms dynamically
        self.sort_functions = {}
        script_dir = os.path.dirname(os.path.abspath(__file__))

        name_mappings = {
            'bubble': 'Bubble Sort',
            'selection': 'Selection Sort',
            'insertion': 'Insertion Sort',
            'merge': 'Merge Sort',
            'quick': 'Quick Sort',
            'heap': 'Heap Sort',
            'radix': 'Radix Sort',
            'counting': 'Counting Sort',
            'bucket': 'Bucket Sort',
            'shell': 'Shell Sort',
            'cocktailShaker': 'Cocktail Shaker Sort',
            'gnome': 'Gnome Sort',
            'comb': 'Comb Sort',
            'tim': 'Tim Sort',
            'stooge': 'Stooge Sort',
            'pancake': 'Pancake Sort',
            'oddEven': 'Odd-Even Sort',
            'cycle': 'Cycle Sort',
            'block': 'Block Sort',
            'strand': 'Strand Sort',
            'tree': 'Tree Sort',
            'cube': 'Cube Sort',
            'gravity': 'Gravity Sort',
            'pigeonhole': 'Pigeonhole Sort',
            'bogo': 'Bogo Sort',
            'sleep': 'Sleep Sort',
            'flash': 'Flash Sort',
        }

        for filename in os.listdir(script_dir):
            if filename.endswith('.py') and filename != 'editor.py' and not filename.startswith('_'):
                module_name = filename[:-3]
                try:
                    # Try importing with 'sorting.' prefix first, then without
                    try:
                        module = importlib.import_module(f'sorting.{module_name}')
                    except (ImportError, ModuleNotFoundError):
                        module = importlib.import_module(module_name)

                    if hasattr(module, 'sort'):
                        display_name = name_mappings.get(module_name, module_name.title() + ' Sort')
                        self.sort_functions[display_name] = module
                except Exception as e:
                    print(f"Failed to import {module_name}: {e}")

        # Radio buttons for algorithm selection (left side layout)
        sorted_algorithms = sorted(self.sort_functions.keys())

        # Create radio button widget on the left side
        self.algo_radio_ax = plt.axes([0.02, 0.25, 0.18, 0.70])
        self.algo_radio = RadioButtons(
            self.algo_radio_ax,
            tuple(sorted_algorithms) if sorted_algorithms else ('No algorithms',),
            active=0
        )

        # Store selected algorithm
        self.selected_algorithm = sorted_algorithms[0] if sorted_algorithms else 'No algorithms'

        # Connect radio button to update selection
        self.algo_radio.on_clicked(self.on_algo_selected)

        # Run sort button (at the bottom with other controls)
        x_pos = x_start + 6.7 * (control_width + spacing)
        self.btn_run_sort = Button(plt.axes([x_pos, bottom_margin + 0.07, control_width, control_height]), 'Run Sort')
        self.btn_run_sort.on_clicked(self.run_sort)

        # Status text (bottom, after Run Sort button)
        x_pos = x_start + 7.8 * (control_width + spacing)
        self.status_text = self.fig.text(x_pos/2, bottom_margin + 0.02, 'Ready', fontsize=9, ha='left', va='center', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))

        # Algorithm info text (bottom left)
        self.algo_info_text = self.fig.text(0.9, 0.15, '', fontsize=9, ha='center', va='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    def on_algo_selected(self, label):
        """Handle algorithm selection and update status"""
        self.selected_algorithm = label
        self.update_status(f"Selected: {label}")

    def update_array_size(self, val):
        self.array_size = int(val)
        self.update_status(f"Array size set to {self.array_size}")

    def update_max_value(self, val):
        self.max_value = int(val)
        self.update_status(f"Max value set to {self.max_value}")

    def generate_random_array(self, event):
        self.data = [np.random.randint(1, self.max_value + 1) for _ in range(self.array_size)]
        self.sort_result = None
        self.update_status(f"Generated random array of {self.array_size} elements")
        self.draw_array()

    def generate_reversed_array(self, event):
        self.data = list(range(self.array_size, 0, -1))
        self.sort_result = None
        self.update_status(f"Generated reversed array of {self.array_size} elements")
        self.draw_array()

    def clear_array(self, event):
        self.data = []
        self.sort_result = None
        self.update_status("Array cleared")
        self.draw_array()

    def add_value(self, event):
        try:
            value = int(self.value_input.text.strip())
            self.data.append(value)
            self.sort_result = None
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
            for widget in [self.value_input]:
                widget.ax.set_facecolor('#2d2d2d')
                widget.label.set_color('white')

            # Update buttons
            for btn in [self.btn_random, self.btn_clear, self.btn_add_value, self.btn_toggle_dark, self.btn_run_sort]:
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
            for widget in [self.value_input]:
                widget.ax.set_facecolor('white')
                widget.label.set_color('black')

            # Update buttons
            for btn in [self.btn_random, self.btn_clear, self.btn_add_value, self.btn_toggle_dark, self.btn_run_sort]:
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

    def run_sort(self, event):
        if not self.data:
            self.update_status("Array is empty")
            return

        selected_algo = self.selected_algorithm
        if selected_algo == 'No algorithms':
            self.update_status("No sorting algorithms available")
            return

        algo_module = self.sort_functions[selected_algo]

        try:
            # Run the sort
            start_time = time.time()
            result = algo_module.sort(self.data.copy())
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds

            self.sort_result = result
            self.update_status(f"{selected_algo}: Sorted array in {elapsed_time:.2f}ms")

            # Display algorithm info
            time_complexity = getattr(algo_module, 'timeComplexity', 'N/A')
            space_complexity = getattr(algo_module, 'spaceComplexity', 'N/A')
            variant_of = getattr(algo_module, 'variantOf', '')

            info_text = f"{selected_algo}\nTime: {time_complexity}\nSpace: {space_complexity}"
            if variant_of:
                info_text += f"\nVariant of: {variant_of}"

            self.algo_info_text.set_text(info_text)

            self.draw_array()

        except Exception as e:
            self.update_status(f"Error during sort: {str(e)}")

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
            sorted_color = '#00ff00'
        else:
            self.array_ax.set_facecolor('#f8f9fa')
            text_color = 'black'
            bar_color = '#007bff'
            sorted_color = '#00ff00'

        if not self.data:
            self.array_ax.set_title('Array Visualization (Empty)', fontsize=14, color=text_color)
            self.array_ax.set_xlim(0, 1)
            self.array_ax.set_ylim(0, 1)
            self.array_ax.text(0.5, 0.5, 'Array is empty\nGenerate or add values', ha='center', va='center', fontsize=12, color=text_color)
        else:
            # Determine which array to display
            display_data = self.sort_result if self.sort_result is not None else self.data
            is_sorted = self.sort_result is not None

            # Create bar chart
            indices = range(len(display_data))
            colors = [sorted_color if is_sorted else bar_color] * len(display_data)

            bars = self.array_ax.bar(indices, display_data, color=colors, edgecolor=text_color, linewidth=1)

            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, display_data)):
                height = bar.get_height()
                self.array_ax.text(bar.get_x() + bar.get_width()/2., height,
                                 f'{value}',
                                 ha='center', va='bottom', fontsize=8, color=text_color)

                # Add index labels below bars
                self.array_ax.text(bar.get_x() + bar.get_width()/2., -max(display_data) * 0.05,
                                 f'[{i}]',
                                 ha='center', va='top', fontsize=7, color=text_color, alpha=0.7)

            # Set labels and title
            sorted_status = " (SORTED)" if is_sorted else ""
            title = f'Array Visualization{sorted_status} - Size: {len(display_data)}'

            self.array_ax.set_title(title, fontsize=14, color=text_color, pad=10)
            self.array_ax.set_xlabel('Index', fontsize=10, color=text_color)
            self.array_ax.set_ylabel('Value', fontsize=10, color=text_color)

            # Style
            self.array_ax.tick_params(colors=text_color)
            for spine in self.array_ax.spines.values():
                spine.set_color(text_color)

            # Set y-axis to start from 0
            self.array_ax.set_ylim(bottom=-max(display_data) * 0.1, top=max(display_data) * 1.15)

        # Update algorithm info box theme
        if self.dark_mode:
            self.algo_info_text.set_bbox(dict(boxstyle='round', facecolor='#2d2d2d', edgecolor='#444', alpha=0.8))
            self.algo_info_text.set_color('white')
        else:
            self.algo_info_text.set_bbox(dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            self.algo_info_text.set_color('black')

        self.fig.canvas.draw_idle()

if __name__ == "__main__":
    editor = InteractiveSortEditor()
