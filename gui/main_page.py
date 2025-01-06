import tkinter as tk
from tkinter import ttk
from datetime import datetime
from .base_frame import BaseFrame

class MainPage(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._init_ui()

    def _init_ui(self):
        self._create_status_frame()
        self._create_subscribe_frame()
        self._create_topics_frame()
        self._create_messages_frame()
        self._create_publish_frame()

    def _create_status_frame(self):
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.status_label = tk.Label(
            frame, 
            text="● Connected", 
            fg="green",
            font=("Helvetica", 10, "bold")
        )
        self.status_label.pack(side=tk.LEFT)

    def _create_subscribe_frame(self):
        frame = tk.LabelFrame(self, text="Subscribe to Topic", )
        frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.add_topic_entry = tk.Entry(frame, width=30)
        self.add_topic_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            frame, 
            text="Subscribe",
            command=self._add_subscription
        ).grid(row=0, column=2, padx=5, pady=5)

    def _create_topics_frame(self):
        frame = tk.LabelFrame(self, text="Subscribed Topics")
        frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.topics_listbox = tk.Listbox(
            frame, 
            height=4,
            selectmode=tk.SINGLE
        )
        self.topics_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.topics_listbox.bind('<Double-Button-1>', self._on_topic_double_click)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.topics_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.topics_listbox.yview)

        tk.Button(
            frame,
            text="Unsubscribe",
            command=self._unsubscribe_selected
        ).pack(side=tk.BOTTOM, pady=5)

    def _create_messages_frame(self):
        frame = tk.LabelFrame(self, text="Received Messages")
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.received_text = tk.Text(
            frame, 
            height=10,
            width=50,
            wrap=tk.WORD,
            state='disabled'  # Make text widget read-only
        )
        self.received_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.received_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.received_text.yview)

        tk.Button(
            frame,
            text="Clear Messages",
            command=self._clear_messages
        ).pack(side=tk.BOTTOM, pady=5)

    def _create_publish_frame(self):
        frame = tk.LabelFrame(self, text="Publish Message")
        frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        tk.Label(frame, text="Topic:").grid(row=0, column=0, padx=5, pady=5)
        self.publish_topic_entry = tk.Entry(frame, width=33)
        self.publish_topic_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Message:").grid(row=1, column=0, padx=5, pady=5)
        self.publish_message_entry = tk.Entry(frame, width=33)
        self.publish_message_entry.grid(row=1, column=1, padx=5, pady=5)

        button_frame = tk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        button_frame.grid_columnconfigure(1, weight=1)

        tk.Button(
            button_frame,
            text="Publish",
            command=self._publish_message
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Disconnect",
            fg="red",
            command=self._disconnect
        ).grid(row=0, column=2, padx=5)

    def _add_subscription(self):
        topic = self.add_topic_entry.get()
        if topic and self.controller.mqtt_client:
            if self.controller.mqtt_client.subscribe(topic):
                self._update_topics_list()
                self._update_received_messages("System", f"Subscribed to: {topic}")
                self.add_topic_entry.delete(0, tk.END)
                self._update_publish_topics_dropdown()

    def _unsubscribe_selected(self):
        selection = self.topics_listbox.curselection()
        if selection:
            topic = self.topics_listbox.get(selection[0])
            self.controller.mqtt_client.unsubscribe(topic)
            self._update_topics_list()
            self._update_received_messages("System", f"Unsubscribed from: {topic}")
            self._update_publish_topics_dropdown()

    def _update_topics_list(self):
        self.topics_listbox.delete(0, tk.END)
        topics = sorted(self.controller.mqtt_client.get_subscribed_topics())
        for topic in topics:
            self.topics_listbox.insert(tk.END, topic)

    def _update_publish_topics_dropdown(self):
        topics = sorted(self.controller.mqtt_client.get_subscribed_topics())
        self.publish_topic_entry['values'] = topics

    def _on_topic_double_click(self, event):
        selection = self.topics_listbox.curselection()
        if selection:
            topic = self.topics_listbox.get(selection[0])
            self.publish_topic_entry.delete(0, tk.END)
            self.publish_topic_entry.insert(0, topic)

    def _disconnect(self):
        self.status_label.config(text="● Disconnected", fg="red")
        # Clear topics
        self.topics_listbox.delete(0, tk.END)
        # Clear messages
        self.received_text.delete(1.0, tk.END)
        # Clear publish entries
        self.publish_topic_entry.delete(0, tk.END)
        self.publish_message_entry.delete(0, tk.END)
        # Clear subscribe entry
        self.add_topic_entry.delete(0, tk.END)
        # Disconnect MQTT
        self.controller.disconnect_broker()

    def _publish_message(self):
        topic = self.publish_topic_entry.get()
        message = self.publish_message_entry.get()
        if self.controller.mqtt_client:
            self.controller.mqtt_client.publish(topic, message)
            self.publish_message_entry.delete(0, tk.END)

    def update_connection_status(self, is_connected: bool):
        if is_connected:
            self.status_label.config(text="● Connected", fg="green")
        else:
            self.status_label.config(text="● Disconnected", fg="red")

    def _clear_messages(self):
        self.received_text.config(state='normal')
        self.received_text.delete(1.0, tk.END)
        self.received_text.config(state='disabled')

    def update_received_messages(self, topic: str, message: str):
        self.received_text.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.received_text.insert(tk.END, f"[{timestamp}] Topic: {topic}\nMessage: {message}\n\n")
        self.received_text.see(tk.END)
        self.received_text.config(state='disabled')