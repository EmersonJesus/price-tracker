import csv
import smtplib
import pyodbc
import requests
from bs4 import BeautifulSoup

class SpiderAmazon:
    def __init__(self):
        
        # Arquivo com os produtos
        self.nomeArquivo = 'lista_de_desejos.txt'
        
        # User agent
        self.browserHeader = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
        }

        # Objeto do pyodbc que sera usado para conectar com o banco de dadps
        self.conexao = None
        
    def capturar(self):
        
        # Preço do site no momento da consulta
        sqlInsert = "INSERT INTO tb_produtos (descricao, url, data, hora, preco) VALUES " \
                    " (?, ?, date(now()), time(now()), ?)"
                    
        # Abrir o arquivo para leitura
        print("[i] Abrindo arquivo...")
        print('-' * 80)
        with open(self.nomeArquivo, mode='r', encoding='utf-8') as dados:
            arquivo = csv.reader(dados, delimiter=';')
            next(arquivo) # Pulando a linha
            linhas = list(tuple(linha) for linha in arquivo)
            
        # Abrir conexão com banco de dados
        print('[i] Conectando com o banco de dados...')
        print('-' * 80)
        self.conexao = self.conectarBancoSQL()
        cursor = self.conexao.cursor()
        
        # Pesquisa cada URL do aquivo
        for linha in linhas:
            url = linha[0]
            pagina = request.get(url, headers=self.browserHeader)
            soup = BeautifulSoup(pagina.content, 'html.parser')
            
