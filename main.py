import logging
import datetime as dt
import argparse
import configparser
from pathlib import Path
from setup import *
from database_util import *
from download_util import *

LOGGING_DIR = f'./logs/download_sgx_data-{dt.datetime.today().strftime("%Y%m%d")}.log'

setup_required_files()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(LOGGING_DIR)),
    ]
)

def valid_date(s):
    """
    Checks if date is validly formatted
    """
    try:
        return dt.datetime.strptime(s, "%Y%m%d").date()
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)

def main():
    parser = argparse.ArgumentParser(prog="SGX Webscraping Job", 
                                     description="Downloads SGX time and sales historical data in different formats.",
                                     epilog="Script made by Zach Riane I. Machacon"
                                     )
    parser.add_argument("-d", "--destination", default=Path('./downloaded'), help="Relative path where files will be downloaded")
    parser.add_argument("-c", "--create_db", 
                        help="Force restart creation of database of date and corresponding record number. This deletes all current data and restarts scraping.", 
                        action="store_true")
    parser.add_argument("-u", "--update_db", 
                        help="Force update database of date and corresponding record number. Skips existing data and updates missing values.", 
                        action="store_true")
    parser.add_argument("-sd", "--start_date", default=dt.datetime.today().date(), type=valid_date, help="Start date (YYYYMMDD) for historical files")
    parser.add_argument("-ed", "--end_date", default=dt.datetime.today().date(), type=valid_date, help="End date (YYYYMMDD) for historical files")
    parser.add_argument("-cfg", "--config_file", metavar="FILE", help="Config file for setting path download")
    args = parser.parse_args()
    latest_index = update_current_date()
    if args.config_file:
        config = configparser.ConfigParser()
        config.read(args.config_file)
        job = {}
        job.update(dict(config.items("job")))
        job['create_db'] = False if (job['create_db'] == 'False' or job['create_db'] == 'false') else True
        job['update_db'] = False if (job['update_db'] == 'False' or job['update_db'] == 'false') else True
        parser.set_defaults(**job)
        args = parser.parse_args()
    if args.create_db:
        create_database(latest_index)
    if args.update_db:
        update_database(latest_index)
    if args.end_date < args.start_date:
        logging.error("Invalid date range. End date is earlier than start date.")
        return
    Path(args.destination).mkdir(parents=True, exist_ok=True)
    download_files(args.start_date, args.end_date, args.destination)

if __name__ == '__main__':
    main()