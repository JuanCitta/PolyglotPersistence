from pymongo import MongoClient
from Modelos import Post
from dataclasses import asdict
from servico_conexoes import inserir_conexao_post, inserir_conexao_posts

client : MongoClient = MongoClient()
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

db = client["lankedin"]
collection = db["posts"]

def contar_posts():
    try:
        res = collection.count_documents({})
        print(res)
        return res
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

def inserir_posts(posts : list[dict]):
    try:
        collection.drop()

        for post in posts:
            collection.insert_one(post)
        return f"Sucesso: Foram inseridos {len(posts)} posts"
    
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

def inserir_post(post : Post):
    try:
        result = collection.insert_one(asdict(post))
        inserir_conexao_post(post.id,post.username,post.create_date)
        return result
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

def buscar_posts(usuario: str):
    try:
        result = collection.find({"username" : usuario}).limit(3)
        posts_list = []
        for post in result:
            del post["_id"]
            novo_post = Post(**result)
            posts_list.append(novo_post)
        return posts_list
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

def buscar_post(id : str):
    try:
        result = collection.find_one({"id": id})
        del result["_id"]
        post_dict = Post(**result)
        return post_dict
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

def deletar_post(id_post : int ):
    try: 
        cursor = collection.find_one_and_delete({"id" : id_post})
        del cursor["_id"]
        post_deletado = Post(**cursor)
        return post_deletado
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

# def alterar_post(id_post : int):
#     cursor = collection.update_one({"id" : id_post})