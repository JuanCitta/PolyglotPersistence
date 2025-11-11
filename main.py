from servico_usuarios import *
from servico_posts import *
from servico_conexoes import *
from gerador_de_dados import *

def main():
    i = input("Digite o modo: ")
    match i:
        case 1:
            lista_usuarios = gerar_usuarios(10)
            lista_conexoes = gerar_conexoes(lista_usuarios)
            lista_posts = gerar_posts(lista_usuarios)
            inserir_usuarios(lista_usuarios)
            inserir_conexoes(lista_conexoes)
            inserir_posts(lista_posts)
        case 2:
            res = buscar_conexoes("cauemendes")
            print(res)
            buscar_posts("xmachado")
            deletar_conexao("jda-cruz","tpastor")
            deletar_post(0)

if __name__ == "__main__":
    main()

