import tkinter as tk
from .base_frame import BaseFrame

class ConnectPage(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._init_ui()

    def _init_ui(self):
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.status_label = tk.Label(
            frame,
            text="● Disconnected",
            fg="red",
            font=("Helvetica", 10, "bold")
        )
        self.status_label.pack(side=tk.LEFT)

        tk.Label(self, text="MQTT Broker Connection", 
                font=("Helvetica", 16)).pack(pady=20)
        
        

        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        fields = [
            ("Broker Address:", "broker.hivemq.com"),
            ("Port:", "1883"),
            ("Client ID:", "app001")
        ]
        
        self.entries = {}
        for i, (label, default) in enumerate(fields):
            tk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(input_frame, width=30)
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        tk.Button(self, text="Connect Broker", 
                 command=self._connect_broker).pack(pady=20)

    def _connect_broker(self):
        broker = self.entries["Broker Address:"].get()
        port = int(self.entries["Port:"].get())
        client_id = self.entries["Client ID:"].get()
        self.controller.connect_broker(broker, port, client_id)