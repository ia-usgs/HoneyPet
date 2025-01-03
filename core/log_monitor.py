import time
import json

class LogMonitor:
    def __init__(self, log_path, transition_state_callback, reset_timer_callback=None):
        """
        Initialize the LogMonitor.

        Args:
            log_path (str): Path to the log file to monitor.
            transition_state_callback (function): Function to call when a state transition is needed.
            reset_timer_callback (function): Function to reset the inactivity timer.
        """
        self.log_path = log_path
        self.transition_state_callback = transition_state_callback
        self.reset_timer_callback = reset_timer_callback  # Store the callback

    def monitor_logs(self):
        """Monitor the log file for suspicious activity in real-time."""
        print(f"Monitoring logs at {self.log_path}...")
        try:
            with open(self.log_path, "r") as log_file:
                # Move to the end of the file
                log_file.seek(0, 2)

                while True:
                    line = log_file.readline()
                    if not line:
                        time.sleep(1)  # Wait for new logs
                        continue

                    try:
                        log_entry = json.loads(line.strip())
                        event_id = log_entry.get("eventid", "")
                        src_ip = log_entry.get("src_ip", "")
                        username = log_entry.get("username", "N/A")
                        password = log_entry.get("password", "N/A")

                        # Handle specific events
                        if event_id == "cowrie.login.failed":
                            print(f"FAILED LOGIN: {username}/{password} from {src_ip}")
                            self.transition_state_callback("Alert")
                            if self.reset_timer_callback:
                                self.reset_timer_callback()  # Reset the timer on activity

                        elif event_id == "cowrie.login.success":
                            print(f"SUCCESSFUL LOGIN: {username}/{password} from {src_ip}")
                            self.transition_state_callback("Engaged")
                            if self.reset_timer_callback:
                                self.reset_timer_callback()  # Reset the timer on activity

                        elif event_id == "cowrie.command.input":
                            command = log_entry.get("input", "")
                            print(f"COMMAND EXECUTED by {src_ip}: {command}")
                            self.transition_state_callback("Engaged")
                            if self.reset_timer_callback:
                                self.reset_timer_callback()  # Reset the timer on activity

                    except json.JSONDecodeError:
                        continue

        except FileNotFoundError:
            print(f"Error: Log file {self.log_path} not found.")
