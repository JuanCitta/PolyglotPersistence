import random
from faker import Faker
from datetime import datetime, date, timedelta
from Modelos import Usuario,Conexao, Post

fake = Faker('pt_BR')

def gerar_nome():
    return f"{fake.first_name()} {fake.last_name()}"


def gerar_usuarios(n):
    usuarios = []
    for i in range(n):
        nome, sobrenome = fake.first_name(), fake.last_name()
        username = fake.user_name()
        email = f"{username}@email.com"
        senha = fake.password(8)
        join_date = fake.date_this_year()
        usuarios.append(Usuario(id=i,username=username,email=email,password=senha,join_date=join_date))
    return usuarios

def gerar_conexoes(usuarios):
    conexoes = []
    pares_conexao = set()  

    for u in usuarios:
        candidatos = []
        data_criacao = u.join_date
        
        id_usuario = u.id
        username_de = u.username

        candidatos = [us for us in usuarios if username_de != us.username ]

        if not candidatos:
            continue

        num_conexoes = random.randint(0, len(usuarios)//5)
        random.shuffle(candidatos)

        for candidato in range(min(num_conexoes, len(candidatos))):
            conexao = candidatos[candidato]
            username_para = conexao.username
            par = (min(username_de, username_para), max(username_de, username_para))
            if par in pares_conexao:
                continue  

            data = fake.date_between_dates(date_start=data_criacao,date_end=date(2025,12,11))
            conexoes.append(Conexao(username_de,username_para,data))
            pares_conexao.add(par)
    return conexoes


def gerar_posts(usuarios):
    posts = []
    if not usuarios: return
    for usuario in usuarios:
        for i in range(0,5):
            join_datetime = datetime.combine(usuario.join_date, datetime.min.time())
            data = fake.date_time_between_dates(datetime_start=join_datetime,datetime_end=datetime.now())
            novo_post : Post = {
                "id" : i,
                "username" : usuario.username,
                "likes" : 0,
                "comments" : [],
                "create_date" : data
            }
            posts.append(novo_post)
    return posts

