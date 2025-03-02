""" Script for uploading images in LabelStudio projects.
"""

import base64
import requests
import os


from pathlib import Path

if __name__ == "__main__":
    # Replace these values with your actual project ID and API token
    project_id = "52"
    API_KEY = "206577e02d599ccf1ad22b516ade0579d1f2e425"  # replace by your Access Token (see Account & Settings)
    # folder with images to upload
    imgs_folder = Path(os.path.join("for_correction"))
    # The LabelStudio API endpoint for uploading files
    url = f"http://147.33.58.23:8080/api/projects/{project_id}/tasks"
    # Prepare the headers with the API token
    headers = {
        "Authorization": f"Token {API_KEY}",
    }
    # Path to the image file you want to upload
    files_counter = 0
    transfered_images_path = Path(".", "transfered", imgs_folder)
    transfered_images_path.mkdir(exist_ok=True, parents=True)
    for image_file in imgs_folder.glob("*.jpg"):
        data = {
            "data": {
                "image": "data:image/jpg;base64," + base64.b64encode(open(image_file, "rb").read()).decode("utf-8")
            }
        }
        # Send the POST request to upload the image file
        response = requests.post(url, headers=headers, json=data)
        files_counter += 1
        # Check the response from LabelStudio
        if response.status_code == 201:
            print(f"Image {files_counter} uploaded successfully!")
            image_file.rename(transfered_images_path.joinpath(image_file.name))
        else:
            print(f"Failed to upload image. Status code: {response.status_code}, Response: {response.text}")
