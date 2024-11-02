import csv
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class FederalContests:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"FederalContests({self.data})"

    @classmethod
    def from_csv(cls, file_path):
        data = {}

        try:
            with open(file_path, mode='r', newline='') as csvfile:
                # Using comma as a delimiter based on provided example
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    # Skip rows that contain only empty or whitespace cells
                    if all(cell.strip() == '' for cell in row):
                        logger.debug("Skipping blank row")
                        continue

                    # Log each row read for diagnosis
                    logger.debug(f"Reading row: {row}")

                    # Process each key-value pair in the row
                    # We assume here that each pair might be separated by a comma, so we check in pairs
                    for i in range(0, len(row), 2):
                        if i + 1 < len(row):  # Ensure there is a value for each key
                            key = row[i].replace('-', '_').strip()  # Convert hyphens to underscores and strip whitespace
                            value = row[i + 1].strip()  # Strip whitespace from the value

                            # Ensure that both key and value are non-empty
                            if key and value:
                                # Format values: convert to integer or float if applicable
                                if value.isdigit():
                                    value = int(value)
                                else:
                                    try:
                                        value = float(value)
                                    except ValueError:
                                        pass  # Keep as string if it cannot be converted

                                # Add to data dictionary
                                data[key] = value
                                logger.debug(f"Added to data: {key} = {value}")
                            else:
                                logger.debug(f"Skipping empty key or value: key='{key}', value='{value}'")

            # Final log of the data dictionary to confirm results
            logger.info(f"Successfully loaded FederalContests data from {file_path}")
            logger.debug(f"Final data dictionary after processing all rows: {data}")
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}")
            raise

        # Create an instance using the populated data dictionary
        federal_results = cls(data)
        logger.debug(f"Federal Results: {federal_results.data}")
        return federal_results
