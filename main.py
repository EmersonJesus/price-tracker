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

        # Objeto do pyodbc que será usado para conectar com o banco de dados
        self.conexao = None

    def capturar(self):
        # Preço do site no momento da consulta
        sqlInsert = "INSERT INTO tb_produtos (descricao, url, data, hora, preco) VALUES (?, ?, CURDATE(), CURTIME(), ?)"

        # Abrir o arquivo para leitura
        print("[i] Abrindo arquivo...")
        print('-' * 80)
        with open(self.nomeArquivo, mode='r', encoding='utf-8') as dados:
            arquivo = csv.reader(dados, delimiter=';')
            next(arquivo)  # Pulando a linha
            linhas = list(tuple(linha) for linha in arquivo)

        # Abrir conexão com o banco de dados
        print('[i] Conectando com o banco de dados...')
        print('-' * 80)
        self.conexao = self.conectarBancoSQL()
        cursor = self.conexao.cursor()

        # Pesquisa cada URL do arquivo
        for linha in linhas:
            url = linha[0]
            pagina = requests.get(url, headers=self.browserHeader)
            soup = BeautifulSoup(pagina.content, 'html.parser')
            produto = soup.find('span', id='productTitle').get_text()
            produto = produto.strip()
            preco = soup.find('span', id='priceblock_ourprice').get_text()
            preco = preco.strip().replace('R$', '').replace('.', '').replace(',', '.')
            show = f"{produto} | Preço atual: {preco}"
            print(f"[i] Consultando {show}")
            print('-' * 80)
            preco_atual = float(preco)
            alvo = float(linha[1])

            param = (produto, url, preco_atual)
            cursor.execute(sqlInsert, param)
            if preco_atual <= alvo:
                self.enviarEmail('emersoncruz692@gmail.com', produto, url)

    def conectarBancoSQL(self):
        servidor = 'localhost'
        banco = 'base_pessoal'
        passwd = 'senha do banco de dados'
        userbd = 'usuario do banco de dados'
        conexao = None

        try:
            conexao = pyodbc.connect(
                f"DRIVER={{MySQL ODBC 8.0 Driver Unicode}};SERVER={servidor};DATABASE={banco};UID={userbd};PWD={passwd}",
                autocommit=True)
            print("[i] Conectando com o banco de dados.")
            print('-' * 80)
        except (pyodbc.Error, pyodbc.OperationalError) as ex:
            print(ex.args[0], ex.args[1])
            conexao = None

        return conexao

    def enviarEmail(self, para, assunto, url):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        para = para.strip()
        assunto = assunto.strip()
        url = url.strip()

        if len(assunto) > 25:
            topo = assunto[:25] + '...'
        else:
            topo = assunto

        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('seu_email@gmail.com', 'sua_senha')
        assunto = f'O preço caiu! Item: {topo}'
        corpo = f'Acesse agora para ver {assunto}\nLink: {url}'
        msg = f'Subject: {assunto}\n\n{corpo}'
        server.sendmail(
            'seu_email@gmail.com',
            para,
            msg.encode('utf8')
        )
        print('[i] E-mail enviado!')
        print('-' * 80)
        server.quit()


amz = SpiderAmazon()
amz.capturar()