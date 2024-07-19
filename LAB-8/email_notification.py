import tkinter as tk
from math import pi, cos, sin
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class TemperatureGauge(tk.Canvas):
    def __init__(self, parent, width=300, height=300, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.radius = min(width, height) // 2 - 20
        self.gauge_radius = int(self.radius * 1)

        self.create_gauge()
        self.create_needle()
        self.set_temperature(0)

    def create_gauge(self):
        self.create_oval(10, 10, self.width-10, self.height-10, fill='#f0f0f0', outline='black', width=2)
        for i in range(-100, 101, 10):
            angle = 70 - i
            x_outer = self.center_x + self.gauge_radius * cos(angle * pi / 140)
            y_outer = self.center_y - self.gauge_radius * sin(angle * pi / 140)
            x_inner = self.center_x + (self.gauge_radius - 15) * cos(angle * pi / 140)
            y_inner = self.center_y - (self.gauge_radius - 15) * sin(angle * pi / 140)
            self.create_line(x_inner, y_inner, x_outer, y_outer, fill='black', width=2)
            if i % 20 == 0:
                x_text = self.center_x + (self.gauge_radius - 30) * cos(angle * pi / 140)
                y_text = self.center_y - (self.gauge_radius - 30) * sin(angle * pi / 140)
                self.create_text(x_text, y_text, text=str(i), fill='black')

    def create_needle(self):
        self.needle = self.create_line(self.center_x, self.center_y, self.center_x, self.center_y - self.gauge_radius, width=3, fill='red')
        self.needle_hub = self.create_oval(self.center_x-5, self.center_y-5, self.center_x+5, self.center_y+5, fill='red')

    def set_temperature(self, temperature):
        angle = 70 - temperature
        x = self.center_x + self.gauge_radius * cos(angle * pi / 140)
        y = self.center_y - self.gauge_radius * sin(angle * pi / 140)
        self.coords(self.needle, self.center_x, self.center_y, x, y)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Temperature Gauge')
        self.geometry('350x400')
        self.gauge = TemperatureGauge(self)
        self.gauge.pack(pady=20)

        self.temp_entry = tk.Entry(self)
        self.temp_entry.pack(pady=10)
        self.set_temp_button = tk.Button(self, text='Set Temperature', command=self.update_temperature)
        self.set_temp_button.pack()

    def update_temperature(self):
        try:
            temperature = int(self.temp_entry.get())
            if -100 <= temperature <= 100:
                self.gauge.set_temperature(temperature)
            else:
                
                # Send email notification
                self.send_email_notification(temperature)
        except ValueError:
            print("Invalid input. Please enter a numerical value.")


    def send_email_notification(self, temperature):
        """
        Send an email notification when the temperature entered is out of range.

        This function creates an email message with the temperature value that is outside
        the normal range and sends it using the SMTP protocol through a Gmail account.

        Args:
            temperature (int): The temperature value that is out of the normal range.
        """

        sender_email = "temporary@gmail.com"
        sender_password = "password"

        receiver_email = "receiver_email@gmail.com"
        
        subject = "Temperature Alert"
        body = f"The temperature entered is out of range: {temperature}°"

        # Creating email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attaching the body
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print("Email sent successfully")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    app = App()
    app.mainloop()
