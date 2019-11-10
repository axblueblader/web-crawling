# CS419 - Infomation Retrieval

Nguyen Quoc Viet - 1651069

## Requirements

- numpy

```
pip3 install numpy
```

## Scraper

File: scraper.py

Usage:

- Run scraper.py or call function **scrape_web** from import

```python
import scraper
url = "https://vnexpress.net/"
links_count,documents = scraper.scrape_web(url,1)
```

Parameter:

- url: link of page to scrape
- level: maximum recursive level to scrape (0 means scrape only current page)

Return:

- links_count: number of links scraped
- documents: a dictionary of documents content

## Boolean Model

File: boolean_model.py

Usage:

- Run boolean_model.py or provide documents from web scraper to initialized and use **retrieve** to get results from query

```python
import scraper
from boolean_model import BooleanModel
url = "https://vnexpress.net/"
links_count,documents = scraper.scrape_web(url,1)
model = BooleanModel(documents)
res = model.retrieve(query)
```
