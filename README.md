# แอพพลิเคชัน MQTT

โปรแกรมสำหรับการสื่อสารผ่านโปรโตคอล MQTT พัฒนาด้วย Python และ Tkinter

## คุณสมบัติ

- เชื่อมต่อกับ MQTT Broker
- สมัครสมาชิก (Subscribe) หลายหัวข้อ
- ส่งข้อความ (Publish) ไปยังหัวข้อต่างๆ
- ติดตามข้อความแบบเรียลไทม์
- จัดการหัวข้อ
- แสดงสถานะการเชื่อมต่อ

## ความต้องการของระบบ

- Python 3.6 ขึ้นไป
- paho-mqtt
- tkinter (มักติดตั้งมาพร้อมกับ Python)

## การติดตั้ง

1. ติดตั้ง dependencies:
```bash
pip install paho-mqtt
```

## วิธีการใช้งาน

1. เริ่มต้นโปรแกรม:
```bash
python mqtt_app/main.py
```

2. เชื่อมต่อกับ Broker:
   - กรอกที่อยู่ Broker (ค่าเริ่มต้น: broker.hivemq.com)
   - กรอกพอร์ต (ค่าเริ่มต้น: 1883)
   - กรอก Client ID
   - คลิก "Connect Broker"

3. การ Subscribe หัวข้อ:
   - กรอกชื่อหัวข้อในช่อง Subscribe
   - คลิกปุ่ม "Subscribe"
   - ดูรายการหัวข้อที่ Subscribe ได้จากรายการด้านล่าง
   - ดับเบิลคลิกที่หัวข้อเพื่อคัดลอกไปยังช่อง Publish

4. การ Publish ข้อความ:
   - กรอกชื่อหัวข้อ
   - กรอกข้อความ
   - คลิกปุ่ม "Publish"

## โครงสร้างโปรเจค

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

## ลิขสิทธิ์

MIT License
