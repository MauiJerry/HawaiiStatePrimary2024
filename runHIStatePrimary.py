import os
import time
import logging
from candidates import Candidate, list_candidates
from contests import Contest, list_contests
from results import load_results, finalize_results
from datalink import write_datalink, copy_to_tricaster, copy_to_sharedFolder
from retrieveStateSummary import check_download_summary, fake_data_file
from makeDocx import generate_opendoc
import shutil
from datetime import datetime
import win32print
import win32api

from load_config import load_config_env

check_state_interval = 60 * 1 # 60sec * N minutes
doDownload = True

# Configure local logger
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

# Define the data folder and file names
data_folder = "./data"
download_folder = "./download"
datalink_folder = "./datalink"
output_folder = "./output"

contest_file_name = "ContestKey.csv"
candidate_file_name = "CandidateKey.csv"
results_file_name = "results.csv"
datalink_file_name = "datalink.csv"
state_summary_file_name = "summary.csv"
docx_base_name = "primary_results"


def print_file(file_path):
    global actually_print
    # Get the default printer
    printer_name = win32print.GetDefaultPrinter()
    # Set the printer to disable duplex mode
    # would b nice do force single sided but currently SetPrinter fives access denied error
    # printer_name = win32print.GetDefaultPrinter()
    # printer_handle = win32print.OpenPrinter(printer_name)
    # printer_info = win32print.GetPrinter(printer_handle, 2)
    # devmode = printer_info['pDevMode']
    #
    # # Disable duplex (set to 1 for no duplex)
    # devmode.Duplex = 1
    #
    # # Apply the settings
    # win32print.SetPrinter(printer_handle, 2, printer_info, 0)
    # win32print.ClosePrinter(printer_handle)

    actually_print = os.getenv("ACTUALLY_PRINT")
    if actually_print == "TRUE":
        actually_print = True
    else:
        actually_print = False

    # Print the file
    print(f"Printing {file_path} on {printer_name}")
    if actually_print:
        win32api.ShellExecute(
            0,
            "print",
            file_path,
            f'/d:"{printer_name}"',
            ".",
            0
        )
    else:
        print("but not really")


def copy_summary_to_data(input_filepath):
    # Define the destination directory and filename
    destination_filename = 'summary.csv'
    destination_filepath = os.path.join(data_folder, destination_filename)

    # Copy the file to the destination, overwriting if necessary
    shutil.copyfile(input_filepath, destination_filepath)
    logger.info(f"Copied {input_filepath} to {destination_filepath}")


def runHIStatePrimary():
    global contest_file_path, candidate_file_path, results_file_path, datalink_file_path
    global state_summary_file_path

    load_config_env()

    check_state_interval = 60 * int(os.getenv("SLEEP_MINUTES"))
    logger.info(f"Sleep seconds {check_state_interval}")

    datalink_folder = os.getenv("DATALINK_FOLDER")
    print("Main: datalink_folder", datalink_folder)

    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(download_folder, exist_ok=True)
    os.makedirs(datalink_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Construct the file paths
    contest_file_path = os.path.join(data_folder, contest_file_name)
    candidate_file_path = os.path.join(data_folder, candidate_file_name)
    results_file_path = os.path.join(data_folder, results_file_name)
    datalink_file_path = os.path.join(datalink_folder, datalink_file_name)
    state_summary_file_path = os.path.join(data_folder, state_summary_file_name)
    # Load candidates and contests

    candidates = Candidate.from_csv(candidate_file_path)
    logger.debug(f"Candidates loaded: {candidates}")
    # list_candidates(candidates)
    contests = Contest.from_csv(contest_file_path)
    logger.debug(f"Contests loaded: {candidates}")

    wait_for_real_data = os.getenv("WAIT_FOR_REAL")
    if wait_for_real_data == "TRUE":
        wait_for_real_data = True
    else:
        wait_for_real_data = False
    logger.info(f"wait_for_real_data {wait_for_real_data}")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')

    # Enter an infinite loop to check for updates
    while True:
        # Retrieve the state summary
        if doDownload:
            path = check_download_summary(download_folder)
        else:
            path = state_summary_file_path
        if path == fake_data_file and wait_for_real_data:
            logger.info("State has not posted real data yet, continue Waiting\n")
            continue

        # If a new summary file is retrieved, process it
        if path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            if doDownload:
                shutil.copy(path, state_summary_file_path)
                logger.info(f"{timestamp} Copied new state summary to {state_summary_file_path}")

            # Load results and update candidates and contests
            load_results(state_summary_file_path, candidates, contests)
            finalize_results(contests, candidates)

            # Export the processed data
            write_datalink(contests, candidates, datalink_file_path)

            copy_data_link_name = os.path.join(output_folder, f'{datalink_file_name}_{timestamp}.csv')
            shutil.copy(datalink_file_path, copy_data_link_name)
            #copy_to_tricaster(copy_data_link_name)
            copy_to_sharedFolder(datalink_file_path)

            # export into a DocX (word document)
            docx_file_path = os.path.join(output_folder, f'{docx_base_name}_{timestamp}.docx')
            generate_opendoc(contests, candidates, docx_file_path)
            print_file(docx_file_path)

            logger.info("Processed and exported new data time: " + timestamp)
            print("\n", timestamp, "Updated datalink at ", datalink_file_path)
        else:
            logger.info("No update, back to sleep." + timestamp)
            print("No update, back to sleep.", timestamp)

        # Sleep for a while before checking again
        if not doDownload:
            break  # no need to repeat
        print(f"Sleep for {check_state_interval} seconds ... {check_state_interval/60} minutes")
        time.sleep(check_state_interval)  # Check for updates every N seconds
    print("Finished while Loop")


def main():
    global contest_file_path, candidate_file_path, results_file_path, datalink_file_path
    global state_summary_file_path

    load_config_env()

    datalink_folder = os.getenv("DATALINK_FOLDER")
    print("Main: datalink_folder", datalink_folder)

    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(download_folder, exist_ok=True)
    os.makedirs(datalink_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Construct the file paths
    contest_file_path = os.path.join(data_folder, contest_file_name)
    candidate_file_path = os.path.join(data_folder, candidate_file_name)
    results_file_path = os.path.join(data_folder, results_file_name)
    datalink_file_path = os.path.join(datalink_folder, datalink_file_name)
    state_summary_file_path = os.path.join(data_folder, state_summary_file_name)

    print("Starting runHIStatePrimary - tool to retrieve primary results and forward them to tricaster")
    runHIStatePrimary()

import sys
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s l:%(lineno)d m:%(module)s.py f():%(funcName)s: %(message)s')
    # main()

    try:
        while True:
            main()
            print("Running 2024 HI State Primary Results Tool... Press Ctrl+C to stop.")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt caught. Cleaning up and exiting...")
        # Perform any cleanup here
        sys.exit(0)
