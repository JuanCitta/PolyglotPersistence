from servico_postgres import inserir_usuarios
from gerador_de_dados import gerar_usuarios, gerar_conexoes
from servico_neo import inserir_conexoes

def main():
    lista_usuarios = gerar_usuarios(10)
    lista_conexoes = gerar_conexoes(lista_usuarios)

    inserir_usuarios(lista_usuarios)
    inserir_conexoes(lista_conexoes)



if __name__ == "__main__":
    main()

