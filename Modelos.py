from dataclasses import dataclass
from datetime import date, datetime


    
@dataclass
class Conexao:
    username_de : str
    username_para: str
    data_conexao : str

@dataclass
class Usuario:
    id : int
    username : str
    email : str
    password : str
    join_date : str

@dataclass
class Post:
    id : int
    title: str
    body : str
    username: str
    likes : int
    comments : list
    create_date : str

@dataclass
class Like:
    id : int
    username_de : str
    username_para : str
    data_conexao : str

@dataclass
class Comentario:
    id : int
    id_post : int
    username: str
    likes : int
    responses : list
    create_date : str
