
from bs4 import BeautifulSoup
import requests
import pandas as pd
from unidecode import  unidecode
from urllib.parse import unquote

def get_links(url):
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

def explore_index_page(url):
    """Parses an index page to return all linked pages"""
    dict = {}
    generator = get_links(url)
    for scrapped_url, scrapped_name in generator:
        dict[scrapped_url] = unidecode(unquote(scrapped_name))
    return dict

def get_pairs(urls):
    """Scrap urls and populate a list of tuples if there is a link between characters"""
    pairs = []
    for url in urls:
        gen = get_links(url)
        for scrapped_url,_ in gen:
            # only add pairs to known character pages
            if scrapped_url in urls:
                a = pages[url]
                b = pages[scrapped_url]
                # only add pairs that aren't already in
                if (a,b) not in pairs and (b,a) not in pairs:
                    pairs.append((a, b))
                    print(f'new link: {a},{b}')
    return pairs

def gen_csv_nodes(dicts):
    """Writes nodes on CSV file""" 
    dict_nodes = {'id':[],'url':[],'type':[]}
    for (dict,typ) in dicts:
        for url,id in dict.items():
            dict_nodes['id'].append(id)
            dict_nodes['url'].append(url)
            dict_nodes['type'].append(typ)
    df_node = pd.DataFrame(data=dict_nodes)
    df_node.to_csv("nodes.csv", sep = ",", index=False)

def gen_csv_links(pairs):
    """Writes page links on CSV file""" 
    dict_links = {'source':[],'target':[]}
    for pair in pairs:
        dict_links['source'].append(pair[0])
        dict_links['target'].append(pair[1])
    df_link = pd.DataFrame(data=dict_links)
    df_link.to_csv("links.csv", sep = ",", index=False)

if __name__ == '__main__':
    # for npcs and divine characters, parse the available index pages
    pnjs = explore_index_page('https://amour-gloire-et-dragons.fandom.com/fr/wiki/PNJs')
    divins = explore_index_page('https://amour-gloire-et-dragons.fandom.com/fr/wiki/Les_divinit%C3%A9s')
    # for pcs, construct the dictionary manually
    pjs = {
        'https://amour-gloire-et-dragons.fandom.com/fr/wiki/Jean-Philippe_Lapage': 'Jean-Philippe_Lapage',
        'https://amour-gloire-et-dragons.fandom.com/fr/wiki/Juliette_Binocle': 'Juliette_Binocle',
        'https://amour-gloire-et-dragons.fandom.com/fr/wiki/Laura_Crochet': 'Laura_Crochet',
        'https://amour-gloire-et-dragons.fandom.com/fr/wiki/William_Gentil': 'William_Gentil',
        'https://amour-gloire-et-dragons.fandom.com/fr/wiki/Waghaghanha': 'Waghaghanha',
        'https://amour-gloire-et-dragons.fandom.com/fr/wiki/Glycydya': 'Glycydya',
        'https://amour-gloire-et-dragons.fandom.com/fr/wiki/Dr_Mhou': 'Dr_Mhou',
        'https://amour-gloire-et-dragons.fandom.com/fr/wiki/Aangus_von_Chemin': 'Aangus_von_Chemin',
        'https://amour-gloire-et-dragons.fandom.com/fr/wiki/Elson_de_l%27Huntz': 'Elson_de_l\'Huntz',
        'https://amour-gloire-et-dragons.fandom.com/fr/wiki/Violette': 'Violette'
    }
    # concatenate the dictionaries
    pages = dict(pjs)
    pages.update(pnjs)
    pages.update(divins)
    # get pairs
    pairs = get_pairs(list(pages.keys()))
    # write data
    gen_csv_nodes([(pjs,"PJ"),(pnjs,"PNJ"),(divins,"divin")])
    gen_csv_links(pairs)
