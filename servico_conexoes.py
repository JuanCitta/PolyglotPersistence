from neo4j import GraphDatabase
from Modelos import Conexao
from dataclasses import asdict

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password123")


def inserir_conexoes(conexoes):

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.execute_query("MATCH(n) DETACH DELETE (n)",database_="neo4j")
        driver.execute_query("CREATE CONSTRAINT IF NOT EXISTS FOR (u:user) REQUIRE u.username IS UNIQUE",
            database_="neo4j")
        driver.execute_query("CREATE CONSTRAINT IF NOT EXISTS FOR (p:post) REQUIRE p.post_id IS UNIQUE",
            database_="neo4j")

        for conexao in conexoes:
            records, summary, keys = driver.execute_query("""
                MERGE (a:user {username: $name})
                MERGE (b:user {username: $friendName})
                MERGE (a)-[:CONECTOU {desde: $date}]-(b)
                """,
                name=conexao.username_de, friendName=conexao.username_para,date= conexao.data_conexao,
                database_="neo4j",
            )
        if summary.counters.relationships_created > 0: return f"Mensagem de sucesso. {len(conexoes)} conexoes adicionadas."

def inserir_conexao(conexao : Conexao):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, summary, keys = driver.execute_query("""
                MERGE (a:user {username: $name})
                MERGE (b:user {username: $friendName})
                MERGE (a)-[:CONECTOU {desde: $date}]-(b)
                """,
                name=conexao.username_de, friendName=conexao.username_para,date= conexao.data_conexao,
                database_="neo4j",
            )
        if summary.counters.relationships_created > 0:
            
            return (f"Nova conexao: {conexao.username_de} <-> {conexao.username_para}")
        
        else:
            return print(f"Conexao ja existente: {conexao.username_de} <-> {conexao.username_para}")


def buscar_conexoes(usuario : str):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records,summary,keys = driver.execute_query(""" 
            MATCH (a : user)-[:CONECTOU]-(b: user)
            WHERE a.username = $name
            RETURN [b.username] AS Conexao
                                       
            """,
            name=usuario,database_="neo4j")
        conexoes_encontradas = [record["Conexao"] for record in records]
    return conexoes_encontradas


def remover_conexao(usuario1 :str, usuario2 : str):
    with GraphDatabase.driver(URI, auth= AUTH) as driver:
        records, summary, keys = driver.execute_query("""
            MATCH (a:user{username : $name1})-[r:CONECTOU]-(b:user {username : $name2})
            WITH a, b,r, r.desde AS data_conexao DELETE r
            RETURN a.username AS usuario_de, b.username AS usuario_para, data_conexao""",
            name1 = usuario1, name2 = usuario2, database_="neo4j")
        if(summary.counters.relationships_deleted > 0):
            record = records[0]
            conexao = Conexao(
                username_de = record["usuario_de"],
                username_para = record["usuario_para"],
                data_conexao = record["data_conexao"]
            )
            return asdict(conexao), f"Sucesso, conexao entre {conexao.username_de} e {conexao.username_para} deletada"
        else:
            print("Nenhuma conexao encontrada")
            return 
        
def remover_conexoes(usuario1 :str):
    with GraphDatabase.driver(URI, auth= AUTH) as driver:
        records, summary, keys = driver.execute_query("""
            MATCH (a:user{username : $name1})
            WITH a, a.username AS usuario_de
            DETACH DELETE a
            RETURN usuario_de""",
            name1 = usuario1, database_="neo4j")
        if(summary.counters.relationships_deleted > 0):
            record = records[0]
            username_de = record["usuario_de"],
            return f"Sucesso usuario {username_de} deletado {summary.counters.relationships_deleted} conexoes deletadas."
        else:
            print("Nenhuma conexao encontrada")
            return 

def inserir_conexao_post(post_id : int, username : str, data):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, summary, keys = driver.execute_query("""
                MERGE (a:user {username: $name})
                MERGE (b:post {post_id: $id_post})
                MERGE (a)-[:POSTOU {em: $date}]->(b)
                """,
                name=username, id_post=post_id,date= data,
                database_="neo4j",
            )
        if summary.counters.relationships_created > 0:
            
            print(f"Nova conexao: {username} -> {post_id}")
        
        else:
            print(f"Conexao ja existente: {username} -> {post_id}")
    return f"Post {post_id} de {username}"

def inserir_conexao_posts(posts):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        for post in posts:
            username =post["username"]
            post_id =post["id"]
            data =post["create_date"]
            records, summary, keys = driver.execute_query("""
                    MERGE (a:user {username: $name})
                    MERGE (b:post {post_id: $id_post})
                    MERGE (a)-[:POSTOU {desde: $date}]->(b)
                    """,
                    name=username, id_post=post_id,date= data,
                    database_="neo4j",
                )
    return f"Sucesso!: {len(posts)} conexoes de usuario->post adicionadas"

def inserir_like(username : str, id_post : int, data: str):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, summary, key = driver.execute_query("""
                MATCH (a:user {username: $name})
                MATCH (b:post {post_id: $friendName})
                MERGE (a)-[:GOSTOU {desde: $date}]->(b)
                """,
            name=username, friendName=id_post,date= data,
            database_="neo4j",
            )
        if summary.counters.relationships_created > 0: return f"Mensagem de sucesso. {username} gostou de {id_post}."