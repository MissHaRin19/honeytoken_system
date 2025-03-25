# Honeytoken System

## Project Roadmap

Our project is designed to enhance security by detecting unauthorized access using honeytokens. It is structured into three phases:

### Phase 1: Intrusion Detection Trap
- Initially developed a basic security mechanism where all file accesses redirected to a decoy, triggering an alert.
- https://github.com/MissHaRin19/intrusion_detection_trap

### Phase 2: Honeytoken System (Current Phase)
- Created a system that monitors specific files (honeytokens) for unauthorized access.
- Captures an image of the intruder using a webcam.
- Logs details (file accessed, timestamp, intruder’s IP) into a database.
- Sends an email alert with the captured image and details of the accessed file.

### Phase 3: Honeytoken-Based Intrusion Detection System (Future Work)
- Expand the system to track user behavior over time.
- Implement employee check-in/check-out tracking.
- Enhance anomaly detection to identify suspicious file access patterns.

## Implementation: Honeytoken System

### What We Did

#### Setup Honeytokens
- Placed fake sensitive files (e.g., `Admin_Passwords.txt`, `Secret.pdf`) in a monitored directory.

#### File Monitoring
- Used the `watchdog` library to detect file modifications in real time.

#### Intruder Identification
- Captured an image using OpenCV when a honeytoken was accessed.
- Recorded access details (timestamp, file path, IP address) in an SQLite database.

#### Alert System
- Sent an email notification with the captured image as an attachment.
- Ensured real-time alerts for quick action.

## Database Setup

### Steps to Create the Database

1. Open a terminal and enter the SQLite shell:
   ```sh
   sqlite3 honeytoken.db
   ```
2. Create the `honeypot_logs` table:
   ```sql
   CREATE TABLE honeypot_logs (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       file_path TEXT,
       file_name TEXT,
       captured_image TEXT,
       timestamp TEXT,
       ip_address TEXT
   );
   ```
3. Exit SQLite:
   ```sh
   .exit
   ```

### Why SQLite?

- **Lightweight & Embedded:** No need for a separate database server.
- **Portable:** The database file can be easily transferred.
- **Simple & Effective:** Ideal for logging security events with minimal overhead.

