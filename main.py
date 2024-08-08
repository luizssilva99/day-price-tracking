from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
from datetime import datetime
from tabulate import tabulate

class WebPageAccess:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def setup_driver(self):
        # Configurando o ChromeDriver usando WebDriver Manager
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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
        print(linhas)

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
            'Nome': nome,
            'Valor Antigo': valor_antigo,
            'Tipo de Pagamento': tipo_pag_vsta,
            'Valor a Vista': valor_vista,
            'Desconto a Vista': desconto_vista,
            'Valor Parcelado': valor_parc,
            'Quantidade de Parcelas': qnt_parc,
            'Link': links,  # Nova coluna com os links
            'Data e Hora de Execução': data_hora_execucao
        })

        # Exibição do DataFrame formatado
        print(tabulate(df, headers='keys', tablefmt='pretty'))   

        df.to_excel(f'tabela_precos{datetime.now().strftime('%Y-%m-%d')}.xlsx', index=False)       


    except Exception as e:
        print(f"Elemento não encontrado: {e}")
    
    web_page.close_driver()
