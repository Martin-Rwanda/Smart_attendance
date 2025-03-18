from django.core.management.base import BaseCommand
import serial
import requests
import json

class Command(BaseCommand):
    help = "Reads fingerprint data from Arduino and sends it to Django"

    def handle(self, *args, **kwargs):
        SERIAL_PORT = "COM3"  # Change this based on your OS
        BAUD_RATE = 9600
        DJANGO_API_URL = "http://127.0.0.1:8000/get_fingerprint/"

        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            self.stdout.write(self.style.SUCCESS("Listening for fingerprint data..."))
        except serial.SerialException as e:
            self.stdout.write(self.style.ERROR(f"Error opening serial port: {e}"))
            return

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
                            self.stdout.write(self.style.SUCCESS(f"Sent: {data}, Response: {response.json()}"))
                        else:
                            self.stdout.write(self.style.ERROR(f"Failed to send data. Status Code: {response.status_code}, Response: {response.text}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error during communication: {e}"))