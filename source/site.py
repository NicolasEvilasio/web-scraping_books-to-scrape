import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import os
import time


class Site:
    """Representa um site que pode ser acessado, analisado e salvo.

       Essa classe possui métodos para acessar o site com requests, fazer webscraping com beautiful soup e gerar um csv ou json com os dados extraídos.

       Atributos:
           url (str): A URL do site.

       Métodos:
           carregar_site(): Carrega o conteúdo HTML do site usando requests e beautiful soup.
           gerar_csv(): Gera um arquivo csv com os dados extraídos do site.
           gerar_json(): Gera um arquivo json com os dados extraídos do site.
   """

    def __init__(self, url):
        """Inicializa um objeto Site com a URL do site.

                Parâmetros:
                    url (str): A URL do site.
        """
        self.__url = url

    def carregar_site(self):
        """Carrega o conteúdo HTML do site usando requests e beautiful soup.

               Retorna:
                   soup (BeautifulSoup): Um objeto BeautifulSoup que representa o documento HTML do site.
       """
        os.system('cls')
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, features='html.parser')
        return soup
