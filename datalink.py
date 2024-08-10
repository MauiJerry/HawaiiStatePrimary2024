# export_datalink.py

import csv
import logging
import math
from candidates import Candidate
from contests import Contest

# Configure logging
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

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
