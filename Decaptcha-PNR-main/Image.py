import os
import requests


def download_image(url, save_path):
    try:
        # Send an HTTP GET request to fetch the image data
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Get the file extension from the URL
        file_extension = os.path.splitext(url.split("/")[-1])[1]

        # Save the image to the specified location
        with open(save_path + file_extension, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print("Image downloaded successfully.")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return False


# Example usage:
if __name__ == "__main__":
    for i in range(1):
        image_url = "https://www.indianrail.gov.in/enquiry/captchaDraw.png"
        save_location = "predict/" + str(i)
        download_image(image_url, save_location)
