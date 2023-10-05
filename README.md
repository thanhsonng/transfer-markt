# Scrape Club Statistics on Transfer Markt

## Installation

Clone this repo.

```bash
git clone git@github.com:thanhsonng/transfer-markt.git

cd transfer-markt
```

Set up Python virtual environment.

```bash
python3 -m venv venv

source venv/bin/activate

# When you need to deactivate virtual environment later
deactivate
```

Install dependencies.

```bash
pip install
```

## Usage

Run Scrapy spider.

```bash
scrapy runspider scrape.py
```

Output CSV files are available at `./output/laliga/*`.
