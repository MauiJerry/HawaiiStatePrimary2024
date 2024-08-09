import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# Define the data folder and file names
data_folder = "./data"
contest_file_name = "ContestKey.csv"
candidate_file_name = "CandidateKey.csv"

# Construct the file paths
contest_file_path = os.path.join(data_folder, contest_file_name)
candidate_file_path = os.path.join(data_folder, candidate_file_name)


# Define the Candidate class with all members from the CSV
class Candidate:
    required_fields = ['#Contest ID', 'Candidate ID', 'Candidate Name', 'DataLinkID', 'DataLinkValue', 'Contest Title',
                       'Contest Party', 'Mail Votes', 'In-Person Votes', 'Total Votes', 'Contest Seq Nbr',
                       'Contest Party']

    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"Candidate({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

    @classmethod
    def load_candidates_from(cls, file_path):
        logging.debug(f"Loading candidates from {file_path}")
        try:
            df = pd.read_csv(file_path)
            list_as_string = ', '.join(df.columns.tolist())
            logging.debug("DataFrame has columns %s", list_as_string)
            check_required_headers(df, cls.required_fields)
            logging.debug("passed required headers")
            candidate_dict = {}
            for index, row in df.iterrows():
                candidate_data = row.to_dict()
                print("Candidate Data", candidate_data)
                for field in cls.required_fields:
                    if field not in candidate_data:
                        candidate_data[field] = 0
                candidate = cls(**candidate_data)
                candidate_index = f"{row['#Contest ID']} {row['Candidate ID']}"
                candidate_dict[candidate_index] = candidate
            print("Loaded candidate dictionary", candidate_data)
            cls.check_required_fields(candidate_dict)
            return candidate_dict
        except Exception as e:
            logging.error(f"Error loading candidates: {e}")
            raise

    @staticmethod
    def check_required_fields(candidate_dict):
        logging.debug("Check Candidate Required Fields", candidate_dict)
        for candidate_id, candidate in candidate_dict.items():
            missing_fields = [field for field in Candidate.required_fields if not hasattr(candidate, field)]
            if missing_fields:
                logging.warning(f"Candidate {candidate_id} is missing required fields: {', '.join(missing_fields)}")
                #raise ValueError(f"Candidate {candidate_id} is missing required fields: {', '.join(missing_fields)}")


# Function to check for required headers
def check_required_headers(df, required_headers):
    loaded_headers = df.columns.tolist()
    list_as_string = ', '.join(required_headers)
    logging.debug(f"Check Required Headers: {list_as_string}")
    missing_headers = [header for header in required_headers if header not in loaded_headers]
    logging.debug(f"Loaded headers: {', '.join(loaded_headers)}")
    if missing_headers:
        logging.error(f"Missing required headers: {', '.join(missing_headers)}")
        print("missed some headers")
        raise ValueError(f"Missing required headers: {', '.join(missing_headers)}")
    else:
        logging.debug("No missing headers")

# Example usage
try:
    logging.debug("try loading candidate file: %s ",candidate_file_path)
    candidate_dict = Candidate.load_candidates_from(candidate_file_path)
    print("Candidates Dictionary:")
    for candidate_id, candidate in candidate_dict.items():
        print(candidate_id, candidate)
except Exception as e:
    print(f"Error loading candidate file : {e}")
