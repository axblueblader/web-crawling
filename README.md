# CS419 - Infomation Retrieval

# Web crawling and model assignments

Nguyen Quoc Viet - 1651069

## Requirements

- numpy
- python 3

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
- Usable operators: and, or, not

```python
import scraper
from boolean_model import BooleanModel
url = "https://vnexpress.net/"
links_count,documents = scraper.scrape_web(url,1)
model = BooleanModel(documents)
res = model.retrieve(query)
```

- Example query: "việt and nam not mỹ"

## Vector Model

File: vector_model.py

Usage:

- Run vector_model.py or provide documents from web scraper to initialized and use **retrieve** to get results ranking from query
- Input: list of keywords seperated by space

```python
import scraper
from vector_model import VectorModel
url = "https://vnexpress.net/"
links_count,documents = scraper.scrape_web(url,1)
model = VectorModel(documents)
res = model.retrieve(query)
```

- Example query: "việt nam"

## All together

- Run main.py to run everything together. By default, it will scrape https://vnexpress.net/ , with recursive level 1, store all contents in the most frequently use HTML tag on a page as one document. User can then input queries, and results from both Boolean Model and Vector Model will be shown.
