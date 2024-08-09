import csv
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

def reformat_name(name):
    # Split the name by comma
    parts = name.split(',')

    # Remove leading/trailing whitespaces from parts
    last_name = parts[0].strip()
    first_middle_name = parts[1].strip()

    # Combine the names in the desired format
    formatted_name = f"{first_middle_name} {last_name}"

    return formatted_name


class Candidate:
    def __init__(self, contest_id, candidate_id, candidate_name, datalink_id, datalink_value, contest_title,
                 contest_party,
                 mail_votes=0, in_person_votes=0, total_votes=0, percent_votes=0):
        self.contest_id = str(contest_id)
        self.candidate_id = str(candidate_id)
        self.candidate_name = candidate_name
        self.datalink_id = datalink_id
        self.datalink_value = datalink_value
        self.contest_title = contest_title
        self.contest_party = contest_party
        self.mail_votes = mail_votes
        self.in_person_votes = in_person_votes
        self.total_votes = total_votes
        self.percent_votes = percent_votes
        self.index = f"{contest_id} {candidate_id}"

    def __repr__(self):
        return (
            f"Candidate(contest_id={self.contest_id}, candidate_id={self.candidate_id}, candidate_name={self.candidate_name}, "
            f"datalink_id={self.datalink_id}, datalink_value={self.datalink_value}, contest_title={self.contest_title}, "
            f"contest_party={self.contest_party}, mail_votes={self.mail_votes}, in_person_votes={self.in_person_votes}, "
            f"total_votes={self.total_votes}, percent_votes={self.percent_votes}) index='{self.index}'")

    @classmethod
    def from_csv(cls, file_path):
        logger.info(f"Loading candidates from {file_path}")
        candidates = {}
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                candidate = cls(
                    contest_id=str(row['#Contest ID']),
                    candidate_id=str(row['Candidate ID']),
                    candidate_name=row['Candidate Name'],
                    datalink_id=row['DataLinkID'],
                    datalink_value=row['DataLinkValue'],
                    contest_title=row['Contest Title'],
                    contest_party=row['Contest Party'],
                    mail_votes=row.get('Mail Votes', 0),
                    in_person_votes=row.get('In-Person Votes', 0),
                    total_votes=row.get('Total Votes', 0),
                    percent_votes=row.get('Percent Votes', 0)
                )
                if candidate.datalink_value == "use name" or candidate.datalink_value is None:
                    candidate.datalink_value = reformat_name(candidate.candidate_name)
                candidates[candidate.index] = candidate
                # logger.debug(f"create candidate idx ({candidate.index})with {candidate}")
                if not candidate.index in candidates:
                    raise ValueError(f"Candidate not added properly {candidate.index}")

        return candidates


update_these_keys = ['Mail Votes', 'In-Person Votes', 'Total Votes']


def update_candidate_from_row(candidate, data):
    candidate.mail_votes = int(data["Mail Votes"])
    candidate.in_person_votes = int(data["In-Person Votes"])
    candidate.total_votes = int(data["Total Votes"])
    logging.debug(
        f"Updated candidate {candidate.index} {candidate.candidate_name} as {candidate.datalink_value} with {candidate.mail_votes}, {candidate.in_person_votes}, {candidate.total_votes} ")


def list_candidates(candidates):
    print("Candidates has ", len(candidates), "candidates")
    logger.debug(f"Candidates loaded: {candidates}")
    for index, (key, candidate) in enumerate(candidates.items()):
        print(f"Index {index} key({key}): {candidate}")
        c = candidates[key]
        if c:
            print(f"look up using ({key}) found it as {c.candidate_name}")
        else:
            print(f"Failed to find {key}")
