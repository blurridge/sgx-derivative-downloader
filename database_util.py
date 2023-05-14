from pathlib import Path
import json
import logging
import requests
import re
import datetime as dt

DATABASE_PATH = './db/indexes.json'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
URL_PREFIX = "https://links.sgx.com/1.0.0/derivatives-historical/"
LOGGING_DIR = f'./logs/download_sgx_data-{dt.datetime.today().strftime("%Y%m%d")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(LOGGING_DIR)),
    ]
)

def create_database(latest_index):
    """
    Exports to a .json file the date and its corresponding index. This redoes the entire index scraping process
    for any major changes to the website. Only use when no database is available or if there are major differences.
    """
    database = {}
    bad_indices = []
    for index in range(2755, latest_index + 1):
        current_date = get_date(index)
        if current_date:
            database[current_date] = index
        else:
            bad_indices.append(index)
        with open(DATABASE_PATH, 'w+') as f:
            json.dump(database, f)

def update_database(latest_index):
    """
    Exports an updated .json file of the date and its corresponding index. Similar to create_database except that 
    it skips indices that already exist. 
    """
    database = {}
    bad_indices = []
    if Path(DATABASE_PATH).exists():
        with open(DATABASE_PATH, 'r') as db:
            database = json.loads(db.read())
    for index in range(2755, latest_index + 1):
        if any(database[date] == index for date in database):
            logging.info(f"{index}'s date is already in the database. Skipping...")
            continue
        current_date = get_date(index)
        if current_date:
            database[current_date] = index
        else:
            bad_indices.append(index)
        with open(DATABASE_PATH, 'w+') as f:
            json.dump(database, f)

def get_date(index):
    """
    Gets the date of the file corresponding to the given index
    """
    url = f'{URL_PREFIX}{index}/WEBPXTICK_DT.zip'
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        cd = r.headers['content-disposition']
        date = re.search(r"(?<=DT-)\d{8}", cd).group(0)
        logging.info(f'Added {index} {date} date to database.')
        return date
    except requests.exceptions.ConnectTimeout:
        logging.error(f'Request timed out. Failed to scrape {index} date.')
    except requests.exceptions.ConnectionError:
        logging.error(f'Lost connection SGX. Failed to scrape {index} date.')
    except Exception:
        logging.error(f'Failed to scrape {index} date.')
    return None

def update_current_date():
    """
    Updates the latest_index.json file to contain the latest index based on current date
    """
    previous_latest = None
    current_date = dt.datetime.today().date()
    if Path(DATABASE_PATH).exists():
        database = {}
        with open(DATABASE_PATH, 'r') as db:
            database = json.loads(db.read())
        previous_latest = database[list(database.keys())[-1]]
    if current_date.weekday() == 5 or current_date.weekday() == 6:
        latest_index = {current_date.strftime('%Y%m%d'):previous_latest}
    else:
        latest_index = {current_date.strftime('%Y%m%d'):previous_latest + 1}
    with open('./db/latest_index.json', 'w+') as f:
        json.dump(latest_index, f)
    logging.info("Updating current latest index based on date...")
    return latest_index[current_date.strftime('%Y%m%d')]