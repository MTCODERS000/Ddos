from instagrapi import Client
import requests

def send_image_in_loop(image_url):
    # Get user input for credentials and recipient
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    recipient_username = input("Enter the recipient's username: ")

    try:
        # Initialize Instagram Client
        client = Client()

        # Attempt to load session or log in
        try:
            client.load_settings("session.json")
            client.login(username, password)
            print("Session loaded and logged in successfully!")
        except Exception:
            print("Unable to load session, logging in from scratch...")
            client.login(username, password)
            client.dump_settings("session.json")
            print("Logged in and session saved.")

        # Get the user ID of the recipient
        try:
            user_id = client.user_id_from_username(recipient_username)
            print(f"Recipient User ID: {user_id}")
        except Exception as e:
            print(f"Failed to fetch user ID for '{recipient_username}': {e}")
            return

        # Download the image from the URL
        image_path = "temp_image.jpg"
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image downloaded and saved as {image_path}")
        else:
            print(f"Failed to download the image. Status Code: {response.status_code}")
            return

        # Send the image in a loop with minimal delay
        while True:
            try:
                # Send the image to the recipient
                client.direct_send_photo(image_path, user_ids=[user_id])
                print(f"Image sent to {recipient_username}.")
            except Exception as e:
                print(f"Error sending image: {e}")
                continue

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Image URL to send
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7eEL2EX7-UScYdYtrpYQ_5xaJZvc452kcAg&usqp=CAU"

# Start the bot
send_image_in_loop(image_url) 
