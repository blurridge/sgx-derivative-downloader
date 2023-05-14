from pathlib import Path
import datetime as dt
import logging

Path('./logs').mkdir(parents=True, exist_ok=True)

LOGGING_DIR = f'./logs/download_sgx_data-{dt.datetime.today().strftime("%Y%m%d")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(LOGGING_DIR)),
    ]
)

def setup_required_files():
    """
    Sets up index database and log directory
    """
    Path('./db').mkdir(parents=True, exist_ok=True)
    Path('./logs').mkdir(parents=True, exist_ok=True)
    Path('./db/indexes.json').touch(exist_ok=True)
    Path('./db/latest_index.json').touch(exist_ok=True)
    logging.info(f"Index database is ready.")