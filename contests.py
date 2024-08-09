import csv
import logging

# Configure logging
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

class Contest:
    def __init__(self, contest_id, contest_seq_nbr, contest_title, contest_party, num_candidates, datalink_id, datalink_value,
                 total_votes=0, blank=0, over=0, invalid=0):
        self.contest_id = contest_id
        self.contest_seq_nbr = contest_seq_nbr
        self.contest_title = contest_title
        self.contest_party = contest_party
        self.num_candidates = num_candidates
        self.datalink_id = datalink_id
        self.datalink_value = datalink_value
        self.total_votes = total_votes
        self.blank = blank
        self.over = over
        self.invalid = invalid
        self.bad_boi = 0
        self.percent_bad_boi = ""

    def __repr__(self):
        return (f"Contest(contest_id={self.contest_id}, contest_seq_nbr={self.contest_seq_nbr}, contest_title={self.contest_title}, "
                f"contest_party={self.contest_party}, num_candidates={self.num_candidates}, datalink_id={self.datalink_id}, "
                f"datalink_value={self.datalink_value}, total_votes={self.total_votes}, blank={self.blank}, over={self.over}, invalid={self.invalid})")

    @classmethod
    def from_csv(cls, file_path):
        contests = {}
        count =0
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contest = cls(
                    contest_id=str(row['#Contest ID']),
                    contest_seq_nbr=row['Contest Seq Nbr'],
                    contest_title=row['Contest Title'],
                    contest_party=row['Contest Party'],
                    num_candidates=row['numCandidates'],
                    datalink_id=row['DataLinkID'],
                    datalink_value=row['DatalinkValue'],
                )
                if isinstance(contest.contest_id, int):
                    raise ValueError("Contest Id should be a string, not an int")

                contests[contest.contest_id] = contest
                #logger.debug(f"loaded contest: {contest}")
                count += 1
        print(f"Loaded {count} contests {len(contests)}")
        return contests


update_these_keys = ['Mail Blank Votes','In-Person Blank Votes',
                     'Mail Over Votes', 'In-Person Over Votes',
                     'Mail Invalid Votes','In-Person Invalid Votes']

def update_contest_from_row(contest, data):
    logger.debug(f"update contest {contest.contest_title} orig  blank { contest.blank} over { contest.over} invalid { contest.invalid}")
    contest.blank = int(data['Mail Blank Votes']) + int(data['In-Person Blank Votes'])
    contest.over = int(data['Mail Over Votes']) + int(data['In-Person Over Votes'])
    contest.invalid = int(data['Mail Invalid Votes']) + int(data['In-Person Invalid Votes'])
    logger.debug(f"Updated contest {contest.contest_id} with: blank { contest.blank} over { contest.over} invalid { contest.invalid}")

def list_contests(contests):
    print("Contests has ", len(contests), "contests")
    logger.debug(f"Candidates loaded: {contests}")