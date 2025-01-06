# MQTT Application

A desktop application for MQTT protocol communication built with Python and Tkinter.

## Features

- Connect to MQTT brokers
- Subscribe to multiple topics
- Publish messages to topics
- Real-time message monitoring
- Topic management
- Connection status monitoring

## Requirements

- Python 3.6+
- paho-mqtt
- tkinter (usually comes with Python)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install paho-mqtt
```

## Usage

1. Start the application:
```bash
python mqtt_app/main.py
```

2. Connect to broker:
   - Enter broker address (default: broker.hivemq.com)
   - Enter port (default: 1883)
   - Enter client ID
   - Click "Connect Broker"

3. Subscribe to topics:
   - Enter topic in subscribe field
   - Click "Subscribe"
   - View subscribed topics in list
   - Double-click topic to copy to publish field

4. Publish messages:
   - Enter topic
   - Enter message
   - Click "Publish"

## Project Structure

```
mqtt_app/
├── __init__.py
├── main.py
├── mqtt_client.py
└── gui/
    ├── __init__.py
    ├── base_frame.py
    ├── connect_page.py
    └── main_page.py
```

## License

MIT License
