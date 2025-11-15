import random
from faker import Faker
from datetime import datetime, date, timedelta
from Modelos import Usuario,Conexao, Post, Comentario
from servico_usuarios import quantidade_usuarios, usuario_aleatorio
from servico_posts import contar_posts

fake = Faker('pt_BR')

def gerar_usuario():
    n = quantidade_usuarios()
    id = n[0]
    id += 1
    username = fake.user_name()
    email = f"{username}@email.com"
    senha = "password"#fake.password(8)
    join_date = fake.date_this_year()
    string_date = join_date.strftime("%Y-%m-%d %H:%M:%S")
    user =(Usuario(id=id,username=username,email=email,password=senha,join_date=string_date))
    return user

def gerar_conexao():
    user1 = usuario_aleatorio()
    user2 = usuario_aleatorio()
    while(user1 == user2):
        user2 = usuario_aleatorio()
    date_start = min(user1.join_date,user2.join_date)
    connect_date = fake.date_between_dates(date_start=date_start,date_end=date(2025,12,11))
    string_date = connect_date.strftime("%Y-%m-%d %H:%M:%S")
    conexao = Conexao(username_de=user1.username,username_para=user2.username,data_conexao=string_date)
    return conexao

def gerar_post():
    user = usuario_aleatorio()
    id = contar_posts() + 1
    date = datetime.now()
    string_date = date.strftime("%Y-%m-%d %H:%M:%S")
    titulo = fake.bairro()
    corpo = fake.catch_phrase()
    post = Post(comments=[],create_date=string_date,id=id,username=user.username,likes=0,title=titulo,body=corpo)
    return post

def popular_usuarios(n):
    usuarios = []
    for i in range(n):
        username = fake.user_name()
        email = f"{username}@email.com"
        senha = "password" #fake.password(8)
        join_date = fake.date_this_year()
        string_date = join_date.strftime("%Y-%m-%d")
        usuarios.append(Usuario(id=i,username=username,email=email,password=senha,join_date=string_date))
    return usuarios


def popular_conexoes(usuarios):
    conexoes = []
    pares_conexao = set()  

    for u in usuarios:
        candidatos = []
        username_de = u.username
        candidatos = [us for us in usuarios if username_de != us.username ]

        if not candidatos:
            continue

        num_conexoes = random.randint(0, len(usuarios)//5)
        random.shuffle(candidatos)

        for candidato in range(min(num_conexoes, len(candidatos))):
            conexao = candidatos[candidato]
            data_criacao = min(u.join_date, conexao.join_date)
            username_para = conexao.username
            par = (min(username_de, username_para), max(username_de, username_para))
            if par in pares_conexao:
                continue  
            
            if(isinstance(data_criacao,str)): data_criacao_date = datetime.strptime(data_criacao, '%Y-%m-%d').date()
            data = fake.date_between(start_date=data_criacao_date,end_date=date(2025,12,11))
            string_date = data.strftime("%Y-%m-%d %H:%M:%S")
            conexoes.append(Conexao(username_de,username_para,string_date))
            pares_conexao.add(par)
    return conexoes


def popular_posts(usuarios):
    posts = []
    count = 0
    if not usuarios: return
    for usuario in usuarios:
        for i in range(0,3):
            count+= 1
            titulo = fake.bairro()
            corpo = fake.catch_phrase()
            data = datetime.now()
            string_date = data.strftime("%Y-%m-%d %H:%M:%S")
            novo_post = {
                "id" : count,
                "title" : titulo,
                "body" : corpo,
                "username" : usuario.username,
                "likes" : 0,
                "comments" : [],
                "create_date" : string_date
            }

            posts.append(novo_post)
    return posts

# def popular_comentarios(usuarios,posts):
#     comentarios = []
#     count = 0
#     if not usuarios or not posts: return
#     for usuario in usuarios:
#         count += 1
#         post = random.choice(posts)
#         novo_comentario : Comentario = {
#             "id" : count,
#             "username" : usuario.username,
#         }
