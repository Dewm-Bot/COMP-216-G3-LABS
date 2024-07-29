import tkinter as tk
from tkinter import ttk
import random  # Import random for generating values

# SensorSimulator class from LAB6 copied here
class SensorSimulator:
    def __init__(self, min_value=18, max_value=21, seed=None):
        self.min_value = min_value
        self.max_value = max_value
        if seed is not None:
            random.seed(seed)
    
    def _generate_normalized_value(self):
        return random.random()
    
    @property
    def value(self):
        normalized_value = self._generate_normalized_value()
        return self.min_value + (self.max_value - self.min_value) * normalized_value
    
    def generate_values(self, num_values=20):
        return [self.value for _ in range(num_values)]

class DisplayChart:
    def __init__(self, root, num_bars, bar_color, title, values):
        self.root = root
        # App Title
        self.root.title(title)
        # Values set via list
        self.values = values
        self.canvas_width = 500
        self.canvas_height = 400
        # Number of bars to display
        self.num_bars = num_bars
        self.padding = 20
        # Base color for bars
        self.bar_color = bar_color
        
        self.ui_gen()

    def ui_gen(self):
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.configure("TEntry", font=("Helvetica", 12), padding=6)
        style.configure("TLabel", font=("Helvetica", 12))

        # Generate the UI
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10)

        # Entry for user to input start index
        self.entry = ttk.Entry(top_frame, style="TEntry")
        self.entry.pack(side=tk.LEFT, padx=5)

        # Go button to update graph
        self.go_button = ttk.Button(top_frame, text="Go", command=self.graph_update, style="TButton")
        self.go_button.pack(side=tk.LEFT, padx=5)
        
        # Label to display range of values
        self.range_label = ttk.Label(self.root, text="", style="TLabel")
        self.range_label.pack(pady=5)

        # Canvas to display the graph
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white", bd=0, highlightthickness=0)
        self.canvas.pack(padx=self.padding, pady=self.padding)
        
        self.graph_gen(0)

    def graph_gen(self, start_index):
        self.canvas.delete("all")

        # Check if start index is valid, if not set to the max possible value
        if start_index < 0 or start_index + self.num_bars > len(self.values):
            start_index = len(self.values) - self.num_bars

        # Update the range label
        self.range_label.config(text=f"Displaying values {start_index} to {start_index + self.num_bars - 1}")
        
        max_value = max(self.values)
        bar_width = (self.canvas_width - 2 * self.padding) / self.num_bars

        previous_x, previous_y = None, None # Initialize previous_x and previous_y to store the previous bar's center coordinates
        
        for i in range(self.num_bars): # Draw bars
            value = self.values[start_index + i]
            bar_height = (value / max_value) * (self.canvas_height - 2 * self.padding)
            x0 = self.padding + i * bar_width
            y0 = self.canvas_height - self.padding - bar_height
            x1 = self.padding + (i + 1) * bar_width - self.padding / 2
            y1 = self.canvas_height - self.padding
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#007aff", outline="")
            # Likely need to add the code to draw the lines here

            # Add a line connecting the centers of adjacent bars
            if previous_x is not None and previous_y is not None:
                self.canvas.create_line(previous_x, previous_y, (x0 + x1) / 2, y0, fill="Red", width=2)
            
            # Draw a dot at the connection point
            dot_x = (x0 + x1) / 2
            dot_y = y0
            self.canvas.create_oval(dot_x - 2, dot_y - 2, dot_x + 2, dot_y + 2, fill="Red", outline="Red")
        
            # Update the previous_x and previous_y to the current bar's center coordinates
            previous_x = (x0 + x1) / 2
            previous_y = y0

    def graph_update(self):
        try: # Update the graph with the new start index
            start_index = int(self.entry.get())
        except ValueError: # Set start index to 0 if invalid
            start_index = 0
        self.graph_gen(start_index)

if __name__ == "__main__":
    sensor = SensorSimulator(min_value=18, max_value=21)  # Create a sensor simulator instance
    values = sensor.generate_values(20)  # Generate 20 values using the sensor simulator
    title = "Display Chart"
    bar_color = "lightblue"
    num_bars = 6
    root = tk.Tk()
    app = DisplayChart(root, num_bars, bar_color, title, values)
    root.mainloop()
