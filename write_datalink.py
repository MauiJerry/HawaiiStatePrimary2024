import csv
import logging
from candidates import Candidate
from contests import Contest

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def write_datalink(contests, candidates, datalink_filepath):
    try:
        with open(datalink_filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the headers
            writer.writerow(["DataLinkID", "DataLinkValue"])
            writer.writerow(["DataLinkID", "Value"])

            for contest_id, contest in contests.items():
                # Write contest DataLink fields
                writer.writerow([contest.DataLinkID, contest.DatalinkValue])

                # Write blank and over fields
                blank_over_count = contest.blank + contest.over
                blank_over_pct = (blank_over_count / contest.TotalVotes) * 100 if contest.TotalVotes > 0 else 0
                writer.writerow([f"{contest.DataLinkID}-blankover-COUNT", blank_over_count])
                writer.writerow([f"{contest.DataLinkID}-blankover-PCT", blank_over_pct])

                for candidate_id, candidate in candidates.items():
                    if candidate.contest_id == contest_id:
                        # Write candidate DataLink fields
                        candidate_fields = [
                            candidate.DataLinkID,
                            candidate.DataLinkValue,
                            f"{candidate.DataLinkID}-Votes",
                            candidate.TotalVotes,
                            f"{candidate.DataLinkID}-Pct",
                            candidate.PercentVotes
                        ]
                        writer.writerow(candidate_fields)
        logging.info(f"DataLink file written to {datalink_filepath}")
    except Exception as e:
        logging.error(f"Error writing DataLink file: {e}")
        raise
