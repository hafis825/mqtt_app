import tkinter as tk
from tkinter import messagebox
from mqtt_client import MQTTClient
from gui.connect_page import ConnectPage
from gui.main_page import MainPage

class MQTTApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MQTT ยู้ฮู......")
        self.root.geometry("600x700")

        self._init_container()
        self._init_frames()
        
        self.mqtt_client = MQTTClient(self._handle_message)
        self.show_frame(ConnectPage)

    def _init_container(self):
        self.container = tk.Frame(self.root)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def _init_frames(self):
        self.frames = {}
        for Frame in (ConnectPage, MainPage):
            frame = Frame(self.container, self)
            self.frames[Frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def connect_broker(self, broker: str, port: int, client_id: str):
        try:
            self.mqtt_client.connect(broker, port, client_id)
            self.frames[MainPage].update_connection_status(True)
            self.show_frame(MainPage)
        except ConnectionError as e:
            messagebox.showerror("Connection Error", str(e))

    def disconnect_broker(self):
        if self.mqtt_client:
            self.mqtt_client.disconnect()
            self.frames[MainPage].update_connection_status(False)
        self.show_frame(ConnectPage)

    def _handle_message(self, topic: str, message: str):
        if topic == "iotapp/status" and message == "Application Connect Success":
            self.root.after(0, lambda: self.show_frame(MainPage))
        
        main_page = self.frames[MainPage]
        main_page.update_received_messages(topic, message)

def main():
    app = MQTTApplication()
    app.root.mainloop()

if __name__ == "__main__":
    main()