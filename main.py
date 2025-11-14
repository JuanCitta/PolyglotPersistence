from servico_usuarios import *
from servico_posts import *
from servico_conexoes import *
from gerador_de_dados import *
from Modelos import *
import requests


def main():
    print("--------------------------------")
    print("            Lankedin")
    print("--------------------------------")
    print("Digite o numero da funcionalidade: ")
    print("Modos: 1.   Popular banco")
    print("Modos: 2. C Inserir dados")
    print("Modos: 3. R Mostrar dados")
    print("Modos: 4. U Alterar dados")
    print("Modos: 5. D Deletar dados")
    i = int(input("Digite o numero da funcionalidade: "))

    match i:
        case 1:
            lista_usuarios = popular_usuarios(10)
            lista_conexoes = popular_conexoes(lista_usuarios)
            lista_posts = popular_posts(lista_usuarios)
            inserir_usuarios(lista_usuarios)
            inserir_conexoes(lista_conexoes)
            inserir_posts(lista_posts)
        case 2:
            print("1. Inserir usuario")
            print("2. Inserir conexao entre usuarios")
            print("3. Inserir Post")
            m = int(input("Digite o modo"))
            match m:
                case 1:
                    user = gerar_usuario(quantidade_usuarios())
                    inserir_usuario(user)
                case 2:
                    con = gerar_conexao()
                    inserir_conexao(con)
                case 3:
                    post = gerar_post()
                    inserir_post(post)
        case 3:
            print("1. Mostrar PostgreSQL")
            print("2. Mostrar Neo4j")
            print("3. Mostrar MongoDB")
            m = int(input("Digite o modo"))
            match m:
                case 1:
                    u = input("Digite o usuario: ")
                    res = buscar_usuario(u)
                    print(res)
                case 2:
                    u = input("Digite o usuario: ")
                    res = buscar_conexoes(u)
                    print(res)
                case 3:
                    p = int(input("Digite o id do post: "))
                    res = buscar_post(p)
                    print(res)
        case 4:
            print("1. Alterar usuario")
            print("2. Alterar senha")
            print("2. Alterar post")
            m = int(input("Digite o modo"))
            match m:
                case 1:
                    u = input("Digite o nome de usuario: ")
                    un = input("Digite o novo nome de usuario: ")
                    res = alterar_username(u,un)
                    print(res)
                case 2:
                    p = input("Digite o username: ")
                    passw = input("Digite a senha")
                    res = alterar_password(p,passw)
                    print(res)
                case 3:
                    p = input("Digite o username: ")
                    passw = input("Digite a senha")
                    res = alterar_password(p,passw)
                    print(res)

        case 5:
            print("1. Deletar usuario")
            print("2. Deletar conexao")
            print("3. Deletar post")
            m = int(input("Digite o modo"))
            match m:
                case 1:
                    p = input("Digite o username: ")
                    passw = input("Digite a senha")
                    res = remover_usuario(p,passw)
                case 2:
                    u = input("Digite o usuario1: ")
                    u2 = input("Digite o usuario2: ")
                    res = remover_conexao(u,u2)
                    print(res)
                case 3:
                    p = int(input("Digite o id do post: "))
                    res = deletar_post(p)
                    print(res)


if __name__ == "__main__":
    main()

