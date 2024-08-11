import os
import time
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import logging
import chardet
import shutil
import difflib
from load_config import load_config_env

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# These are set from config.env on first attempt

# URL and file paths
website_url = 'http://elections.hawaii.gov/files/media.txt'

fake_data_file = "./data/fake_summary.txt"

last_lastModified = None
# Function to check for updates on the website
def check_for_updates():
    global summary_url, username, password
    global last_lastModified

    summary_url = os.getenv("SUMMARY_URL")
    username = os.getenv("HI_USERNAME")
    password = os.getenv("HI_PASSWORD")

    logger.debug(f" \n\tChecking for updates: {summary_url}, u: {username} p:{password}")

    response = requests.head(summary_url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        cur_lastModified = response.headers['Last-Modified']

        if last_lastModified == cur_lastModified:
            logger.debug(f" NO CHANGE: last LastMod {last_lastModified} same as cur {cur_lastModified}")
            print(f" NO CHANGE: last LastMod {last_lastModified} same as cur {cur_lastModified}")
            return last_lastModified
        logger.debug(f" ** CHANGED: last LastMod {last_lastModified} same as cur {cur_lastModified}")
        print(f" ** CHANGED: last LastMod {last_lastModified} same as cur {cur_lastModified}")
        last_lastModified = cur_lastModified
        return cur_lastModified
    else:
        logger.debug(f"Request response is:{response.status_code}")
    return None

# Function to download the updated CSV file with a timestamp
def download_summary(local_folder):
    global summary_url, username, password
    summary_url = os.getenv("SUMMARY_URL")
    username = os.getenv("HI_USERNAME")
    password = os.getenv("HI_PASSWORD")

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


def convert_to_ascii(input_file_path, temp_file_path, encoding):
    """Convert a file to UTF-8 encoding."""
    try:
        with open(input_file_path, 'r', encoding=encoding) as f:
            content = f.read()

        with open(temp_file_path, 'w', encoding='ascii') as f:
            f.write(content)

        logger.info(f"File {input_file_path} has been successfully converted to UTF-8 and saved as {temp_file_path}")
    except Exception as e:
        logger.error(f"Error converting {input_file_path} to UTF-8: {e}")
        raise


def ensure_ascii(file_path):
    """Ensure that a CSV file is UTF-8 encoded. If not, convert it."""
    encoding, confidence = detect_encoding(file_path)
    logger.debug(f"file {file_path} encoding is {encoding} confidence {confidence}")

    if encoding.lower() == 'ascii':
        logger.info(f"The file is UTF-8 encoded with confidence {confidence}.")
        return file_path
    else:
        logger.info(f"Converting file from {encoding} to ascii.")
        temp_file_path = file_path + '.ascii'
        convert_to_ascii(file_path, temp_file_path, encoding)
        return temp_file_path

def strip_file(filepath):
    global _state_file_is_hold
    logger.debug(f"strip_file({filepath})")
    try:
        # Read the file and find the line starting with "#Contest ID"
        with open(filepath, 'r') as file:
            lines = file.readlines()

        if lines[0].startswith("Format#"):
            if not lines[0].startswith("Format#1"):
                raise ValueError(f"downloaded file {filepath} is NOT Format#1")
            else:
                logger.debug(f"first line seems to be Format1: {lines[0]}")
                print("web file is still Format#1")
        else:
            if lines[0].startswith("Information will be posted at a later date."):
                logger.warning("Downloaded file is HOLD, State Has Not Posted real data")
                return filepath, fake_data_file

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

        _state_file_is_hold = False
        return filepath, new_filepath

    except Exception as e:
        return str(e), None


last_used_file = None
def check_download_summary(local_folder):
    global last_used_file

    if not hasattr(check_download_summary, "last_modified_time"):
        check_download_summary.last_modified_time = 'None'  # Initialize the static variable
        logger.debug(f"first time using check_download")
        # load_config_env()

    current_modified_time = check_for_updates()

    retPath = None
    logger.debug(f"Check Download \n\tcurrent mod time {current_modified_time} \n\tlast mod time{check_download_summary.last_modified_time}")
    if current_modified_time and current_modified_time != check_download_summary.last_modified_time:
        logger.info("New update found. Downloading CSV...")
        local_summary_path = download_summary(local_folder)
        if local_summary_path:
            print("Download is at ", local_summary_path)
            utf8_file_path = ensure_ascii(local_summary_path)
            logger.debug("download in utf is at" + utf8_file_path)

            origPath, newPath = strip_file(utf8_file_path)
            retPath = origPath
            if newPath:
                if newPath == fake_data_file:
                    logger.warning("FAKE DATA loaded")
                logger.debug("updated (stripped 1st line) at" + newPath)
                retPath = newPath
            else:
                logger.info("no need to strip lines use " + origPath)

            if last_used_file is None:
                last_used_file = retPath
            elif retPath == last_used_file:
                #no difference, set to None
                print("retpath == last_used_file")
                retPath = None
            else:
                # test if the contents are different
                with open(retPath,'r') as newFile, open(last_used_file,'r') as lastFile:
                    newLines = newFile.readlines()
                    lastLines = lastFile.readlines()
                    unified = difflib.unified_diff(newLines,lastLines, fromfile=retPath, tofile=last_used_file)
                    diffences = list(unified)
                    print(diffences)
                    if len(diffences) == 0:
                        logger.debug(f"new file and last file compare as NO DIFFERENCE")
                        print(f"   NO DIFFERENCE in new and last file")
                        retPath = None
                    else:
                        print("    New File is different!")


            check_download_summary.last_modified_time = current_modified_time
            last_used_file = retPath
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
    local_folder = "./download"
    os.makedirs(local_folder, exist_ok=True)
    load_config_env()

    while True:
        path = check_download_summary(local_folder)
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
