from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import os

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

def validate_link(val,rules):
    for rule in rules:
        if (not rule(val)):
            return False
    return True

def check_duplicate(href,new_links,visited):
    return any(href in x for x in (new_links,visited))

def remove_hash_from_url(href):
    return href.split("#")[0]

def get_new_links(soup,new_links,visited):
    for new_link in soup.find_all('a'):
        href = new_link.get('href')
        if(not is_url(href)):
            continue
        href = remove_hash_from_url(href)
        if (check_duplicate(href,new_links,visited)):
            continue
        # print("Added link:",href)
        new_links.add(href)
    return new_links

def is_empty(string):
    return not (string and string.strip())

def count_content_tags(soup,tags_freq):
    black_list_tags = ["script","style"]
    for tag in soup.find_all():
        text = tag.string
        if (not is_empty(text) and not (tag.name in black_list_tags)):
            if (tag.name in tags_freq):
                tags_freq[tag.name] += 1
            else:
                tags_freq[tag.name] = 1
    return tags_freq

def sorted_tags_descending(tags_freq):
    return sorted(tags_freq.items(), key = lambda x : x[1],reverse=True)

def scrape_web(url,max_level):
    print("Scraping: ",url,", max recursive level:",max_level)
    cur_level = 1
    links = {url}
    visited = set()
    tags_freq = {}
    soups_set = set()

    while (cur_level < max_level+1):
        new_links = set()
        for link in links:
            visited.add(link)
            doc = requests.get(link)
            soup = BeautifulSoup(doc.content,"html5lib")
            soups_set.add(soup)
            new_links = get_new_links(soup,new_links,visited)
            tags_freq = count_content_tags(soup,tags_freq)
        links = new_links
        cur_level = cur_level + 1
    sorted_tags_freq = sorted_tags_descending(tags_freq)
    print(sorted_tags_freq)
    
    top_freq_tag = sorted_tags_freq[0][0]
    i = 0
    file_dir = os.path.dirname(os.path.abspath(__file__))
    for soup in soups_set:
        file_name = f"files/{i}.txt"
        file_path = os.path.join(file_dir,file_name)
        f = open(file_path,"w+")
        for ele in soup.find_all(top_freq_tag):
            if not is_empty(ele.string):
                f.write(ele.string.strip()+"\r\n")
        f.close() 
        i += 1
    return len(soups_set)

if __name__ == "__main__":
    url = "https://vnexpress.net/"
    links_count = scrape_web(url,1)
    print("Number of links scraped: ",links_count)
