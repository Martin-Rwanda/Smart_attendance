import serial
import requests
import json

# Serial Port Configuration
SERIAL_PORT = "COM3"  # Change this based on your OS
# SERIAL_PORT = "/dev/ttyUSB0"  # For Linux (use `ls /dev/tty*` to find your port)
BAUD_RATE = 9600

# Django API Endpoint (Corrected URL)
DJANGO_API_URL = "http://127.0.0.1:8000/get_fingerprint/"

# Open Serial Connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print("Listening for fingerprint data...")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

while True:
    try:
        if ser.in_waiting > 0:
            fingerprint_id = ser.readline().decode("utf-8").strip()

            if fingerprint_id.isdigit():
                data = {
                    "student_id": int(fingerprint_id),
                    "names": f"Student {fingerprint_id}",
                    "fingerprint_data": f"Template_{fingerprint_id}"
                }

                response = requests.post(DJANGO_API_URL, json=data)

                if response.status_code == 200:
                    print(f"Sent: {data}, Response: {response.json()}")
                else:
                    print(f"Failed to send data. Status Code: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print(f"Error during communication: {e}")