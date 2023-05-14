# SGX Derivative Downloader

## Context
Derivative data in SGX is a collection of historical and real-time market data for derivatives contracts traded on the Singapore Exchange. This data can be used by traders, investors, and analysts to make informed decisions about trading derivatives.

There are many reasons why you might want to download derivative data from SGX. For example, you might want to:
- Backtest trading strategies
- Analyze market trends
- Monitor portfolio performance
- Generate reports

Derivative data can be a valuable tool for anyone who wants to gain a deeper understanding of the derivatives markets. By downloading and analyzing this data, you can make more informed decisions about your trading and investment activities.

## Run Locally 
Clone the project

```bash
  git clone https://github.com/blurridge/sgx-derivative-downloader
```

Go to the project directory

```bash
  cd sgx-derivative-downloader
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the script

```bash
  python main.py [-h] [-d DESTINATION] [-c] [-u] [-sd START_DATE] [-ed END_DATE]
```

## Arguments 
```bash
options:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination DESTINATION
                        Relative path where files will be downloaded
  -c, --create_db       Force restart creation of database of date and corresponding record number.
                        This deletes all current data and restarts scraping.
  -u, --update_db       Force update database of date and corresponding record number. Skips existing
                        data and updates missing values.
  -sd START_DATE, --start_date START_DATE
                        Start date (YYYYMMDD) for historical files
  -ed END_DATE, --end_date END_DATE
                        End date (YYYYMMDD) for historical files
```