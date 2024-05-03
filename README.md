# Rastreador de Preços de Produtos

![](https://i.imgur.com/egQnuuM.png)

Este é um rastreador de preços de produtos desenvolvido em Python utilizando Flask e TinyDB. Ele permite aos usuários acompanhar os preços de produtos de sites online e receber notificações quando os preços atingem um valor-alvo específico.

## Funcionalidades

- Adicionar produtos para rastreamento, informando o URL e o preço-alvo de cada produto.
- Visualizar a lista de produtos rastreados, incluindo nome, imagem, preço atual e preço-alvo.
- Excluir produtos da lista de rastreamento.

## Como Usar

1. Clone o repositório para o seu ambiente local.
2. Instale as dependências necessárias utilizando `pip install -r requirements.txt`.
3. Execute a aplicação utilizando o comando `python app.py`.
4. Acesse a aplicação em seu navegador através do endereço `http://localhost:5000`.

## Tecnologias Utilizadas

- Python
- Flask
- TinyDB
- BeautifulSoup (para web scraping)
- Requests (para realizar requisições HTTP)

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para fazer um fork do projeto e enviar pull requests com melhorias, correções de bugs ou novas funcionalidades.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
