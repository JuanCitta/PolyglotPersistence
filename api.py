from fastapi import FastAPI
from servico_usuarios import *
from servico_conexoes import *
from servico_posts import *
from Modelos import *
from datetime import datetime

app = FastAPI()


## --- Parte Usuarios -----------------------------------------------
@app.get("/users")
async def get_all_users():
    return buscar_usuarios()

@app.get("/users/{username}")
async def get_user_by_username(username : str):
    print(username)
    return buscar_usuario(username)

@app.post("/users")
async def insert_user(user : dict):
    id = user["id"]
    username = user["username"]
    email = user["email"]
    password = user["password"]
    usuario = Usuario(id=id,username= username, email= email, password= password, join_date= datetime.now())
    return inserir_usuario(usuario)

@app.post("/users/popular")
async def insert_user(user : list[dict]):
    usuarios = []
    for us in user:
        usuario = Usuario(**us)
        usuarios.append(usuario)
    return inserir_usuarios(usuarios)


@app.put("/users/{username}")
async def update_username(username : str,username_novo:str):
    return alterar_username(username,username_novo)

## --- Fim Usuarios -----------------------------------------------


## --- Parte Conexoes -----------------------------------------------
@app.post("/conexoes/popular")
async def insert_connections(conexoes : list[dict]):
    connections = []
    for conexao in conexoes:
        us_de = conexao["username_de"]
        us_para = conexao["username_para"]
        data = conexao["data_conexao"]
        data_c = datetime.fromisoformat(data)
        con = Conexao(username_de=us_de,username_para= us_para, data_conexao=data_c)
        connections.append(con)
    return inserir_conexoes(connections)
## --- FIM CONEXOES -------------------------------------------------

## --- PARTE POSTS -----------------------------------------------
@app.post("/posts/popular")
async def insert_posts(posts : list[dict]):
    return inserir_posts(posts)

@app.post("/posts/conexoes/popular")
async def insert_posts(posts : list[dict]):
    return inserir_conexao_posts(posts)
## --- FIM POSTS -------------------------------------------------
