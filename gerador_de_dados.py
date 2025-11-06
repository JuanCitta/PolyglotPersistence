import random
from faker import Faker
from datetime import datetime, date, timedelta
from Modelos import Usuario,Conexao

fake = Faker('pt_BR')

def gerar_nome():
    return f"{fake.first_name()} {fake.last_name()}"


def gerar_usuarios(n):
    usuarios = []
    for i in range(n):
        nome, sobrenome = fake.first_name(), fake.last_name()
        if i % 2 == 0:
            username = f"{nome}_{sobrenome}"
            email = f"{nome}_{sobrenome}"
        elif i>n/2:
            username = f"{nome}.{sobrenome}"
            email = f"{nome}.{sobrenome}"
        else:
            username = f"{nome}{sobrenome}"
            email = f"{nome}{sobrenome}"
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

        for us in usuarios:
            if us.join_date <= data_criacao and us.id != id_usuario:
                candidatos.append(us)

        if not candidatos:
            continue

        num_conexoes = random.randint(0, len(usuarios)//5)
        random.shuffle(candidatos)

        for c in range(min(num_conexoes, len(candidatos))):
            conexao = candidatos[c]
            username_para = conexao.username
            par = (username_de, username_para)

            if par in pares_conexao:
                continue  

            data = fake.date_between_dates(date_start=data_criacao,date_end=date(2025,12,11))
            conexoes.append(Conexao(username_de,username_para,data))
            pares_conexao.add(par)

    return conexoes


