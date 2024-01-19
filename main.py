import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import os
import time
import source

# 0 - Ajustar o pandas para printar sem truncar as colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# 1 - Retornar o html do site
os.system('cls')
response = requests.get('https://books.toscrape.com/catalogue/category/books_1/index.html')
soup = BeautifulSoup(response.text, features='html.parser')

# 2 - Verificar a quantidade total de páginas
'''
Cada página tem uma tag <li> cuja class "current" tem o valor "Página X de Y"
O código abaixo faz:

1 - usa o find para localizar a tag <li> com a class "current"
2 - retorna o texto dentro dessa tag usando a propriedade .text
3 - usei o strip para remover os espaoços no início e no fim da string retornada
4 - usei o slicer [-2:] para retornar os dois últimos caracteres da string
5 - Precisei usar o strip, pois se a página for menor que 10 irá ter um espaço em branco, assim ' 9'
6 - por fim, transformei em int
'''
ultima_pagina = int(soup.find('li', class_='current').text.strip()[-2:].strip())

# 3 - localizar o elemento "root" dos livros
all_books = soup.find('ol')
articles = all_books.find_all('article')  # os dados dos livros estão dentro de uma tag article, dentro da ol

# 4 - iterar sobre as páginas e coletar os dados dos livros
lista_dicionario_livros = []
MAX_TRIES = 5  # máximo de tentativas de conexão com cada página

for n_pagina in tqdm(range(1, ultima_pagina + 1), 'Lendo páginas do site'):  # envolve o range com o tqdm
    tentativa_atual = 1
    while tentativa_atual <= 5:
        try:
            response = requests.get(f'https://books.toscrape.com/catalogue/category/books_1/page-{n_pagina}.html')
            soup = BeautifulSoup(response.text, features='html.parser')

            all_books = soup.find('ol')
            articles = all_books.find_all('article')

            for article in articles:
                titulo = article.find('h3').find('a')['title']
                preco = article.find('p', class_='price_color').text[2:]
                classificacao = article.find('p')['class'][1]
                disponibilidade = article.find_all('p')[2].text.strip()

                lista_dicionario_livros.append(dict({'Título': titulo, 'Preço': preco, 'Classificaçao': classificacao,
                                                     'Disponibilidade': disponibilidade}))
            break
        except ConnectionError as e:
            tentativa_atual += 1
            print(f'Página: {n_pagina} ------ {e}')
            time.sleep(5)

# Quantidade de livros extraídos do site
df = pd.DataFrame(lista_dicionario_livros)
print(f'\n{len(lista_dicionario_livros)} livros encontrados',
      '\nexibindo os 20 primeiros livros:',
      df.head(20),
      sep='\n')


