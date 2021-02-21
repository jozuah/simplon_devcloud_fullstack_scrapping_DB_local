# import libraries
from bs4 import BeautifulSoup
#Permet de faire d'établir des connexions avec les pages web
import urllib.request

import logging

#sert à faire des list dans des value de dict
from collections import defaultdict

#necessaire au fonctionnement du beautifulsoup
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(filename='my_log.txt', encoding='utf-8', level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def request_JV_website (my_url):
    try:
        try:
            # stockage de la page de top
            page = urllib.request.urlopen(my_url)
            logging.info("[SCRAPPING] Request has been successfully achieve from %s" , (my_url)) 
        except:
            logging.warning("[SCRAPPING] Cant't acces to %s", (my_url))  
            return
        # parse the html using beautiful soup and store in variable 'soup'
        soup = BeautifulSoup(page, 'html.parser')

        #print(soup) affiche toute la page

        # find results h2 sur JV avec la class="gameTitle__3PBZI1", <h2 class="gameTitle__3PBZI1" data-reactid="363"><a href="/jeux/ps5/jeu-1219075/" class="gameTitleLink__196nPy" data-reactid="364"><!-- react-text: 365 -->Assassin's Creed Valhalla<!-- /react-text --><em data-reactid="366"> sur PS5</em></a></h2>
        title_game = soup.find_all('a',attrs={'class': 'gameTitleLink__196nPy'})

        #je créé un dict pour récupérer mes données
        dict_jv = {}
        for i in range (0,10):
            title_string = title_game[i].text
            #concatenation de la string de titre pour enlever "sur ..."
            title_string = title_string[0:-7]
            title_string = title_string.replace("'"," ")
            #j'ajoute les éléments dans mon dict
            dict_jv.update({i+1:title_string})
        logging.info("[SCRAPPING] Data has been successfully put in a dict from %s" , (my_url))    
        return dict_jv
    except:
        logging.warning("[SCRAPPING] Fail to put data in a dict from %s", (my_url))  
        

url_ign_ps5 = 'https://www.ign.com/articles/the-best-ps5-games'
url_ign_xbox = 'https://www.ign.com/articles/best-xbox-series-x-games'
url_ign_pc = 'https://www.ign.com/articles/best-pc-games'

def request_IGN_website (my_url):

    # stockage de la page de top
    page = urllib.request.urlopen(my_url)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')


    #print(soup) affiche toute la page

    # find results h2 sur JV avec la class="gameTitle__3PBZI1", <h2 class="gameTitle__3PBZI1" data-reactid="363"><a href="/jeux/ps5/jeu-1219075/" class="gameTitleLink__196nPy" data-reactid="364"><!-- react-text: 365 -->Assassin's Creed Valhalla<!-- /react-text --><em data-reactid="366"> sur PS5</em></a></h2>
    title_game = soup.find_all('h2')

    #je créé un dict pour récupérer mes données
    dict_jv = {}
    rank = 1
    for i in range (len(title_game)-3,len(title_game)-13,-1):
        
        title_string = title_game[i].text
        title_string = title_string[3:]
        #concatenation de la string de titre pour enlever "sur PS5"
        title_string = title_string.replace("'"," ")
        #j'ajoute les éléments dans mon dict
        dict_jv.update({rank :title_string})
        rank += 1

    return dict_jv

def fonction_en_attente():
    my_dict = request_IGN_website(url_ign_ps5)
    print(my_dict)
    my_dict2 = request_IGN_website(url_ign_xbox)
    print(my_dict2)
    my_dict3 = request_IGN_website(url_ign_pc)
    print(my_dict3)

    final_dict = defaultdict(list)
    for d in (my_dict, my_dict2, my_dict3): # you can list as many input dicts as you want here
        for key, value in d.items():
            final_dict[key].append(value)

    print(final_dict)   

