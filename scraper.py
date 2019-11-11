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
    for ele in soup.find_all():
        text = ele.string
        if (not is_empty(text) and not (ele.name in black_list_tags)):
            if (ele.name in tags_freq):
                tags_freq[ele.name] += 1
            else:
                tags_freq[ele.name] = 1
    return tags_freq

def count_content_classes(soup, classes_freq):
    black_list_tags = ["script","style"]
    for ele in soup.find_all(class_=True):
        text = ele.string
        if (not is_empty(text) and not (ele.name in black_list_tags)):
            for clazz in ele["class"]:
                if (clazz in classes_freq):
                    classes_freq[clazz] += 1
                else:
                    classes_freq[clazz] = 1
    return classes_freq

def sorted_descending(dict_var):
    return sorted(dict_var.items(), key = lambda x : x[1],reverse=True)

def scrape_web(url,max_level):
    print("Scraping: ",url,", max recursive level:",max_level)
    print("This might take a while")
    cur_level = 0
    links = {url}
    visited = set()
    tags_freq = {}
    class_freq = {}
    soups_set = set()
    max_retry = 3

    while (cur_level <= max_level):
        new_links = set()
        for link in links:
            visited.add(link)
            retry = 0
            doc = None
            while(retry < max_retry):
                try:
                    doc = requests.get(link)
                    break
                except:
                    retry +=1
            if (doc is None):
                print("Connection to {link} failed")
                break
            soup = BeautifulSoup(doc.content,"html5lib")
            soups_set.add(soup)
            new_links = get_new_links(soup,new_links,visited)
            tags_freq = count_content_tags(soup,tags_freq)
            class_freq = count_content_classes(soup,class_freq)
        links = new_links
        cur_level = cur_level + 1
    sorted_tags_freq = sorted_descending(tags_freq)
    # sorted_class_freq = sorted_descending(class_freq)
    # print("Sorted tags frequency: ",sorted_tags_freq)
    # print("Sorted classes frequency: ",sorted_class_freq)
    
    top_freq_tag = sorted_tags_freq[0][0]
    i = 0
    file_dir = os.path.dirname(os.path.abspath(__file__))
    documents = {}
    for soup in soups_set:
        
        file_name = f"files/{i}.txt"
        file_path = os.path.join(file_dir,file_name)
        file_path = os.path.abspath(os.path.realpath(file_path))

        f = open(file_path,"w+")
        for ele in soup.find_all(top_freq_tag):
            if not is_empty(ele.string):
                f.write(ele.string.strip()+"\r\n")
                if (i in documents):
                    tmp = documents[i] + ele.string.strip() + "\r\n"
                else:
                    tmp = ele.string.strip() + "\r\n"
                documents[i] = tmp
        f.close() 
        i += 1
    return len(soups_set),documents

if __name__ == "__main__":
    url = "https://vnexpress.net/"
    links_count,documents = scrape_web(url,0)
    print("Number of links scraped: ",links_count)
    for key in documents:
        print(key,documents[key])
