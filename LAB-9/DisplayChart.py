import tkinter as tk
from tkinter import messagebox

class DisplayChart:
    def __init__(self, root,num_bars,bar_color,title,values):
        self.root = root
        #App Title
        self.root.title(title)
        #Values set via list
        self.values = values
        self.canvas_width = 500
        self.canvas_height = 400
        #Number of bars to display
        self.num_bars = num_bars
        self.padding = 20
        #Base color for bars
        self.bar_color = bar_color
        #Border color for bars
        self.border_color = "black"
        
        self.ui_gen()

    def ui_gen(self):
        #Generate the UI
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)
        #Entry for user to input start index
        self.entry = tk.Entry(top_frame)
        self.entry.pack(side=tk.LEFT)
        #Go button to update graph
        self.go_button = tk.Button(top_frame, text="Go", command=self.graph_update)
        self.go_button.pack(side=tk.LEFT, padx=5)
        #Label to display range of values
        self.range_label = tk.Label(self.root, text="")
        self.range_label.pack(pady=5)
        #Canvas to display the graph
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white", bd=2, relief="sunken")
        self.canvas.pack(padx=self.padding, pady=self.padding)
        
        self.graph_gen(0)

    def graph_gen(self, start_index):
        self.canvas.delete("all")
        #Check if start index is valid, if not set to the max possible value
        if start_index < 0 or start_index + self.num_bars > len(self.values):
            start_index = len(self.values) - self.num_bars

        #Update the range label
        self.range_label.config(text=f"Displaying values {start_index} to {start_index + self.num_bars -1}")
        
        max_value = max(self.values)
        bar_width = (self.canvas_width - 2 * self.padding) / self.num_bars
        
        for i in range(self.num_bars): #Draw bars
            value = self.values[start_index + i]
            bar_height = (value / max_value) * (self.canvas_height - 2 * self.padding)
            x0 = self.padding + i * bar_width
            y0 = self.canvas_height - self.padding - bar_height
            x1 = self.padding + (i + 1) * bar_width - self.padding / 2
            y1 = self.canvas_height - self.padding
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.bar_color, outline=self.border_color)
            #Likely need to add the code to draw the lines here

    def graph_update(self):
        try: #Update the graph with the new start index
            start_index = int(self.entry.get())
        except ValueError: #Set start index to 0 if invalid
            start_index = 0
        self.graph_gen(start_index)

if __name__ == "__main__":
    #TEMP VALUES, PLEASE CHANGE TO DATA GEN VALUES
    values = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    #Change name maybe
    title = "Display Chart"
    bar_color = "lightblue"
    num_bars = 6
    root = tk.Tk()
    app = DisplayChart(root,num_bars,bar_color,title,values)
    root.mainloop()
