from servico_usuarios import *
from servico_posts import *
from servico_conexoes import *
from gerador_de_dados import *
from Modelos import *
import requests

url = 'http://127.0.0.1:8000' 

def inserir_no_log(response):
    string = f"{response.text} em {response.elapsed} \n"
    with open("log.txt", 'a') as log:
        log.write(string)

def inserir_string_log(strin):
    with open("log.txt", 'a') as log:
        log.write(strin+"\n")

def fazer_request(operacao,dados,endpoint):
    try:

        metodo = getattr(requests,operacao)
        if operacao.lower() == 'get':
            req = metodo(url + endpoint)
        else:
            req = metodo(url + endpoint, json=dados)
        req.raise_for_status()
        inserir_no_log(req)
    except requests.exceptions.HTTPError as err:
        print(f"Erro HTTP: {err}")
        inserir_string_log(str(err))
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        inserir_string_log(str(e))

def transformar_em_dict(lista : list):
    if(isinstance(lista, list)):
        lista_limpa = []
        for elemento in lista:
            lista_limpa.append(asdict(elemento))
        return lista_limpa
    else: return asdict(lista)

def menu():
    print("--------------------------------")
    print("            Lankedin")
    print("--------------------------------")
    print("Digite o numero da funcionalidade: ")
    print("Modos: 1.   Popular banco")
    print("Modos: 2. C Inserir dados")
    print("Modos: 3. R Mostrar dados")
    print("Modos: 4. U Alterar dados")
    print("Modos: 5. D Deletar dados")
    print("Modos: 6. - Mostrar Menu")
    print("Modos: 0. - Sair")

def main():
    menu()
    i = 1
    while(i != 0):
        i = int(input("Digite o numero da funcionalidade: "))

        match i:
            case 1:
                lista_usuarios = popular_usuarios(10)
                lista_conexoes = transformar_em_dict(popular_conexoes(lista_usuarios))
                lista_posts    = popular_posts(lista_usuarios)
                lista_usuarios_l = transformar_em_dict(lista_usuarios)
                fazer_request("post",lista_usuarios_l,"/users/popular")
                fazer_request("post",lista_conexoes,"/conexoes/popular")
                fazer_request("post",lista_posts,"/posts/popular")
                fazer_request("post", lista_posts,"/posts/conexoes/popular")
            case 2:
                print("1. Inserir usuario")
                print("2. Inserir conexao entre usuarios")
                print("3. Inserir Post")
                print("4. Inserir like")
                m = int(input("Digite o modo: "))
                match m:
                    case 1:
                        user = asdict(gerar_usuario())
                        fazer_request("post",user,"/users")
                    case 2:
                        con = asdict(gerar_conexao())
                        fazer_request("post",con,"/conexoes")
                    case 3:
                        post = gerar_post()
                        conexao_post = {"username": post.username, "id_post" : post.id,"data": post.create_date}
                        fazer_request("post",asdict(post),"/posts")
                        fazer_request("post",conexao_post,"/conexoes/posts")
                    case 4:
                        u = input("Digite o usuario: ")
                        post = int(input("Digite o id_post: "))
                        date = datetime.now()
                        string_date = date.strftime("%Y-%m-%d %H:%M:%S")
                        like = {"id_post" : post, "date": string_date}
                        fazer_request("put",post,f"/posts/like/{post}")
                        fazer_request("post",like,f"/conexoes/likes/{u}")

            case 3:
                print("1. Mostrar informacao de usuario")
                print("2. Mostrar conexoes de usuario")
                print("3. Mostrar Post por ID")
                print("4. Mostrar Posts por username")
                print("5. Mostrar todos os usuarios")
                m = int(input("Digite o modo: "))
                match m:
                    case 1:
                        u = input("Digite o usuario: ")
                        fazer_request("get",u,f"/users/{u}")
                    case 2:
                        u = input("Digite o usuario: ")
                        fazer_request("get",u,f"/conexoes/{u}")
                    case 3:
                        p = int(input("Digite o id do post: "))
                        fazer_request("get",p,f"/posts/{p}")
                    case 4:
                        u =input("Digite o usuario para ver seus posts: ")
                        fazer_request("get",u,f"/posts/por/{u}")
                    case 5:
                        u = 0
                        fazer_request("get",u,f"/users")
            case 4:
                print("1. Alterar usuario")
                print("2. Alterar senha")
                print("3. Alterar post")
                m = int(input("Digite o modo: "))
                match m:
                    case 1:
                        u = input("Digite o nome de usuario: ")
                        un = input("Digite o novo nome de usuario: ")
                        dados = {"username_novo" : un}
                        fazer_request("put",dados,f"/users/{u}")
                        fazer_request("put",dados,f"/conexoes/alterar_usuario/{u}")
                        fazer_request("put",dados,f"/posts/alterar_usuario/{u}")
                    case 2:
                        u = input("Digite o nome de usuario: ")
                        p = input("Digite o novo password: ")
                        dados = {"senha_nova" : p}
                        fazer_request("put",dados,f"/users/atualizar_senha/{u}")
                    case 3:
                        p = int(input("Digite o id do post: "))
                        title = input("Digite o novo titulo: ")
                        body = input("Digite o novo corpo: ")
                        dados = {"title" : title, "body" : body}
                        fazer_request("put",dados,f"/posts/{p}")
                        

            case 5:
                print("1. Deletar usuario")
                print("2. Deletar conexao")
                print("3. Deletar post")
                m = int(input("Digite o modo: "))
                match m:
                    case 1:
                        u = input("Digite o nome de usuario: ")
                        p = input("Digite o password: ")
                        dados = {"senha" : p}
                        fazer_request("delete",dados,f"/users/{u}")
                        fazer_request("delete",dados,f"/conexoes/remover_usuario/{u}")
                    case 2:
                        u = input("Digite o usuario1: ")
                        u2 = input("Digite o usuario1: ")
                        dados = {"usuario_2" : u2}
                        fazer_request("delete",dados,f"/conexoes/remover_usuario/{u}")
                    case 3:
                        p = int(input("Digite o id do post: "))
                        fazer_request("delete",p,f"/posts/{p}")
            case 6:
                menu()

if __name__ == "__main__":
    main()

