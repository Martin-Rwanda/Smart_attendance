from django.core.management.base import BaseCommand
import serial
import json
import time
import requests
import re

class Command(BaseCommand):
    help = "Communicates with Arduino for fingerprint registration and verification"

    def add_arguments(self, parser):
        parser.add_argument('--port', type=str, default='COM3', help='Serial port for Arduino')
        parser.add_argument('--baud', type=int, default=9600, help='Baud rate for communication')
        parser.add_argument('--api', type=str, default='http://127.0.0.1:8000/get_fingerprint/', 
                          help='Django API endpoint')

    def handle(self, *args, **options):
        serial_port = options['port']
        baud_rate = options['baud']
        api_url = options['api']

        self.stdout.write(self.style.SUCCESS(f"Starting Arduino communication on {serial_port}"))
        
        try:
            ser = serial.Serial(serial_port, baud_rate, timeout=1)
            self.stdout.write(self.style.SUCCESS("Connected to Arduino. Listening for data..."))
        except serial.SerialException as e:
            self.stdout.write(self.style.ERROR(f"Error opening serial port: {e}"))
            return

        while True:
            try:
                if ser.in_waiting > 0:
                    line = ser.readline().decode("utf-8").strip()
                    self.stdout.write(f"Received: {line}")
                    
                    # Process fingerprint registration responses
                    if line.startswith("SUCCESS:Fingerprint Saved:"):
                        # Extract the fingerprint ID
                        fingerprint_id = line.split(":")[-1]
                        student_id = fingerprint_id  # In this case they're the same
                        
                        # Send to Django backend
                        data = {
                            "student_id": int(student_id),
                            "fingerprint_data": fingerprint_id
                        }
                        
                        self.stdout.write(f"Sending to Django: {data}")
                        
                        try:
                            response = requests.post(api_url, json=data)
                            if response.status_code == 200:
                                self.stdout.write(self.style.SUCCESS(
                                    f"Successfully registered fingerprint {fingerprint_id} for student {student_id}"
                                ))
                            else:
                                self.stdout.write(self.style.ERROR(
                                    f"Failed to register fingerprint. Status: {response.status_code}, Response: {response.text}"
                                ))
                        except requests.RequestException as e:
                            self.stdout.write(self.style.ERROR(f"API request failed: {e}"))
                    
                    # Process attendance records from fingerprint scanning
                    elif line.startswith("API_CALL:"):
                        match = re.search(r"API_CALL:(\w+), ID: (\d+)", line)
                        if match:
                            action, student_id = match.groups()
                            
                            # Different endpoints based on action
                            action_endpoints = {
                                "check-in": "/attendance/check-in/",
                                "checkout": "/attendance/check-out/",
                                "remove": "/attendance/remove/"
                            }
                            
                            if action in action_endpoints:
                                endpoint = action_endpoints[action]
                                url = f"http://127.0.0.1:8000{endpoint}"
                                
                                data = {"student_id": int(student_id)}
                                
                                try:
                                    response = requests.post(url, json=data)
                                    if response.status_code == 200:
                                        self.stdout.write(self.style.SUCCESS(
                                            f"Successfully processed {action} for student {student_id}"
                                        ))
                                    else:
                                        self.stdout.write(self.style.ERROR(
                                            f"Failed to process {action}. Status: {response.status_code}, Response: {response.text}"
                                        ))
                                except requests.RequestException as e:
                                    self.stdout.write(self.style.ERROR(f"API request failed: {e}"))
                
                time.sleep(0.1)  # Small delay to prevent CPU hogging
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error during communication: {e}"))
                time.sleep(1)  # Longer delay after error