# results.py

import csv
import logging
from candidates import update_candidate_from_row
from contests import update_contest_from_row

# Configure logging
#logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

def load_results(file_path, candidates, contests):
    """Load results from a CSV file and update candidates and contests."""
    num_updated = 0
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        # print(f"headers are: {csv_reader.fieldnames}")

        try:
            #results_df = pd.read_csv(file_path)
            logger.info(f"Loading results from {file_path}")
            # for index, row in results_df.iterrows():
            index = 0
            for row in csv_reader:
                #print(f"row {index}= {row}")
                contest_id = str(row['#Contest ID'])
                candidate_id = str(row['Candidate ID'])

                if contest_id in contests:
                    logger.debug(f"loading row {index} with id {contest_id} is \n{row}")
                    candidate_index = f"{contest_id} {candidate_id}"
                    if candidate_index in candidates:
                        num_updated += 1
                        candidate = candidates[candidate_index]
                        logger.debug(f"update with candidate {candidate.candidate_name}")
                        update_candidate_from_row(candidate, row)
                        update_contest_from_row(contests[row['#Contest ID']], row)
                    else:
                        logger.warning(f'unexpected candidate: {candidate_index}')
                        raise ValueError(f"Unexpected candidate: {candidate_index}")
                else:
                    #logger.warning(f"contest {contest_id} not found in contests")
                    pass
                index += 1
            if num_updated < 1:
                logger.error("NO CANDIDATES UPDATED!")
                raise ValueError("No Candidates Updated")
            logger.info(f"updated {num_updated} candidates")
        except Exception as e:
            logger.error(f"Error loading results: {e}")
            raise

def finalize_results(contests, candidates):
    """Finalize the results by calculating total and percentage votes for each candidate"""
    for contest_id, contest in contests.items():
        total_votes = 0
        for candidate in candidates.values():
            if candidate.contest_id == contest_id:
                total_votes += int(candidate.total_votes)
        contest.bad_boi = contest.blank + contest.over + contest.invalid
        contest.total_votes = total_votes + contest.bad_boi
        contest.percent_bad_boi = round((contest.bad_boi / contest.total_votes) * 100 if contest.total_votes > 0 else 0,1)

        # also need to add totals of contest. blank over and invalid
        for candidate in candidates.values():
            # select only those candidates in this contest
            if candidate.contest_id == contest_id:
                candidate.percent_votes = (candidate.total_votes / contest.total_votes) * 100 if contest.total_votes > 0 else 0
                candidate.percent_votes = round(candidate.percent_votes,1)
