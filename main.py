from core.state_manager import StateManager
from honeypots.honeypot_manager import HoneypotManager
from core.log_monitor import LogMonitor
import time

class HoneyPet:
    def __init__(self):
        # Initialize the State Manager and Honeypot Manager
        self.state_manager = StateManager()
        self.honeypot_manager = HoneypotManager()
        # Initialize LogMonitor with the Cowrie log path and state transition function
        self.inactivity_timeout = 30  # Set inactivity timeout (in seconds)
        self.last_activity_time = time.time()  # Track the last time activity occurred
        self.log_monitor = LogMonitor(
            log_path="/home/pi/HoneyPet/honeypots/cowrie/var/log/cowrie/cowrie.json",
            transition_state_callback=self.transition_state,
            reset_timer_callback=self.reset_activity_timer  # Pass reset timer callback
        )

    def reset_activity_timer(self):
        """Reset the inactivity timer."""
        self.last_activity_time = time.time()

    def transition_state(self, new_state):
        """Transition to a new state and handle actions."""
        print(f"Transitioning to {new_state} State")
        self.state_manager.state = new_state

    def run(self):
        print("Starting HoneyPet...")

        # Main loop to integrate functionality
        while True:
            try:
                # Check the current state
                current_state = self.state_manager.state
                print(f"Current State: {current_state}")

                if current_state == "Booting":
                    print("Booting up the system...")
                    self.state_manager.transition_to_monitoring()

                elif current_state == "Monitoring":
                    print("Monitoring network activity...")
                    self.honeypot_manager.start_all()

                    # Start monitoring logs in real-time
                    self.log_monitor.monitor_logs()

                elif current_state == "Engaged":
                    print("Engaged state active. Processing logs...")

                    # Check for inactivity timeout
                    if time.time() - self.last_activity_time > self.inactivity_timeout:
                        print("No activity detected. Transitioning to Idle state...")
                        self.state_manager.transition_to_idle()
                    else:
                        # Process logs and reset the timer if activity occurs
                        self.honeypot_manager.process_all_logs()
                        time.sleep(5)  # Check logs every 5 seconds

                elif current_state == "Alert":
                    print("Alert state active. Checking for critical issues...")
                    self.honeypot_manager.check_status()
                    time.sleep(5)
                    self.state_manager.transition_to_idle()

                elif current_state == "Idle":
                    print("Idle state. Stopping all honeypots to conserve resources...")
                    self.honeypot_manager.stop_all()
                    time.sleep(10)  # Simulate idle period
                    self.state_manager.transition_to_monitoring()

            except KeyboardInterrupt:
                print("Stopping HoneyPet...")
                self.honeypot_manager.stop_all()
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    honeypet = HoneyPet()
    honeypet.run()
