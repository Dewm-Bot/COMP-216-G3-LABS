# Mohammed Aadil
# COMP 216
# LAB 7 & 8

from tkinter import Tk, Canvas, Frame, Entry, Button, Label, IntVar

class TemperatureDisplay(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title('Temperature Display')
        self.pack(fill = 'both', expand = True)

        # Main canvas for the thermometer display
        self.canvas = Canvas(self, height = 200, width = 50, bg = 'white')
        self.temperature_var = IntVar(value = 20)  # Default temperature
        self.temp_bar = self.canvas.create_rectangle(10, 180, 40, 180 - self.temperature_var.get() * 3, fill = 'blue', outline = 'blue')
        self.canvas.create_text(25, 10, text = f"{self.temperature_var.get()}°C", font = ('Arial', 10, 'bold'))
        self.canvas.pack(pady = 20)

        # Label for unit and range information
        self.info_label = Label(self, text = 'Unit: °C, Range: 18-21°C', font = ('Arial', 10))
        self.info_label.pack()

        # Entry for new temperature input
        self.entry = Entry(self, textvariable = self.temperature_var, font = ('Arial', 12), width = 7)
        self.entry.pack(pady = 10)
        self.entry.bind('<Return>', lambda event: self.update_temperature())  # Enter key will trigger UPDATE

        # Update button
        self.update_button = Button(self, text = 'UPDATE', command = self.update_temperature)
        self.update_button.pack(side = 'right', padx = 10, pady = 10)

    def update_temperature(self):
        # Read the current temperature value
        temp = self.temperature_var.get()
        
        # Update the height of the temperature bar
        new_height = 180 - temp * 3
        
        self.canvas.coords(self.temp_bar, 10, 180, 40, new_height)
        self.canvas.itemconfig(self.temp_bar, fill = 'blue' if 18 <= temp <= 21 else 'red')
        
        # Update the temperature display text
        self.canvas.itemconfig(2, text = f"{temp}°C")

root = Tk()
root.geometry('350x350')
app = TemperatureDisplay()
root.mainloop()
