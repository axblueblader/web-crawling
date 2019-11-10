import scraper
from boolean_model import BooleanModel
from vector_model import VectorModel

if __name__ == "__main__":
    url = "https://vnexpress.net/"
    links_count,documents = scraper.scrape_web(url,1)
    print("Number of links scraped: ",links_count)
    bool_model = BooleanModel(documents)
    vect_model = VectorModel(documents)
    while(1):
        query = input("Enter query or 'quit()' to quit: ")
        if (query == "quit()"):
            break
        res = bool_model.retrieve(query)
        print("Documents that satisfy query from Boolean Model: ",res)
        res = vect_model.retrieve(query)
        print("Documents scores from Vector Model: ",res)

    