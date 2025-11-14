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
    usuario = buscar_usuario(username)
    return usuario

@app.post("/users")
async def insert_user(user : dict):
    usuario = Usuario(**user)
    return inserir_usuario(usuario)

@app.post("/users/popular")
async def insert_user(user : list[dict]):
    usuarios = []
    for us in user:
        usuario = Usuario(**us)
        usuarios.append(usuario)
    return inserir_usuarios(usuarios)

@app.put("/users/{us}")
async def update_username(us : str, userdata : dict):
    
    username_novo = userdata["username_novo"]
    return alterar_username(us,username_novo)

@app.put("/users/atualizar_senha/{u}")
async def update_password(u : str, userdata : dict):
    senha_nova = userdata["senha_nova"]
    return alterar_password(u,senha_nova)

@app.delete("/users/{u}")
async def delete_user(u : str, userdata : dict):
    senha = userdata["senha"]
    msg= remover_usuario(u,senha)
    return msg

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

@app.post("/conexoes/posts")
async def post_connection_to_post(data : dict):
    data_p,username,id_post = data["data"],data["username"],data["id_post"]
    msg = inserir_conexao_post(id_post,username,data_p)
    return msg

@app.post("/conexoes")
async def insert_connection(conexao : dict):
    con = Conexao(**conexao)
    return inserir_conexao(con)

@app.post("/conexoes/likes/{u}")
async def insert_like(u: str, data : dict):
    id_post = data["id_post"]
    date = data["date"]
    return inserir_like(username=u,id_post=id_post,data=date)


@app.get("/conexoes/{username}")
async def get_connections_by_username(username : str):
    conexao = buscar_conexoes(username)
    return conexao

@app.delete("/conexoes/{u}")
async def delete_connection(u : str, userdata : dict):
    us2 = userdata["usuario_2"]
    res, msg = remover_conexao(u,us2)
    return msg

@app.delete("/conexoes/remover_usuario/{u}")
async def delete_connections(u : str, userdata: dict):
    msg= remover_conexoes(u)
    return msg

@app.put("/conexoes/alterar_usuario/{u}")
async def alter_username(u: str, data : dict):
    un = data["username_novo"]
    msg = alterar_usuario_conexao(u,un)
    return msg
## --- FIM CONEXOES -------------------------------------------------

## --- PARTE POSTS -----------------------------------------------
@app.post("/posts/popular")
async def insert_posts(posts : list[dict]):
    return inserir_posts(posts)

@app.post("/posts/conexoes/popular")
async def insert_posts_nodes(posts : list[dict]):
    return inserir_conexao_posts(posts)

@app.post("/posts")
async def insert_post(post : dict):
    p = Post(**post)
    msg = inserir_post(p)
    return msg

@app.get("/posts/{id}")
async def get_post_by_id(id : int):
    post= buscar_post(id)
    return post

@app.get("/posts/por/{u}")
async def get_post_by_user(u: str):
    posts = buscar_posts(u)
    return posts

@app.delete("/posts/{id_post}")
async def delete_post_by_id(id_post: int):
    post, msg = deletar_post(id_post)
    return msg

@app.put("/posts/{id_post}")
async def alter_post_by_id(id_post : int, data : dict):
    title = data["title"]
    body = data["body"]
    post = alterar_post(id_post, title, body)
    return post

@app.put("/posts/like/{id_post}")
async def like_post(id_post : int):
    post = alterar_likes_post(id_post)
    return post

@app.put("/posts/alterar_usuario/{u}")
async def alter_username_posts(u: str, data : dict):
    un = data["username_novo"]
    msg = alterar_usuario_post(u,un)
    return msg

## --- FIM POSTS -------------------------------------------------
