from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import sqlite3
from time import sleep
from datetime import datetime
from tabulate import tabulate

class WebPageAccess:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def setup_driver(self):
        # Configurando o ChromeDriver em modo headless
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Configurando o ChromeDriver usando WebDriver Manager
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def open_page(self):
        if self.driver is None:
            self.setup_driver()
        self.driver.get(self.url)

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def find_elements(self, by, value):
        return self.driver.find_elements(by, value)

    def close_driver(self):
        if self.driver is not None:
            self.driver.quit()

def create_database():
    conn = sqlite3.connect('precos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            valor_antigo TEXT,
            tipo_pagamento TEXT,
            valor_vista TEXT,
            desconto_vista TEXT,
            valor_parcelado TEXT,
            qnt_parcelas TEXT,
            link TEXT,
            data_hora_execucao TEXT
        )
    ''')
    conn.commit()
    return conn

def insert_data(conn, df):
    df.to_sql('precos', conn, if_exists='append', index=False)

if __name__ == "__main__":
    url = "https://www.pichau.com.br/hardware/memorias"  # Substitua pela URL que deseja acessar
    web_page = WebPageAccess(url)
    web_page.open_page()

    sleep(5)
    
    try:
        tabela = web_page.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div[2]/div/div[1]/div[3]')
        
        # Encontrar os elementos de link
        links_elements = web_page.find_elements(By.XPATH, '//*[@id="__next"]/div[1]/main/div[2]/div/div[1]/div[3]//a')

        # Processamento dos dados extraídos
        text = tabela.text
        linhas = text.split('\n')
        # print(linhas)

        nome = []
        valor_antigo = []
        tipo_pag_vsta = []
        valor_vista = []
        desconto_vista = []
        valor_parc = []
        qnt_parc = []
        links = []
        data_hora_execucao = []

        i = 0
        link_index = 0

        while i < len(linhas):
            if 'Memoria' in linhas[i]:
                nome.append(linhas[i])
                valor_antigo.append(linhas[i+1])
                tipo_pag_vsta.append(linhas[i+2])
                valor_vista.append(linhas[i+3])
                desconto_vista.append(linhas[i+4])
                valor_parc.append(linhas[i+5])
                qnt_parc.append(linhas[i+6])

                # Adiciona o link correspondente
                links.append(links_elements[link_index].get_attribute('href'))
                data_hora_execucao.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                link_index += 1

                i += 7
            else:
                i += 1

        df = pd.DataFrame({
            'nome': nome,
            'valor_antigo': valor_antigo,
            'tipo_pagamento': tipo_pag_vsta,
            'valor_vista': valor_vista,
            'desconto_vista': desconto_vista,
            'valor_parcelado': valor_parc,
            'qnt_parcelas': qnt_parc,
            'link': links,  # Nova coluna com os links
            'data_hora_execucao': data_hora_execucao
        })
        
        # Criar e conectar ao banco de dados SQLite
        conn = create_database()

        # Inserir os dados no banco de dados
        insert_data(conn, df)

        # Fechar a conexão
        conn.close()

    except Exception as e:
        print(f"Elemento não encontrado: {e}")
    
    web_page.close_driver()
