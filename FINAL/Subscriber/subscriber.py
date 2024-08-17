import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import json
import threading
import sys

class Subscriber:
    def __init__(self, root, min_value=18, max_value=21, app_title="Temperature Analytics: 1"):
        self.root = root
        self.root.title(app_title)

        self.MIN_VALUE = min_value
        self.MAX_VALUE = max_value

        self.chart_data = []
        self.is_paused = False
        self.running = True

        self.setup_ui()
        self.setup_mqtt()

        #if the window is closed, run closing routine
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):

        chart_frame = ttk.Frame(self.root)
        chart_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Temperature (Cº)")
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        log_frame = ttk.Frame(self.root)
        log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=10)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        #Creates a scrollbar for the logger
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text['yscrollcommand'] = scrollbar.set

        #Sets Colors for different log types
        self.log_text.tag_config("error", foreground="red")

        #Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
       
        self.stop_resume_button = ttk.Button(button_frame, text="Stop", command=self.toggle_pause)
        self.stop_resume_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_chart)
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=5)

        

    def setup_mqtt(self):
        #Initalize MQTT CLient
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        #Connect to localhost
        try:
            self.client.connect("localhost", 1883, 60)
        except Exception as e:
            self.log_error(f"Failed to connect to MQTT broker - {e}")
            self.root.quit()
            return

        try:
            self.mqtt_thread = threading.Thread(target=self.mqtt_loop)
            self.mqtt_thread.daemon = True  # Make the thread daemon, so it exits when the main program exits
            self.mqtt_thread.start()
        except Exception as e:
            self.log_error(f"Failed to start MQTT thread - {e}")

    #Client Loop
    def mqtt_loop(self):
        while self.running:
            try:
                self.client.loop(timeout=0.1)
            except Exception as e:
                self.log_error(f"MQTT loop error - {e}")
                self.running = False
        self.client.disconnect()

    #Message Handler
    def on_message(self, client, userdata, msg):
        if not self.is_paused:
            try:
                #Recieve Message
                data = json.loads(msg.payload)
                sensor_value = data['sensor_value']
                timestamp = data['timestamp']

                #Check if Message is in range
                if sensor_value < self.MIN_VALUE or sensor_value > self.MAX_VALUE:
                    self.log_error(f"{timestamp} - Value: {sensor_value} out of range!") 
                else:
                    #Log
                    self.log_data(sensor_value, timestamp)
                    #Update Chart
                    self.update_chart(sensor_value)
                #Error Handling
            except json.JSONDecodeError as e:
                self.log_error(f"Failed to decode JSON - {e}")
            except KeyError as e:
                self.log_error(f"Missing key in JSON - {e}")
            except Exception as e:
                self.log_error(f"Unexpected error - {e}")

    def update_chart(self, value):
        self.chart_data.append(value)
        self.ax.clear()
        self.ax.set_title("Temperature (Cº)")
        self.ax.plot(self.chart_data, marker='o')
        self.canvas.draw()

    def log_data(self, value, timestamp): #Data Log handler
        self.log_text.insert(tk.END, f"{timestamp} - RECIEVED Value: {value}\n")
        self.log_text.yview(tk.END)

    def log_error(self, message): #Error message handler (Log)
        self.log_text.insert(tk.END, f"[ERROR] {message}\n", "error")
        self.log_text.yview(tk.END)

    def on_connect(self, client, userdata, flags, rc):
        #Topic to subscribe to
        client.subscribe("test/topic")

    def toggle_pause(self):
        self.is_paused = not self.is_paused #Toggle pause
        self.stop_resume_button.config(text="Resume" if self.is_paused else "Stop") #Toggle Pause Text

    def reset_chart(self):
        self.chart_data = []
        self.ax.clear()
        self.ax.set_title("Temperature (Cº)")
        self.canvas.draw()

    def on_closing(self): 
        #Exit Routine
        self.running = False
        if self.mqtt_thread.is_alive():
            self.mqtt_thread.join()
        self.root.quit()

    def start(self): #Safer script handling
        try:
            self.root.mainloop()
        except KeyboardInterrupt: #Properly handle keyboard interupt
            self.on_closing()
            print(f"Keyboard Interupt Recieved! Closing!")
            sys.exit(0)
        except Exception as e: #Handle fatal errors
            print(f"ERROR: {e} Force Closing")
            self.on_closing()

if __name__ == "__main__":
    root = tk.Tk()
    app = Subscriber(root, min_value=15, max_value=25)
    app.start()
