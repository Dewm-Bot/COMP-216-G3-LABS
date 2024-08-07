import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import random
import time

class DynamicChartApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dynamic Data Display")
        self.geometry("800x600")
        
        # Styling the main window
        self.configure(background='#FC6C85')
        
        # Data for plotting
        self.initial_data = [random.randint(0, 100) for _ in range(10)]
        self.data = self.initial_data[:]
        self.running = False  # Control flag for the thread
        
        # Initialize UI
        self.initUI()
    
    def initUI(self):
        # Creating a figure and setting its properties
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor('#FFC1CC')  # Set the background color for the plot area
        
        # Embedding the plot in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # 'Go' button to start the dynamic update
        self.go_button = ttk.Button(self, text="Go", command=self.start_thread)
        self.go_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # 'Stop' button to halt the dynamic update
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_thread)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # 'Reset' button to reset the data to initial state
        self.reset_button = ttk.Button(self, text="Reset", command=self.reset_data)
        self.reset_button.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def start_thread(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.update_plot)
            self.thread.daemon = True
            self.thread.start()

    def stop_thread(self):
        if self.running:
            self.running = False
            self.thread.join()  # Ensure thread stops cleanly

    def reset_data(self):
        if not self.running:  # Prevent reset while updating
            self.data = self.initial_data[:]
            self.update_plot_once()  # Update plot immediately after reset
    
    def update_plot(self):
        while self.running:
            # Simulate dynamic data changes
            self.data.pop(0)  # Remove the first item
            self.data.append(random.randint(0, 100))  # Add a new random value
            self.update_plot_once()
            time.sleep(0.5)  # Sleep for 0.5 seconds

    def update_plot_once(self):
        # Update line chart
        self.ax1.clear()
        self.ax1.plot(self.data, label='Data', color='blue')
        self.ax1.set_facecolor('#FFD1DC')  # Light background color for the chart area
        self.ax1.set_title("Dynamic Line Chart")
        self.ax1.set_xlabel("Index")
        self.ax1.set_ylabel("Value")
        self.ax1.legend()
        
        # Redraw the canvas
        self.canvas.draw()

if __name__ == "__main__":
    app = DynamicChartApp()
    app.mainloop()
