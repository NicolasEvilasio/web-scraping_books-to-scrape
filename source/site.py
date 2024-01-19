import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
# import time


class Site:
    """Representa um site que pode ser acessado, analisado e salvo.

       Essa classe possui métodos para acessar o site com requests,
       fazer webscraping com beautiful soup e gerar um csv ou json com os dados extraídos.

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
        self.lista_dicionario_livros = None
        self.soup = None
        self.paginas = None
        self.articles = None
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
            self.paginas = int(self.soup.find('li', class_='current').text.strip()[-2:].strip())
        except AttributeError:
            self.paginas = 'index'

        return self.paginas

    def __achar_elemento_root(self):
        """Localiza a tag que será utilizada como elemento root para retornar as informações pertinentes aos livros

                Retorna:
                    articles (str): Elemento root da lista de livros
        """
        all_books = self.soup.find('ol')
        self.articles = all_books.find_all('article')

        return self.articles

    def coletar_dados(self):
        """Coleta dados dos livros.

                Retorna:
                    lista_dicionario_livros (list): lista de dicionários
        """
        max_tries = 5  # máximo de tentativas de conexão com cada página
        lista_dicionario_livros = []

        for n_pagina in tqdm(range(1, self.paginas + 1), 'Lendo páginas do site'):  # envolve o range com o tqdm
            tentativa_atual = 1
            while tentativa_atual <= max_tries:
                try:
                    response = requests.get(
                        f'https://books.toscrape.com/catalogue/category/books_1/page-{n_pagina}.html')
                    soup = BeautifulSoup(response.text, features='html.parser')

                    # all_books = soup.find('ol')
                    # articles = all_books.find_all('article')
                    self.__achar_elemento_root()

                    for article in self.articles:
                        titulo = article.find('h3').find('a')['title']
                        preco = article.find('p', class_='price_color').text[2:]
                        classificacao = article.find('p')['class'][1]
                        disponibilidade = article.find_all('p')[2].text.strip()

                        lista_dicionario_livros.append(
                            dict({'Título': titulo, 'Preço': preco, 'Classificaçao': classificacao,
                                  'Disponibilidade': disponibilidade}))
                    break
                except ConnectionError as e:
                    tentativa_atual += 1
                    print(f'Página: {n_pagina} ------ {e}')
                    # time.sleep(5)

        self.lista_dicionario_livros = lista_dicionario_livros

        return self.lista_dicionario_livros
