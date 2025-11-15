# PolyglotPersistence
Projeto sobre a implementação da infraestrutura de uma rede social simples.
As funcionalidades atuais são: CRUD de posts, usuários, likes em posts e conexões entre usuários.

## Como rodar
* Clonando o repositório basta abrir um terminal no diretório "PolyglotPersistence".
* Inserir o comando "docker-compose up -d" para subir os bancos (-d libera o terminal após a conclusão)
* Inserir o comando fastapi run api.py para subir o servidor uvicorn no endereco e porta :http://127.0.0.1:8000/
* Em outro terminal inserir o comando python requester.py
* Isso abrira um menu interativa para acessar as funcionalidades.
* As operações e seus resultados serão salvos no log.txt


## Justificativa da escolha dos bancos

#### Postgres

Escolhemos o Postgres para salvar os dados de login e da conta do usuário. 
Por se tratarem de informações com uma estrutura rígida, decidimos que um banco
relacional seria suficiente para atender as funcionalidades requisitadas pelo serviço
CRUD dos usuários.

#### Neo4j

Escolhemos o Neo4j para salvar os dados dos relacionamentos entre usuários e posts.
Por se tratar de dados que dependem das relações entre duas entidades, um banco direcionado
por grafos fez muito sentido.

#### MongoDB

Escolhemos o MongoDB para salvar os posts. São um dado que podem variar em sua estrutura
então um banco de documentos, com estrutura flexível se alinhou com as necessidades.

## Descrição do S2

Implementamos esse serviço que recebe as requisições HTTP do requester.py, realiza a operação e retorna
os dados ou mensagens de erro.

## Dependências

#### Python

Instalar o Python: https://www.python.org/downloads/

#### Docker

Instalar o docker: https://www.docker.com/get-started/


### Bibliotecas

#### Requests

Biblioteca para gerar HTTP requests 

pip install requests

#### FastAPI

Biblioteca para manejar as requests HTTP

pip install fastapi

#### Neo4j

Driver do Neo4j para Python

pip install neo4j

#### Mongo

Driver do Mongo para Python

pip install pymongo

#### Psycopg2

Driver do Neo4j para Python

pip install psycopg2
