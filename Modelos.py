from dataclasses import dataclass
from datetime import date


    
@dataclass
class Conexao:
    username_de : str
    username_para: str
    data_conexao : date

@dataclass
class Usuario:
    id : int
    username : str
    email : str
    password : str
    join_date : date