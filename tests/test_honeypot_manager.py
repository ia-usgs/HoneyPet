import subprocess
import platform
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.json_manager import JSONManager
from honeypots.honeypot_manager import HoneypotManager

def test_honeypot_manager():
    print("Testing HoneypotManager...")
    manager = HoneypotManager()

    # Test starting all honeypots
    print("\nStarting all honeypots...")
    manager.start_all()

    # Test checking status
    print("\nChecking status of all honeypots...")
    manager.check_status()

    # Test processing logs
    print("\nProcessing logs for all honeypots...")
    manager.process_all_logs()

    # Test stopping all honeypots
    print("\nStopping all honeypots...")
    manager.stop_all()

    print("\nHoneypotManager tests completed.")

if __name__ == "__main__":
    test_honeypot_manager()
