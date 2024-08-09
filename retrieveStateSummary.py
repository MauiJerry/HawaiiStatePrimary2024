import os
import time
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import logging
import chardet
import shutil

logger = logging.getLogger(__name__)

# URL and file paths
website_url = 'http://elections.hawaii.gov/files/media.txt'
summary_url = 'https://go-elections.hawaii.gov/media-results/files/summary.txt'

# User credentials
username = 'akaku.maui.media'
password = 'TheElectionOfHawaii!!'


# Function to check for updates on the website
def check_for_updates():
    response = requests.head(summary_url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        return response.headers['Last-Modified']
    return None


# Function to download the updated CSV file with a timestamp
def download_summary(local_folder):
    response = requests.get(summary_url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        timestamped_file_path = os.path.join(local_folder, f'summary_{timestamp}.txt')
        with open(timestamped_file_path, 'wb') as file:
            file.write(response.content)
        return timestamped_file_path
    else:
        logger.warning(f"Failed to download file. Status code: {response.status_code}")
        return None


def detect_encoding(file_path):
    """Detect the encoding of a file using the chardet library."""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']

        return encoding, confidence


def convert_to_utf8(input_file_path, temp_file_path):
    """Convert a file to UTF-8 encoding."""
    try:
        with open(input_file_path, 'r', encoding='utf-16') as f:
            content = f.read()

        with open(temp_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"File {input_file_path} has been successfully converted to UTF-8 and saved as {temp_file_path}")
    except Exception as e:
        logger.error(f"Error converting {input_file_path} to UTF-8: {e}")
        raise


def strip_file(filepath):
    try:
        # Read the file and find the line starting with "#Contest ID"
        with open(filepath, 'r') as file:
            lines = file.readlines()

        if lines[0].startswith("Format#"):
            if not lines[0].startswith("Format#1"):
                raise ValueError(f"downloaded file {filepath} is NOT Format#1")
            else:
                print("web file is still Format#1")

        # Find the index of the line that starts with "#Contest ID"
        start_index = next((i for i, line in enumerate(lines) if line.startswith("#Contest ID")), None)

        if start_index is None:
            raise ValueError(f"No line starting with '#Contest ID' found in file: {filepath}")

        # Extract content from the found line to the end
        stripped_content = lines[start_index:]

        # Create a new file path with the '.striped.txt' extension
        base, _ = os.path.splitext(filepath)
        new_filepath = f"{base}.striped.txt"

        # Write the extracted content to the new file
        with open(new_filepath, 'w') as new_file:
            new_file.writelines(stripped_content)

        return filepath, new_filepath

    except Exception as e:
        return str(e), None


def ensure_utf8(file_path):
    """Ensure that a CSV file is UTF-8 encoded. If not, convert it."""
    encoding, confidence = detect_encoding(file_path)

    if encoding.lower() == 'utf-8':
        logger.info(f"The file is UTF-8 encoded with confidence {confidence}.")
        return file_path
    else:
        logger.info(f"Converting file from {encoding} to UTF-8.")
        temp_file_path = file_path + '.utf8'
        convert_to_utf8(file_path, temp_file_path)
        return temp_file_path


def check_download_summary(local_folder):
    if not hasattr(check_download_summary, "last_modified_time"):
        check_download_summary.last_modified_time = 'None'  # Initialize the static variable
    current_modified_time = check_for_updates()

    retPath = None
    logger.debug(f"current mod time {current_modified_time} last mod time{check_download_summary.last_modified_time}")
    if current_modified_time and current_modified_time != check_download_summary.last_modified_time:
        logger.info("New update found. Downloading CSV...")
        local_summary_path = download_summary(local_folder)
        if local_summary_path:
            print("Download is at ", local_summary_path)
            utf8_file_path = ensure_utf8(local_summary_path)
            logger.debug("download in utf is at" + utf8_file_path)

            origPath, newPath = strip_file(utf8_file_path)
            retPath = origPath
            if newPath:
                logger.info("updated (stripped 1st line) at" + newPath)
                retPath = newPath
            else:
                logger.info("no need to strip lines use " + origPath)
            check_download_summary.last_modified_time = current_modified_time
    else:
        logger.info("no update on web " + summary_url)
    return retPath


def copy_to_summary(input_filepath):
    # Define the destination directory and filename
    destination_dir = 'data'
    destination_filename = 'summary.csv'
    destination_filepath = os.path.join(destination_dir, destination_filename)

    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Copy the file to the destination, overwriting if necessary
    shutil.copyfile(input_filepath, destination_filepath)
    logger.info(f"Copied {input_filepath} to {destination_filepath}")


intervalTime = 60 * 1


# Main function to monitor and process updates
def main():
    os.makedirs(local_folder, exist_ok=True)

    while True:
        path = check_download_summary()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if path:
            print("Main: updated at", timestamp, " new file path is ", path)
            copy_to_summary(path)
        else:
            print("No Update", timestamp)
        time.sleep(intervalTime)  # Check for updates every interval seconds


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s')

    main()
