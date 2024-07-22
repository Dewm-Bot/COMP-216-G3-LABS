# Group6 
# Alex Rahemat
# Sua Cha
# Mohammed Aadil
# Ujjwal Poudel

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
import tkinter as tk
from math import pi, cos, sin

class TemperatureGauge(tk.Canvas):
    def __init__(self, parent, width=280, height=280, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.radius = min(width, height) // 2 - 20
        self.gauge_radius = self.radius

        self.create_gauge()
        self.create_needle()
        self.set_temperature(0)

    def create_gauge(self):
        # Draw the gauge background
        self.create_oval(10, 10, self.width-10, self.height-10, fill='#f0f0f0', outline='black', width=2)

        # Draw the gauge ticks
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
        # Draw the needle
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
        self.gauge.pack(pady=5)

        self.temp_entry = tk.Entry(self)
        self.temp_entry.pack(pady=5)
        self.set_temp_button = tk.Button(self, text='Set Temperature', command=self.update_temperature)
        self.set_temp_button.pack()

        self.check_email_button = tk.Button(self, text='Check Sent Emails', command=self.check_sent_emails)
        self.check_email_button.pack()

    def update_temperature(self):
        try:
            temperature = int(self.temp_entry.get())
            if -100 <= temperature <= 100:
                self.gauge.set_temperature(temperature)
            else:
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

        sender_email = "sua.tdot.dev@gmail.com"
        sender_password = "alwl jslv jxzl guxn"  # Directly use the email password
        receiver_email = "sua.tdot.dev@gmail.com"

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

    def check_sent_emails(self):
        """
        Check the latest sent email from the Gmail account.

        This function logs into the Gmail account, accesses the "Sent Mail" folder,
        and prints the details of the latest sent email.

        Args:
            None
        """

        email_user = "sua.tdot.dev@gmail.com"
        email_pass = "alwl jslv jxzl guxn"  # Directly use the email password

        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(email_user, email_pass)
            mail.select('"[Gmail]/Sent Mail"')

            result, data = mail.search(None, "ALL")
            email_ids = data[0].split()
            latest_email_id = email_ids[-1]

            result, data = mail.fetch(latest_email_id, "(RFC822)")
            raw_email = data[0][1]

            msg = email.message_from_bytes(raw_email)
            print("Subject:", msg["subject"])
            print("From:", msg["from"])
            print("To:", msg["to"])

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        print("Body:", part.get_payload(decode=True).decode())
            else:
                print("Body:", msg.get_payload(decode=True).decode())

            mail.logout()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    app = App()
    app.mainloop()
