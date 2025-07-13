import os
from datetime import datetime
import requests


class FileHandler:
    def __init__(self, base_folder):
        self.base_folder = base_folder
        self.setup_folder()

    def setup_folder(self):
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)
            print(f"Created folder at: {self.base_folder}")

    def clean_filename(self, filename):
        return "".join(x for x in filename if x.isalnum() or x in (' ', '-', '_'))

    def download_image(self, image_url, title, headers=None):
        try:
            safe_title = self.clean_filename(title)[:50]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_title}_{timestamp}.jpg"
            filepath = os.path.join(self.base_folder, filename)

            headers = headers or {}
            response = requests.get(image_url, headers=headers)

            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath

            print(f"Failed to download image. Status: {response.status_code}")
            return None

        except Exception as e:
            print(f"Error downloading image: {e}")
            return None