import tkinter as tk
from tkinter import ttk
import threading
from publisher import Publisher

class PublisherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Publisher")

        self.publisher = Publisher()

        self.setup_ui()
        self.is_publishing = False
        self.publish_thread = None

    def setup_ui(self):
        # Frame for controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.BOTH, expand=True)

        # Topic Label and Entry
        ttk.Label(control_frame, text="Topic:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.topic_entry = ttk.Entry(control_frame)
        self.topic_entry.grid(row=0, column=1, padx=5)
        self.topic_entry.insert(0, self.publisher.topic)

        # Min Value Label and Entry
        ttk.Label(control_frame, text="Min Value:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.min_value_entry = ttk.Entry(control_frame)
        self.min_value_entry.grid(row=1, column=1, padx=5)
        self.min_value_entry.insert(0, self.publisher.sensor.min_value)

        # Max Value Label and Entry
        ttk.Label(control_frame, text="Max Value:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.max_value_entry = ttk.Entry(control_frame)
        self.max_value_entry.grid(row=2, column=1, padx=5)
        self.max_value_entry.insert(0, self.publisher.sensor.max_value)

        # Repeat Label and Entry
        ttk.Label(control_frame, text="Repeat:").grid(row=3, column=0, sticky=tk.W, padx=5)
        self.repeat_entry = ttk.Entry(control_frame)
        self.repeat_entry.grid(row=3, column=1, padx=5)
        self.repeat_entry.insert(0, "10")

        # Interval Label and Entry
        ttk.Label(control_frame, text="Interval (s):").grid(row=4, column=0, sticky=tk.W, padx=5)
        self.interval_entry = ttk.Entry(control_frame)
        self.interval_entry.grid(row=4, column=1, padx=5)
        self.interval_entry.insert(0, "2")

        # Start Button
        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_publishing)
        self.start_button.grid(row=5, column=0, pady=10)

        # Stop Button
        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_publishing)
        self.stop_button.grid(row=5, column=1, pady=10)

    def start_publishing(self):
        if not self.is_publishing:
            # Update publisher settings
            self.publisher.topic = self.topic_entry.get()
            self.publisher.sensor.min_value = float(self.min_value_entry.get())
            self.publisher.sensor.max_value = float(self.max_value_entry.get())
            repeat = int(self.repeat_entry.get())
            interval = float(self.interval_entry.get())

            # Start publishing in a separate thread
            self.is_publishing = True
            self.publish_thread = threading.Thread(target=self.publisher.start, args=(repeat, interval))
            self.publish_thread.start()

    def stop_publishing(self):
        if self.is_publishing:
            self.publisher.stop()
            if self.publish_thread is not None:
                self.publish_thread.join()
            self.is_publishing = False

if __name__ == "__main__":
    root = tk.Tk()
    app = PublisherApp(root)
    root.mainloop()
