import subprocess
import os
import json
import time
from core.json_manager import JSONManager

class CowrieController:
    def __init__(self):
        self.cowrie_path = "/home/pi/HoneyPet/honeypots/cowrie/bin/cowrie"
        self.logs_path = "/home/pi/HoneyPet/honeypots/cowrie/var/log/cowrie/cowrie.json"
        self.json_manager = JSONManager()
        self.report_path = "reports/json/cowrie_activity.json"  # HoneyPet log output path
        self.service_name = "cowrie"

    def start(self):
        """Start the Cowrie honeypot."""
        print(f"Starting {self.service_name} honeypot...")
        try:
            # Check if Cowrie is already running
            result = subprocess.run(["pgrep", "-f", "twistd"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{self.service_name} is already running (PID: {result.stdout.strip()}).")
                return  # Exit without starting again

            # Start Cowrie
            subprocess.run(["systemctl", "start", self.service_name], check=True)
            print(f"{self.service_name} started successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to start {self.service_name}: {e}")

    def stop(self):
        """Stop the Cowrie honeypot."""
        print(f"Stopping Cowrie honeypot...")
        try:
            subprocess.run(["bash", self.cowrie_path, "stop"], check=True)
            print("Cowrie stopped successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to stop Cowrie: {e}")

    def status(self):
        """Check the status of the Cowrie honeypot."""
        print(f"Checking status of Cowrie honeypot...")
        try:
            subprocess.run(["bash", self.cowrie_path, "status"], check=True)
        except Exception as e:
            print(f"Failed to check status of Cowrie: {e}")

    def process_logs(self):
        """Process Cowrie's JSON logs and store them in the HoneyPet format."""
        print(f"Processing logs from {self.logs_path}...")
        if not os.path.exists(self.logs_path):
            print(f"No logs found at {self.logs_path}")
            return

        with open(self.logs_path, "r") as log_file:
            for line in log_file:
                try:
                    log_entry = json.loads(line.strip())
                    timestamp = log_entry.get("timestamp", "N/A")
                    src_ip = log_entry.get("src_ip", "N/A")
                    activity = log_entry.get("eventid", "N/A")
                    self.log_activity(timestamp, src_ip, activity)
                except json.JSONDecodeError:
                    print("Failed to decode log entry.")

    def log_activity(self, timestamp, src_ip, activity):
        """Log activity to HoneyPet JSON format."""
        print(f"Logging activity: {timestamp}, {src_ip}, {activity}")
        data = {
            "title": "Cowrie Activity Log",
            "headers": ["Timestamp", "Source IP", "Activity"],
            "rows": []
        }

	# Ensure the reports/json directory exists
        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)
        new_row = [timestamp, src_ip, activity]
        try:
            self.json_manager.append_to_json(new_row, self.report_path)
        except FileNotFoundError:
            data["rows"].append(new_row)
            self.json_manager.create_json(data, self.report_path)
