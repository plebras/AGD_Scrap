
from bs4 import BeautifulSoup
import requests
import pandas as pd
from unidecode import  unidecode
from urllib.parse import unquote

def get_link(url):
    """Generator used to get the link contained on one page"""
    #request the url
    r = requests.get(url)
    #create the soup
    soup = BeautifulSoup(r.content, 'html.parser')
    #take the div content
    mydivs = soup.find_all("div", {"id": "content"})

    #loop on all a to create a generator
    for a in mydivs[0].find_all("a"):
        link = str(a.get("href"))
        split = link.split('/')
        if (len(split) == 4) and split[0] == "":
            name = split[3]
            if '?' not in name:
                yield f"https://amour-gloire-et-dragons.fandom.com{link}", name


def scrap(first_url, first_title):
    """Main scrap function
        Start from a given page, scrap the links and call them
    """
    dict_link_to_name = {first_url : first_title}
    file_to_scrap = [first_url]
    list_pairs = []

    total = 0

    while len(file_to_scrap) != 0 and total < 200:
        current_url = file_to_scrap.pop(0)
        generator = get_link(current_url)
        for scrapped_url, scrapped_name in generator:
            list_pairs.append((current_url, scrapped_url))
            print("added pair : ")
            print((current_url, scrapped_url))

            #if not visited yet, we will visit it later
            if scrapped_url not in dict_link_to_name:
                file_to_scrap.append(scrapped_url)
                dict_link_to_name[scrapped_url] = scrapped_name

        total = total + 1

    return dict_link_to_name, list_pairs

def gen_csv(dict_link_name, pairs):

    dict_pair = {"Source" : [], "Target" : [], "Weight" : []}
    for pair in pairs :
        dict_pair["Source"].append(unidecode(unquote(dict_link_name[pair[0]])))
        dict_pair["Target"].append(unidecode(unquote(dict_link_name[pair[1]])))
        dict_pair["Weight"].append(1)

    dict_nodes = {"id" : [], "label" : []}
    for name in dict_link_name.values():
        dict_nodes["id"].append(unidecode(unquote(name)))
        dict_nodes["label"].append(unidecode(unquote(name)))


    df_nodes = pd.DataFrame(data = dict_nodes)
    df_pairs = pd.DataFrame(data = dict_pair)

    df_pairs.to_csv("pairs.csv", sep = ";", index=False)
    df_nodes.to_csv("nodes.csv", sep = ";", index=False)

if __name__ == '__main__':
    dict, pairs = scrap("https://amour-gloire-et-dragons.fandom.com/fr/wiki/Jean-Philippe_Lapage", "Jean-Philippe_Lapage")
    gen_csv(dict, pairs)
