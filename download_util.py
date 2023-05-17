from pathlib import Path
import datetime as dt
import json 
import logging
import requests

URL_PREFIX = "https://links.sgx.com/1.0.0/derivatives-historical/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
DATABASE_PATH = './db/indexes.json'
FILES = ['WEBPXTICK_DT.zip', 'TickData_structure.dat', 'TC.txt', 'TC_structure.dat']
LOGGING_DIR = f'./logs/download_sgx_data-{dt.datetime.today().strftime("%Y%m%d")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(LOGGING_DIR)),
    ]
)

def get_file_path_name(current_path, file_name, current_date):
    """
    Gets file path for file to be downloaded
    """
    if file_name == "WEBPXTICK_DT.zip":
        file_name = f'WEBPXTICK_DT-{current_date.strftime("%Y%m%d")}.zip'
    elif file_name == "TC.txt":
        file_name = f'TC_{current_date.strftime("%Y%m%d")}.txt'
    return [f'{current_path}/{file_name}', file_name]

def download_files(start_date, end_date, destination):
    """
    Downloads SGX derivative data files for a range of dates
    """
    index_data = {}
    if Path(DATABASE_PATH).exists():
        with open(DATABASE_PATH, 'r') as db:
            index_data = json.loads(db.read())
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 5 or current_date.weekday() == 6 or current_date.strftime("%Y%m%d") not in index_data.keys():
            logging.error(f'No file exists for {current_date.strftime("%Y%m%d")}')
            current_date += dt.timedelta(1)
            continue
        current_path = f'{destination}/{current_date}'
        Path(current_path).mkdir(parents=True, exist_ok=True)
        for current_file in FILES:
            file_name = current_file
            file_path, file_name = get_file_path_name(current_path, file_name, current_date)
            if Path(file_path).exists():
                logging.info(f'{file_name} already exists. Skipping...')
            else:
                url = f'{URL_PREFIX}{index_data[current_date.strftime("%Y%m%d")]}/{current_file}'
                try:
                    r = requests.get(url, headers=HEADERS, timeout=10)
                    with open(file_path, 'wb') as f:
                        f.write(r.content)
                    logging.info(f'Successfully downloaded {file_name}')
                except requests.exceptions.ConnectTimeout:
                    logging.error(f'Request timed out. Failed to download {file_name}')
                except requests.exceptions.ConnectionError:
                    logging.error(f'Lost connection SGX. Failed to download {file_name}')
                except Exception:
                    logging.error(f'Failed to download {file_name}')
        current_date += dt.timedelta(1)