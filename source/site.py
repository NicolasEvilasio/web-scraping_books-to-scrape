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
           __url (str): A URL do site.

       Métodos:
           carregar_site(): Carrega o conteúdo HTML do site usando requests e beautiful soup.
           gerar_csv(): Gera um arquivo csv com os dados extraídos do site.
           gerar_json(): Gera um arquivo json com os dados extraídos do site.
   """

    def __init__(self, url: str):
        """Inicializa um objeto Site com a URL do site.

                Parâmetros:
                    url (str): A URL do site.
        """
        self.soup = None
        self.__url = url

    def carregar_site(self):
        """Carrega o conteúdo HTML do site usando requests e beautiful soup.

               Retorna:
                   soup (BeautifulSoup): Um objeto BeautifulSoup que representa o documento HTML do site.
       """
        os.system('cls')
        response = requests.get(self.__url)
        self.soup = BeautifulSoup(response.text, features='html.parser')
        return self.soup

    def contar_paginas(self):
        """Verifica a quantidade total de páginas no site.

                Cada página tem uma tag <li> cuja class "current" tem o valor "Página X de Y"

                Este método faz:
                    1 - usa o find para localizar a tag <li> com a class "current"
                    2 - retorna o texto dentro dessa tag usando a propriedade .text
                    3 - usei o strip para remover os espaoços no início e no fim da string retornada
                    4 - usei o slicer [-2:] para retornar os dois últimos caracteres da string
                    5 - Precisei usar o strip, pois se a página for menor que 10 irá ter um espaço em branco, assim ' 9'
                    6 - por fim, transformei em int


                Retorna:
                    paginas (int): Quantidade de páginas ou
                    index (str): Site tem apenas uma página
        """
        try:
            paginas = int(self.soup.find('li', class_='current').text.strip()[-2:].strip())
        except AttributeError as e:
            paginas = 'index'

        return paginas

    def __achar_elemento_root(self):
        """Localiza a tag que será utilizada como elemento root para retornar as informações pertinentes aos livros

                Retorna:
                    articles (str): Elemento root da lista de livros
        """
        all_books = self.soup.find('ol')
        articles = all_books.find_all('article')  # os dados dos livros estão dentro de uma tag article, dentro da ol

        return articles
