import tkinter as tk
from math import pi, cos, sin

class TemperatureGauge(tk.Canvas):
    def __init__(self, parent, width=300, height=300, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.center_x = width // 2 #// takes out the decimal. This is as close as we can get to the center
        self.center_y = height // 2
        self.radius = min(width, height) // 2 - 20
        self.gauge_radius = int(self.radius * 1)  #Adjusts positioning of the interior of the gauge. Not very important, but if needed.

        self.create_gauge()
        self.create_needle()
        self.set_temperature(0)

    def create_gauge(self):
        # Draw background
        self.create_oval(10, 10, self.width-10, self.height-10, fill='#f0f0f0', outline='black', width=2)

        # Draw major ticks for positive and negative values
        for i in range(-100, 101, 10):
            angle = 70 - i  #If you edit the below values (pi / *) edit this until 0 is at the top
            x_outer = self.center_x + self.gauge_radius * cos(angle * pi / 140) #The inverse of 140 degrees is the range of the gauge
            y_outer = self.center_y - self.gauge_radius * sin(angle * pi / 140)
            x_inner = self.center_x + (self.gauge_radius - 15) * cos(angle * pi / 140)
            y_inner = self.center_y - (self.gauge_radius - 15) * sin(angle * pi / 140)
            #Create lines for the ticks
            self.create_line(x_inner, y_inner, x_outer, y_outer, fill='black', width=2)
            if i % 20 == 0:
                x_text = self.center_x + (self.gauge_radius - 30) * cos(angle * pi / 140)
                y_text = self.center_y - (self.gauge_radius - 30) * sin(angle * pi / 140)
                #Create temperature text
                self.create_text(x_text, y_text, text=str(i), fill='black')

    def create_needle(self):
        # Initialize the needle to point upwards
        self.needle = self.create_line(self.center_x, self.center_y, self.center_x, self.center_y - self.gauge_radius, width=3, fill='red')
        self.needle_hub = self.create_oval(self.center_x-5, self.center_y-5, self.center_x+5, self.center_y+5, fill='red')

    def set_temperature(self, temperature):
        #Angle should match the angle above in create_gauge
        angle = 70 - temperature
        x = self.center_x + self.gauge_radius * cos(angle * pi / 140) #140 degrees should also match with the above
        y = self.center_y - self.gauge_radius * sin(angle * pi / 140)
        self.coords(self.needle, self.center_x, self.center_y, x, y)

class App(tk.Tk): #Generate app window
    def __init__(self):
        super().__init__()
        self.title('Temperature Gauge')
        self.geometry('350x350')
        self.gauge = TemperatureGauge(self)
        self.gauge.pack(pady=20)

        #Set Temperature with this
        self.gauge.set_temperature(-60)

if __name__ == '__main__':
    app = App()
    app.mainloop()
