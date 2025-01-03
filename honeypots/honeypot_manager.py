from honeypots.cowrie_controller import CowrieController

class HoneypotManager:
    def __init__(self):
        # Initialize honeypot controllers
        self.honeypots = {
            "cowrie": CowrieController(),
            # Additional honeypots can be added here
        }

    def start_all(self):
        """
        Start all honeypot services.
        """
        for name, controller in self.honeypots.items():
            print(f"Starting {name} honeypot...")
            controller.start()

    def stop_all(self):
        for name, controller in self.honeypots.items():
            if name == "cowrie":
                print(f"Skipping stopping {name} honeypot to keep it running...")
                continue
            print(f"Stopping {name} honeypot...")
            controller.stop()

    def check_status(self):
        """
        Check the status of all honeypot services.
        """
        for name, controller in self.honeypots.items():
            print(f"Checking status of {name} honeypot...")
            controller.status()

    def process_all_logs(self):
        """
        Process logs from all honeypots.
        """
        for name, controller in self.honeypots.items():
            print(f"Processing logs for {name} honeypot...")
            controller.process_logs()
