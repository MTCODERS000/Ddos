from instagrapi import Client
import time
import requests

# Your credentials
username = "your_username"
password = "your_password"

# Login to Instagram
cl = Client()
cl.login(username, password)

# Image URL and caption
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTaZdcNAGxmogv0EClUmn1m6etMN-aNDdvf8THj2jB6zUg6MPL0-0mRHx0&s=10"
caption = "😳💏👄💋"

# Download image
img_data = requests.get(image_url).content
with open('temp_image.jpg', 'wb') as f:
    f.write(img_data)

# Loop to post the image
while True:
    try:
        # Post the image with caption
        cl.photo_upload('temp_image.jpg', caption)
        print(f"Image posted successfully with caption: {caption}")
        
        # Wait before posting again (you can adjust the sleep time as needed)
        time.sleep(10)  # Adjust the sleep time (in seconds)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        break 
