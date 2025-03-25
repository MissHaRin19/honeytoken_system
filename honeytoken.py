import os
import smtplib
import time
import cv2
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sqlite3
import socket

DB_PATH = os.path.expanduser("~/honeytoken/honeytoken.db")

def get_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print(f"Error fetching IP: {e}")
        return "Unknown"

def save_to_db(file_path, image_filename):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file_name = os.path.basename(file_path)
        ip_address = get_ip()

        cursor.execute(
            "INSERT INTO honey_token (file_path, file_name, captured_image, timestamp, ip_address) VALUES (?, ?, ?, ?, ?)",
            (file_path, file_name, image_filename, timestamp, ip_address)
        )

        conn.commit()
        conn.close()
        print("Logged access to database.")

    except sqlite3.OperationalError as e:
        print(f"Database error: {e} - Check if the table exists.")

# List of honeytoken files
HONEYTOKENS = [
    os.path.expanduser("~/honeytoken/fake/Secret.pdf"),
    os.path.expanduser("~/honeytoken/fake/Admin_Passwords.txt"),
    os.path.expanduser("~/honeytoken/fake/Payroll_2024.xlsx"),
]

# Email details
SENDER_EMAIL = "gentleefforts@gmail.com"
RECEIVER_EMAIL = "160622733108@stanley.edu.in"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
APP_PASSWORD = "prxitcmadaispqqi"  # Store in environment variable!

SUBJECT = "Honeytoken Alert"
BODY = "A honeytoken file was accessed! Attached is the intruder's image."

# Define webcam capture function
def capture_image():
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    ret, frame = cap.read()
    if ret:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_filename = os.path.expanduser(f"~/honeytoken/captured_{timestamp}.jpg")
        cv2.imwrite(image_filename, frame)
        print(f"Captured image: {image_filename}")
    else:
        print("Failed to capture image.")
        image_filename = None
    cap.release()
    return image_filename

# Send email function with image attachment
def send_email(image_filename, accessed_file):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = SUBJECT
    msg.attach(MIMEText(f"The file {accessed_file} was accessed!\n\n{BODY}", 'plain'))

    if image_filename:
        with open(image_filename, 'rb') as image_file:
            img = MIMEImage(image_file.read())
            img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_filename))
            msg.attach(img)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            print(f"Email sent successfully for {accessed_file}!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# File access handler
class HoneytokenHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer  # Store observer reference

    def on_modified(self, event):
        if not event.is_directory and event.src_path in HONEYTOKENS:
            print(f"Honeytoken {event.src_path} was accessed!")
            image_filename = capture_image()
            save_to_db(event.src_path, image_filename)
            send_email(image_filename, event.src_path)

            # Stop observer and exit the script after first detection
            self.observer.stop()
            sys.exit(0)  # Ensures script stops

# Start monitoring function
def start_monitoring():
    observer = Observer()
    event_handler = HoneytokenHandler(observer)
    for file in HONEYTOKENS:
        observer.schedule(event_handler, os.path.dirname(file), recursive=False)
    observer.start()
    print("Monitoring honeytokens for access...")
    try:
        while observer.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()
