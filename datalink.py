#### Datalink.py handles createing and xfering the tricaster datalink file
import os
import shutil
import csv
import logging
import math
from candidates import Candidate
from contests import Contest

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def copy_to_tricaster(source_datalink_file):
    # retrieve values from Environment (see load_config.py)
    tricaster_host = os.getenv("TRICASTER_HOST")
    tricaster_datalink_path = os.getenv("TRICASTER_PATH")
    tricaster_user = os.getenv("TRICASTER_USER")
    tricaster_pwd = os.getenv("TRICASTER_PWD")

    if tricaster_host is None or tricaster_host == "None":
        logger.info("No tricaster defined, dont copy file")
        return

    # Construct the network path
    network_path = f"\\\\{tricaster_host}\\{tricaster_datalink_path}"

    # Check if the network path is already accessible using os.popen()
    with os.popen(f'dir {network_path}') as stream:
        output = stream.read()

    # If the network path is not accessible, attempt to mount it
    if "File Not Found" in output or "cannot find" in output.lower():
        print(f"Network path {network_path} not accessible, attempting to mount...")
        with os.popen(f'net use {network_path} /user:{tricaster_user} {tricaster_pwd}') as mount_stream:
            mount_output = mount_stream.read()
            logger.info(f"Opened Tricaster {mount_output} {network_path}")
    else:
        logger.debug(f"Network path {network_path} is already accessible.")

    # Construct the destination file path
    destination_file = os.path.join(network_path, 'datalink.csv')

    # Copy the file to the Tricaster folder
    try:
        shutil.copy(datalink_file_path, destination_file)
        logger.info(f"File copied successfully to {destination_file}")
    except Exception as e:
        logger.warning(f"Failed to copy file to tricaster: {e}")


def write_datalink(contests, candidates, datalink_filepath):
    try:
        print(f"Writing datalink to {datalink_filepath}")
        with open(datalink_filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for contest_id, contest in contests.items():
                writer.writerow([contest.datalink_id, contest.datalink_value])
                logging.debug(f"contest {contest_id} blank {contest.blank} over {contest.over}")
                writer.writerow([f"{contest.datalink_id}-blankover-COUNT", contest.bad_boi,
                                 f"{contest.datalink_id}-blankover-PCT", f"{contest.percent_bad_boi}%"])

                for candidate in candidates.values():
                    if candidate.contest_id == contest_id:
                        candidate_fields = [
                            candidate.datalink_id,
                            candidate.datalink_value,
                            f"{candidate.datalink_id}-VOTE",
                            candidate.total_votes,
                            f"{candidate.datalink_id}-PCT",
                            f"{candidate.percent_votes}%"
                        ]
                        writer.writerow(candidate_fields)
        logger.info(f"DataLink file written to {datalink_filepath}")
    except Exception as e:
        logger.error(f"Error writing DataLink file: {e}")
        raise
