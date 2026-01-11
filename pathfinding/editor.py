import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, RadioButtons
import numpy as np
import matplotlib.cm as cm
import os
import importlib

class InteractiveGraphEditor:
    def __init__(self):
        self.graph = {}
        self.pos = {}
        self.dark_mode = False
        self.dragging_node = None
        self.creating_edge = False
        self.edge_start_node = None
        self.current_weight = 1.0
        self.current_node_name = "A"
        self.fig = plt.figure(figsize=(14, 10))
        self.graph_ax = plt.axes([0.22, 0.05, 0.73, 0.90])
        self.cmap = cm.viridis
        self.norm = plt.Normalize(vmin=0, vmax=1)
        self.sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=self.norm)
        self.sm.set_array([])
        self.colorbar = self.fig.colorbar(self.sm, ax=self.graph_ax, orientation='vertical', fraction=0.05, pad=0.02)
        self.colorbar.set_label('Edge Weight', fontsize=10)
        self.colorbar.ax.tick_params(labelsize=8)
        self.start_node = None
        self.goal_node = None
        self.current_path = None
        self.setup_controls()
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.in_navigation_mode = False
        self.apply_theme()
        self.draw_graph()
        plt.show()
    
    def setup_controls(self):
        left_margin = 0.02
        control_width = 0.16
        start_y = 0.90
        control_height = 0.04
        spacing = 0.06
        self.fig.text(left_margin + control_width/2, 0.96, 'GRAPH EDITOR', fontsize=14, fontweight='bold', ha='center')
        self.fig.text(left_margin, start_y+0.01, 'Node Name:', fontsize=10, ha='left')
        self.node_name_input = TextBox(plt.axes([left_margin, start_y - 0.04, control_width, 0.04]), '', initial=self.current_node_name)
        self.node_name_input.on_submit(self.update_node_name)
        self.btn_add_node = Button(plt.axes([left_margin, start_y - 0.10, control_width, control_height]), 'Add Node')
        self.btn_add_node.on_clicked(self.add_node_click)
        self.fig.text(left_margin, start_y - 0.15, 'Edge Weight:', fontsize=10, ha='left')
        self.edge_weight_input = TextBox(plt.axes([left_margin, start_y - 0.20, control_width, control_height]), '', initial=str(self.current_weight))
        self.edge_weight_input.on_submit(self.update_weight)
        self.btn_add_edge = Button(plt.axes([left_margin, start_y - 0.26, control_width, control_height]), 'Start Edge')
        self.btn_add_edge.on_clicked(self.start_edge_creation)
        self.btn_cancel_edge = Button(plt.axes([left_margin, start_y - 0.32, control_width, control_height]), 'Cancel Edge')
        self.btn_cancel_edge.on_clicked(self.cancel_edge_creation)
        self.fig.add_artist(plt.Line2D([left_margin, left_margin + control_width], [start_y - 0.36, start_y - 0.36], color='black', alpha=0.3))
        self.btn_toggle_dark = Button(plt.axes([left_margin, start_y - 0.40, control_width, control_height]), 'Dark Mode')
        self.btn_toggle_dark.on_clicked(self.toggle_dark_mode)
        self.btn_clear = Button(plt.axes([left_margin, start_y - 0.46, control_width, control_height]), 'Clear Graph')
        self.btn_clear.on_clicked(self.clear_graph)
        self.layout_radio_ax = plt.axes([left_margin+control_width+0.02, start_y - 0.62, control_width, 0.14])
        self.layout_radio = RadioButtons(self.layout_radio_ax, ('Kamada-Kawaii', 'Circle', 'Spring', 'Shell'), active=0)
        self.btn_arrange = Button(plt.axes([left_margin+control_width+0.02, start_y - 0.68, control_width, control_height]), 'Arrange')
        self.btn_arrange.on_clicked(self.arrange_graph)
        self.btn_print = Button(plt.axes([left_margin, start_y - 0.52, control_width, control_height]), 'Print Graph')
        self.btn_print.on_clicked(self.print_graph)
        self.btn_example = Button(plt.axes([left_margin, start_y - 0.58, control_width, control_height]), 'Load Example')
        self.btn_example.on_clicked(self.load_example)
        self.status_text = self.fig.text((left_margin + control_width/2)+0.5, 0.01, 'Everything OK', fontsize=10, ha='center', va='bottom', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        self.start_text = self.fig.text(left_margin, 0.275, 'Start Node:', fontsize=10, ha='left')
        self.goal_text = self.fig.text(left_margin, 0.225, 'Goal Node:', fontsize=10, ha='left')
        self.start_input = TextBox(plt.axes([left_margin + 0.08, 0.26, control_width - 0.08, control_height]), '', initial=self.start_node if self.start_node else '')
        self.goal_input = TextBox(plt.axes([left_margin + 0.08, 0.21, control_width - 0.08, control_height]), '', initial=self.goal_node if self.goal_node else '')
        self.start_input.on_submit(self.update_start_node)
        self.goal_input.on_submit(self.update_goal_node)
        self.pathfinding_functions = {}
        script_dir = os.path.dirname(os.path.abspath(__file__))
        name_mappings = {
            'aStar': 'A*',
            'dStar': 'D*',
            'bellManFord': 'Bellman-Ford',
            'dijikstra': 'Dijkstra',
            'floydWarshall': 'Floyd-Warshall',
            'bidirectionalSearch': 'Bidirectional Search',
        }
        for filename in os.listdir(script_dir):
            if filename.endswith('.py') and filename != 'editor.py' and not filename.startswith('_'):
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(module_name)
                    display_name = name_mappings.get(module_name, module_name)
                    self.pathfinding_functions[display_name] = module
                except Exception as e:
                    print(f"Failed to import {module_name}: {e}")
        radio_left = left_margin + control_width + 0.02
        self.pathfinding_radio_ax = plt.axes([radio_left, 0.70, control_width, 0.25])
        sorted_algorithms = sorted(self.pathfinding_functions.keys())
        self.pathfinding_radio = RadioButtons(self.pathfinding_radio_ax, tuple(sorted_algorithms), active=0)
        self.btn_run_pathfinding = Button(plt.axes([radio_left, 0.64, control_width, control_height]), 'Run Pathfinding')
        self.btn_run_pathfinding.on_clicked(self.pathfind)
    
    def pathfind(self, event):
        if self.start_node is None or self.goal_node is None:
            self.update_status("Please set both start and goal nodes")
            return
        if self.start_node not in self.graph or self.goal_node not in self.graph:
            self.update_status("Start or goal node not in graph")
            return
        selected_algo = self.pathfinding_radio.value_selected
        algo_function = self.pathfinding_functions[selected_algo]
        try:
            path, distance = algo_function.pathfind(self.graph, self.start_node, self.goal_node, self.pos)
            if path:
                self.current_path = path
                self.update_status(f"{selected_algo}: Path found: {' -> '.join(path)} (Distance: {distance})")
            else:
                self.current_path = None
                self.update_status(f"{selected_algo}: No path found")
            self.draw_graph()
        except Exception as e:
            self.current_path = None
            self.update_status(f"Error during pathfinding: {str(e)}")

    def apply_theme(self):
        if self.dark_mode:
            self.fig.patch.set_facecolor('#121212')
            self.graph_ax.set_facecolor('#1e1e1e')
            for text in self.fig.texts:
                text.set_color('white')
            self.node_name_input.ax.set_facecolor('#2d2d2d')
            self.node_name_input.label.set_color('white')
            self.edge_weight_input.ax.set_facecolor('#2d2d2d')
            self.edge_weight_input.label.set_color('white')
            for btn in [self.btn_add_node, self.btn_add_edge, self.btn_cancel_edge, self.btn_toggle_dark, self.btn_clear, self.btn_arrange, self.btn_print, self.btn_example, self.btn_run_pathfinding]:
                btn.color = '#2d2d2d'
                btn.hovercolor = '#3d3d3d'
                btn.label.set_color('white')
            self.btn_toggle_dark.label.set_text('Light Mode')
            self.pathfinding_radio_ax.set_facecolor('#2d2d2d')
            for label in self.pathfinding_radio.labels:
                label.set_color('white')
            self.layout_radio_ax.set_facecolor('#2d2d2d')
            for label in self.layout_radio.labels:
                label.set_color('white')
            self.cmap = cm.viridis
            self.sm.set_cmap(self.cmap)
        else:
            self.fig.patch.set_facecolor('white')
            self.graph_ax.set_facecolor('#f8f9fa')
            for text in self.fig.texts:
                text.set_color('black')
            self.node_name_input.ax.set_facecolor('white')
            self.node_name_input.label.set_color('black')
            self.edge_weight_input.ax.set_facecolor('white')
            self.edge_weight_input.label.set_color('black')
            for btn in [self.btn_add_node, self.btn_add_edge, self.btn_cancel_edge, self.btn_toggle_dark, self.btn_clear, self.btn_arrange, self.btn_print, self.btn_example, self.btn_run_pathfinding]:
                btn.color = '0.85'
                btn.hovercolor = '0.95'
                btn.label.set_color('black')
            self.btn_toggle_dark.label.set_text('Dark Mode')
            self.pathfinding_radio_ax.set_facecolor('white')
            for label in self.pathfinding_radio.labels:
                label.set_color('black')
            self.layout_radio_ax.set_facecolor('white')
            for label in self.layout_radio.labels:
                label.set_color('black')
            self.cmap = cm.plasma
            self.sm.set_cmap(self.cmap)
        self.fig.canvas.draw_idle()
    
    def toggle_dark_mode(self, event):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.draw_graph()
    
    def arrange_graph(self, event):
        if len(self.graph) < 1:
            self.update_status("Need at least 1 node to arrange")
            return
        G = nx.Graph()
        for node in self.graph:
            G.add_node(node)
        for node, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                if not G.has_edge(node, neighbor):
                    G.add_edge(node, neighbor, weight=weight)

        selected_layout = self.layout_radio.value_selected
        try:
            if selected_layout == 'Kamada-Kawaii':
                pos = nx.kamada_kawai_layout(G)
            elif selected_layout == 'Circle':
                pos = nx.circular_layout(G)
            elif selected_layout == 'Spring':
                pos = nx.spring_layout(G)
            elif selected_layout == 'Shell':
                pos = nx.shell_layout(G)
            else:
                pos = nx.kamada_kawai_layout(G)

            if pos:
                center_x = sum(p[0] for p in pos.values()) / len(pos)
                center_y = sum(p[1] for p in pos.values()) / len(pos)
                for node in pos:
                    x, y = pos[node]
                    pos[node] = (x - center_x, y - center_y)
            self.pos = pos
            self.update_status(f"Graph arranged with {selected_layout} layout")
            self.draw_graph()
        except Exception as e:
            self.update_status(f"Arrangement failed: {str(e)}")
    
    def update_node_name(self, text):
        self.current_node_name = text.strip() or "A"
        self.update_status(f"Node name: {self.current_node_name}")
    
    def update_weight(self, text):
        try:
            self.current_weight = float(text)
            self.update_status(f"Weight set to {self.current_weight}")
        except ValueError:
            self.update_status("Invalid weight. Using 1.0")
            self.current_weight = 1.0
            self.edge_weight_input.set_val("1.0")
        self.draw_graph()
    
    def add_node_click(self, event):
        node_name = self.current_node_name
        if not node_name:
            self.update_status("Please enter a node name")
            return
        self.graph[node_name] = {}
        self.pos[node_name] = (np.random.rand() * 0.2 - 0.1, np.random.rand() * 0.2 - 0.1)
        self.update_status(f"Added node '{node_name}'")
        self.draw_graph()
    
    def start_edge_creation(self, event):
        if len(self.graph) < 2:
            self.update_status("Need at least 2 nodes to create an edge")
            return
        self.creating_edge = True
        if self.dark_mode:
            self.btn_add_edge.color = '#4d4d4d'
            self.btn_add_edge.hovercolor = '#4d4d4d'
        else:
            self.btn_add_edge.color = '0.8'
            self.btn_add_edge.hovercolor = '0.8'
        self.fig.canvas.draw_idle()
        self.update_status("Click first node for edge (ESC to cancel)")
    
    def cancel_edge_creation(self, event):
        self.creating_edge = False
        self.edge_start_node = None
        if self.dark_mode:
            self.btn_add_edge.color = '#2d2d2d'
            self.btn_add_edge.hovercolor = '#3d3d3d'
        else:
            self.btn_add_edge.color = '0.85'
            self.btn_add_edge.hovercolor = '0.95'
        self.fig.canvas.draw_idle()
        self.update_status("Edge creation cancelled")
        self.draw_graph()
    
    def clear_graph(self, event):
        self.graph = {}
        self.pos = {}
        self.creating_edge = False
        self.edge_start_node = None
        if self.dark_mode:
            self.btn_add_edge.color = '#2d2d2d'
            self.btn_add_edge.hovercolor = '#3d3d3d'
        else:
            self.btn_add_edge.color = '0.85'
            self.btn_add_edge.hovercolor = '0.95'
        self.fig.canvas.draw_idle()
        self.update_status("Graph cleared")
        self.draw_graph()
    
    def print_graph(self, event):
        print("\n" + "="*50)
        print("ADJACENCY DICTIONARY:")
        print("="*50)
        if not self.graph:
            print("Empty graph")
        else:
            for node, neighbors in sorted(self.graph.items()):
                if neighbors:
                    neighbor_str = ", ".join([f"{n}: {w:.1f}" for n, w in sorted(neighbors.items())])
                    print(f"{node}: {{{neighbor_str}}}")
                else:
                    print(f"{node}: {{}}")
        print("="*50)
        self.update_status("Graph printed to console")
    
    def load_example(self, event):
        example_graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1, 'E': 3},
            'E': {'D': 3, 'F': 2},
            'F': {'E': 2}
        }
        self.graph = example_graph
        nodes = list(example_graph.keys())
        n = len(nodes)
        radius = 2.0
        for i, node in enumerate(nodes):
            angle = 2 * np.pi * i / n
            self.pos[node] = (radius * np.cos(angle), radius * np.sin(angle))
        self.update_status("Loaded example graph")
        self.draw_graph()
    
    def update_status(self, message):
        self.status_text.set_text(message)
        if self.dark_mode:
            self.status_text.set_bbox(dict(boxstyle='round', facecolor='#2d2d2d', edgecolor='#444', alpha=0.8))
            self.status_text.set_color('white')
        else:
            self.status_text.set_bbox(dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
            self.status_text.set_color('black')
        self.fig.canvas.draw_idle()
    
    def find_node_at_position(self, x, y, threshold=0.1):
        xlim = self.graph_ax.get_xlim()
        ylim = self.graph_ax.get_ylim()
        x_range = xlim[1] - xlim[0]
        threshold_scaled = threshold * x_range / 2.0
        for node, (node_x, node_y) in self.pos.items():
            distance = np.sqrt((node_x - x)**2 + (node_y - y)**2)
            if distance < threshold_scaled:
                return node
        return None
    
    def update_start_node(self, text):
        node = text.strip()
        if node in self.graph:
            self.start_node = node
            self.update_status(f"Start node set to '{node}'")
            self.draw_graph()
        else:
            self.update_status(f"Node '{node}' not in graph")

    def update_goal_node(self, text):
        node = text.strip()
        if node in self.graph:
            self.goal_node = node
            self.update_status(f"Goal node set to '{node}'")
            self.draw_graph()
        else:
            self.update_status(f"Node '{node}' not in graph")

    def on_click(self, event):
        if event.inaxes != self.graph_ax:
            return
        if hasattr(self.fig.canvas, 'toolbar') and self.fig.canvas.toolbar:
            if self.fig.canvas.toolbar.mode != '':
                self.in_navigation_mode = True
                return
        if event.button == 1:
            node = self.find_node_at_position(event.xdata, event.ydata)
            if self.creating_edge:
                if node:
                    if self.edge_start_node is None:
                        self.edge_start_node = node
                        self.update_status(f"First node: {node}. Click second node")
                    else:
                        if node == self.edge_start_node:
                            self.update_status("Cannot create self-loop (click different node)")
                        elif node in self.graph[self.edge_start_node]:
                            self.update_status(f"Edge {self.edge_start_node}-{node} already exists")
                        else:
                            self.graph[self.edge_start_node][node] = self.current_weight
                            self.graph[node][self.edge_start_node] = self.current_weight
                            self.update_status(f"Added edge {self.edge_start_node}-{node} (weight: {self.current_weight})")
                        self.creating_edge = False
                        self.edge_start_node = None
                        if self.dark_mode:
                            self.btn_add_edge.color = '#2d2d2d'
                            self.btn_add_edge.hovercolor = '#3d3d3d'
                        else:
                            self.btn_add_edge.color = '0.85'
                            self.btn_add_edge.hovercolor = '0.95'
                        self.fig.canvas.draw_idle()
                        self.draw_graph()
            else:
                if node:
                    # Start edge creation from this node
                    self.creating_edge = True
                    self.edge_start_node = node
                    if self.dark_mode:
                        self.btn_add_edge.color = '#4d4d4d'
                        self.btn_add_edge.hovercolor = '#4d4d4d'
                    else:
                        self.btn_add_edge.color = '0.8'
                        self.btn_add_edge.hovercolor = '0.8'
                    self.fig.canvas.draw_idle()
                    self.update_status(f"First node: {node}. Click second node (ESC to cancel)")
                else:
                    node_name = self.current_node_name
                    if not node_name:
                        node_name = chr(65 + len(self.graph))
                        self.node_name_input.set_val(node_name)
                        self.current_node_name = node_name
                    actual_node_name = node_name
                    if actual_node_name in self.graph:
                        i = 1
                        base_name = actual_node_name
                        while f"{base_name}{i}" in self.graph:
                            i += 1
                        actual_node_name = f"{base_name}{i}"
                    self.graph[actual_node_name] = {}
                    self.pos[actual_node_name] = (event.xdata, event.ydata)
                    self.update_status(f"Added node '{actual_node_name}' at ({event.xdata:.2f}, {event.ydata:.2f})")
                    self.draw_graph()
        elif event.button == 3:
            node = self.find_node_at_position(event.xdata, event.ydata)
            if node:
                del self.graph[node]
                del self.pos[node]
                for other_node in self.graph:
                    if node in self.graph[other_node]:
                        del self.graph[other_node][node]
                self.update_status(f"Removed node '{node}' and its edges")
                self.draw_graph()
    
    def on_release(self, event):
        self.dragging_node = None
        self.in_navigation_mode = False
    
    def on_motion(self, event):
        if event.inaxes != self.graph_ax:
            return
        if self.in_navigation_mode:
            return
        if self.dragging_node and event.button == 1:
            self.pos[self.dragging_node] = (event.xdata, event.ydata)
            self.draw_graph()
        if self.creating_edge and self.edge_start_node:
            self._last_mouse_pos = (event.xdata, event.ydata)
            self.draw_graph()
    
    def on_key_press(self, event):
        if self.in_navigation_mode:
            return
        if event.key == 'escape':
            if self.creating_edge:
                self.cancel_edge_creation(None)
        elif event.key == 'delete' or event.key == 'backspace':
            if event.inaxes == self.graph_ax:
                node = self.find_node_at_position(event.xdata, event.ydata)
                if node:
                    del self.graph[node]
                    del self.pos[node]
                    for other_node in self.graph:
                        if node in self.graph[other_node]:
                            del self.graph[other_node][node]
                    self.update_status(f"Removed node '{node}' and its edges (DEL)")
                    self.draw_graph()

    def get_graph_bounds(self):
        if not self.pos:
            return (-2, 2, -2, 2)
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        center_x = (min(xs) + max(xs)) / 2
        center_y = (min(ys) + max(ys)) / 2
        max_distance_from_center = 0
        for x, y in zip(xs, ys):
            distance = max(abs(x - center_x), abs(y - center_y))
            if distance > max_distance_from_center:
                max_distance_from_center = distance
        padding = max(max_distance_from_center * 0.2, 0.5)
        size = max(max_distance_from_center * 2 + padding * 2, 3.0)
        x_min = -size / 2
        x_max = size / 2
        y_min = -size / 2
        y_max = size / 2
        return (x_min, x_max, y_min, y_max)
    
    def draw_graph(self):
        self.graph_ax.clear()
        x_min, x_max, y_min, y_max = self.get_graph_bounds()
        self.graph_ax.set_xlim(x_min, x_max)
        self.graph_ax.set_ylim(y_min, y_max)
        self.graph_ax.set_aspect('equal')
        if self.dark_mode:
            self.graph_ax.set_facecolor('#1e1e1e')
            axis_color = '#666'
            grid_color = '#333'
            text_color = 'white'
            node_text_color = 'white'
        else:
            self.graph_ax.set_facecolor('#f8f9fa')
            axis_color = 'gray'
            grid_color = '#ddd'
            text_color = 'black'
            node_text_color = 'black'
        self.graph_ax.axhline(y=0, color=axis_color, linestyle='-', linewidth=0.5, alpha=0.3)
        self.graph_ax.axvline(x=0, color=axis_color, linestyle='-', linewidth=0.5, alpha=0.3)
        if x_max - x_min < 10 and y_max - y_min < 10:
            self.graph_ax.grid(True, which='both', linestyle='--', alpha=0.3, linewidth=0.5, color=grid_color)
        self.graph_ax.set_title('Graph Visualization Area', fontsize=14, pad=20, color=text_color)
        self.graph_ax.tick_params(colors=text_color)
        for spine in self.graph_ax.spines.values():
            spine.set_color(text_color)
        all_weights = []
        for node, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                if node < neighbor:
                    all_weights.append(weight)
        if all_weights:
            min_weight = min(all_weights)
            max_weight = max(all_weights)
            weight_range = max_weight - min_weight if max_weight != min_weight else 1
        else:
            min_weight = 0
            max_weight = 1
            weight_range = 1
        path_edges = set()
        if self.current_path and len(self.current_path) > 1:
            for i in range(len(self.current_path) - 1):
                n1, n2 = self.current_path[i], self.current_path[i + 1]
                path_edges.add((min(n1, n2), max(n1, n2)))
        view_width = x_max - x_min
        for node, neighbors in self.graph.items():
            x1, y1 = self.pos[node]
            for neighbor, weight in neighbors.items():
                if node < neighbor:
                    x2, y2 = self.pos[neighbor]
                    is_path_edge = (min(node, neighbor), max(node, neighbor)) in path_edges
                    if is_path_edge:
                        edge_color = "#ff0000"
                        linewidth = 5.0
                        alpha = 1.0
                        zorder = 2
                    else:
                        if weight_range > 0:
                            normalized_weight = (weight - min_weight) / weight_range
                        else:
                            normalized_weight = 0.5
                        edge_color = self.cmap(normalized_weight)
                        linewidth = 2.5
                        alpha = 0.7
                        zorder = 1
                    self.graph_ax.plot([x1, x2], [y1, y2], color=edge_color, alpha=alpha, linewidth=linewidth, zorder=zorder)
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    fontsize = max(6, min(12, 10 * view_width / 4))
                    bbox_face = 'white' if not self.dark_mode else '#2d2d2d'
                    bbox_edge = edge_color
                    self.graph_ax.text(mid_x, mid_y, f'{weight:.1f}', fontsize=fontsize, ha='center', va='center', bbox=dict(boxstyle='round,pad=0.2', facecolor=bbox_face, edgecolor=bbox_edge, alpha=0.9), zorder=4, color=text_color)
        for node, (x, y) in self.pos.items():
            if node == self.start_node:
                node_color = '#ff0000'
                node_border_width = 3
            elif node == self.goal_node:
                node_color = '#ff0000'
                node_border_width = 3
            elif self.dragging_node == node:
                node_color = '#ffc107'
                node_border_width = 2
            elif self.creating_edge and node == self.edge_start_node:
                node_color = '#17a2b8'
                node_border_width = 2
            else:
                node_color = '#007bff' if not self.dark_mode else '#4dabf7'
                node_border_width = 2
            view_width = x_max - x_min
            node_size = 0.1 * view_width / 4
            edge_color = 'white' if self.dark_mode else 'black'
            circle = plt.Circle((x, y), node_size, color=node_color, ec=edge_color, lw=node_border_width, zorder=3)
            self.graph_ax.add_patch(circle)
            fontsize = 12 * view_width / 4
            self.graph_ax.text(x, y, node, fontsize=fontsize, fontweight='bold', ha='center', va='center', color=node_text_color, zorder=4)
        if self.creating_edge and self.edge_start_node and hasattr(self, '_last_mouse_pos'):
            x, y = self.pos[self.edge_start_node]
            mx, my = self._last_mouse_pos
            self.graph_ax.plot([x, mx], [y, my], 'r--', alpha=0.5, linewidth=1.5, zorder=2)
            view_width = x_max - x_min
            target_size = max(0.008, min(0.02, 0.015 * view_width / 4))
            target_circle = plt.Circle((mx, my), target_size, color='rgba(0,255,0,0.3)', ec='green', lw=1, zorder=2)
            self.graph_ax.add_patch(target_circle)
        self.norm.vmin = min_weight
        self.norm.vmax = max_weight
        self.sm.set_norm(self.norm)
        self.colorbar.update_normal(self.sm)
        if self.dark_mode:
            self.colorbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
            self.colorbar.outline.set_edgecolor('white')
        else:
            self.colorbar.ax.yaxis.set_tick_params(color='black', labelcolor='black')
            self.colorbar.outline.set_edgecolor('black')
        self.fig.canvas.draw_idle()

if __name__ == "__main__":
    editor = InteractiveGraphEditor()