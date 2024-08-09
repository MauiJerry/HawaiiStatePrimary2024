import os
import time
import logging
from candidates import Candidate, list_candidates
from contests import Contest, list_contests
from results import load_results, finalize_results
from datalink import write_datalink
from retrieveStateSummary import check_download_summary
from makeDocx import generate_opendoc
import shutil
from datetime import datetime

check_state_interval = 60 * 5
doDownload = False

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

# Construct the file paths
contest_file_path = os.path.join(data_folder, contest_file_name)
candidate_file_path = os.path.join(data_folder, candidate_file_name)
results_file_path = os.path.join(data_folder, results_file_name)
datalink_file_path = os.path.join(datalink_folder, datalink_file_name)
state_summary_file_path = os.path.join(data_folder, state_summary_file_name)

def print_file(file_path):
    # Get the default printer
    printer_name = win32print.GetDefaultPrinter()
    # Print the file
    print(f"Printing {file_path} on {printer_name}" )
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
    # Load candidates and contests
    candidates = Candidate.from_csv(candidate_file_path)
    logger.debug(f"Candidates loaded: {candidates}")
    list_candidates(candidates)
    contests = Contest.from_csv(contest_file_path)
    logger.debug(f"Contests loaded: {candidates}")

    # Enter an infinite loop to check for updates
    while True:
        # Retrieve the state summary
        if doDownload:
            path = check_download_summary(download_folder)
        else:
            path = state_summary_file_path
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # If a new summary file is retrieved, process it
        if path:
            if doDownload:
                shutil.copy(path, state_summary_file_path)
                logger.info(f"{timestamp} Copied new state summary to {state_summary_file_path}")

            # Load results and update candidates and contests
            load_results(state_summary_file_path, candidates, contests)
            finalize_results(contests, candidates)

            # Export the processed data
            write_datalink(contests, candidates, datalink_file_path)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            copy_data_link_name = os.path.join(output_folder, f'{datalink_file_name}_{timestamp}.csv')
            shutil.copy(datalink_file_path,copy_data_link_name)

            # export into a DocX (word document)
            docx_file_path = os.path.join(output_folder, f'{docx_base_name}_{timestamp}.docx')
            generate_opendoc(contests, candidates, docx_file_path)
            # print_file(docx_file_path)

            logger.info("Processed and exported new data." + timestamp)
            print("\n",timestamp, "Updated datalink at ", datalink_file_path)
        else:
            logger.info("No update, back to sleep." + timestamp)
            print("No update, back to sleep.", timestamp)

        # Sleep for a while before checking again
        if not doDownload:
            break  # no need to repeat
        time.sleep(check_state_interval)  # Check for updates every 60 seconds
    print("Finished while Loop")

def main():
    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(download_folder, exist_ok=True)
    os.makedirs(datalink_folder, exist_ok=True)
    print("Starting runHIStatePrimary - tool to retrieve primary results and forward them to tricaster")
    runHIStatePrimary()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN,
                        format='%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s')
    main()
