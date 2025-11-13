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
        return f"Sucesso: Foi inserido post de id: {post.id}.", result
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

def buscar_posts(usuario: str):
    try:
        result = collection.find({"username" : usuario})
        posts_list = []
        for post in result:
            del post["_id"]
            posts_list.append(post)
        print(posts_list)
        return posts_list, f"Usuario tem {len(posts_list)} postagens"
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

def buscar_post(id : int):
    try:
        result = collection.find_one({"id": id})
        # if(result):
        #     del result["_id"]
        return f"Post do usuario: {result["username"]} ", result
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

def deletar_post(id_post : int ):
    try: 
        cursor = collection.find_one_and_delete({"id" : id_post})
        del cursor["_id"]
        post_deletado = cursor
        return post_deletado, f"Post {id_post} foi deletado"
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

def alterar_post(id_post : int, title:str, body: str):
    try: 
        cursor = collection.find_one_and_update({"id" : id_post},
                                   {
                                    "$set": { "title": title, "body": body },
                                    "$currentDate" : { "lastModified": True }})
        if cursor :
            del cursor["_id"]
            post_alterado = cursor
            return post_alterado, f"Post {id_post} foi alterado"
        else: 
            return f"Nenhum post encontrado. "
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

def alterar_likes_post(id_post : int):
    try: 
        cursor = collection.find_one_and_update({"id" : id_post},
                                   {
                                    "$inc": { "likes": 1},
                                   })
        if cursor :
            del cursor["_id"]
            post_alterado = cursor
            return post_alterado, f"Post {id_post} foi alterado"
        else: 
            return f"Nenhum post encontrado. "
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

