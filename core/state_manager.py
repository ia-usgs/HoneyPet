import time
from core.json_manager import JSONManager
from core.html_generator import HTMLGenerator

class StateManager:
    def __init__(self):
        self.state = "Booting"  # Initial state
        self.json_manager = JSONManager()
        self.html_generator = HTMLGenerator()

        # Paths for reports
        self.json_path = "reports/json/state_report.json"
        self.html_path = "reports/html/state_report.html"

        # Initialize states and transitions
        self.states = ["Booting", "Monitoring", "Engaged", "Alert", "Idle"]
        self.transition_triggers = {
            "Booting": self.transition_to_monitoring,
            "Monitoring": self.transition_to_engaged,
            "Engaged": self.transition_to_alert,
            "Alert": self.transition_to_idle,
            "Idle": self.transition_to_monitoring,
        }

    def transition_to_monitoring(self):
        print("Transitioning to Monitoring State")
        self.state = "Monitoring"
        self.log_state("Monitoring")

    def transition_to_engaged(self):
        print("Transitioning to Engaged State")
        self.state = "Engaged"
        self.log_state("Engaged")

    def transition_to_alert(self):
        print("Transitioning to Alert State")
        self.state = "Alert"
        self.log_state("Alert")

    def transition_to_idle(self):
        print("Transitioning to Idle State")
        self.state = "Idle"
        self.log_state("Idle")

    def log_state(self, state):
        """
        Log the current state to the JSON file and generate an HTML report.
        """
        # Define the log entry
        data = {
            "title": "State Transition Report",
            "headers": ["Timestamp", "State"],
            "rows": []
        }

        # Append a new row for the state transition
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        new_row = [timestamp, state]

        try:
            self.json_manager.append_to_json(new_row, self.json_path)
        except FileNotFoundError:
            # If the JSON file doesn't exist, create it
            data["rows"].append(new_row)
            self.json_manager.create_json(data, self.json_path)

        # Generate the HTML report
        json_data = self.json_manager.read_json(self.json_path)
        self.html_generator.generate_html(json_data, self.html_path)

    def run(self):
        """
        Main loop to manage state transitions.
        """
        while True:
            print(f"Current State: {self.state}")
            
            # Trigger state transitions based on the current state
            if self.state in self.transition_triggers:
                self.transition_triggers[self.state]()
            
            # Simulate a delay between state transitions
            time.sleep(5)
