import scraper
from boolean_model import BooleanModel

if __name__ == "__main__":
    url = "https://vnexpress.net/"
    links_count,documents = scraper.scrape_web(url,1)
    print("Number of links scraped: ",links_count)
    model = BooleanModel(documents)
    while(1):
        query = input("Enter query or 'quit()' to quit: ")
        if (query == "quit()"):
            break
        res = model.retrieve(query)
        print("Documents that satisfy query: ",res)
    