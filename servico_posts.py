from pymongo import MongoClient
from typing import TypedDict
from pymongo.collection import Collection
from pymongo import errors
from Modelos import Post
import randomname
from random import randint
from datetime import date, datetime



client : MongoClient = MongoClient()
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

db = client["lankedin"]
collection = db["posts"]

def inserir_posts(posts : list[Post]):
    collection.drop()
    result = collection.insert_many(posts)
    if result:
        return f"Mensagem de sucesso. Foram inseridos {len(posts)} documentos"
  
def buscar_posts(usuario: str = None):
    cursor = collection.find({"username" : usuario}).limit(3)
    posts_list = []
    for post in cursor:
        del post["_id"]
        novo_post = Post(**cursor)
        posts_list.append(novo_post)
    return posts_list

def deletar_post(id_post : int ):
    cursor = collection.find_one_and_delete({"id" : id_post})
    del cursor["_id"]
    post_deletado = Post(**cursor)
    print(post_deletado)
    return post_deletado

# def alterar_post(id_post : int):
#     cursor = collection.update_one({"id" : id_post})