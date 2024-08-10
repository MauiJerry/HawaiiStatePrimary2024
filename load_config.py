import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

def load_config_env():
    logger.debug(f"Loading configuration from config.env: ")

    load_dotenv(dotenv_path='config.env')

    # these are here as examples. usages should be to define and use local method variables
    # with these as templates
    wait_for_real_data = os.getenv("WAIT_FOR_REAL")
    if wait_for_real_data == "TRUE":
        wait_for_real_data = True
    else:
        wait_for_real_data = False

    actually_print = os.getenv("ACTUALLY_PRINT")
    if actually_print == "TRUE":
        actually_print = True
    else:
        actually_print = False

    summary_url = os.getenv("SUMMARY_URL")
    username = os.getenv("HI_USERNAME")
    password = os.getenv("HI_PASSWORD")
    datalink_folder = os.getenv("DATALINK_FOLDER")

    logger.debug(f"Loaded Username: {username}, Password: {password}, _pauseUntilReal{wait_for_real_data}")
    logger.debug(f"datalink folder {datalink_folder}")
    logger.debug(f"Summary URL {summary_url}")
