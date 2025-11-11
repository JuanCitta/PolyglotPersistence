from neo4j import GraphDatabase
from Modelos import Conexao

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password123")


def inserir_conexoes(conexoes : list[Conexao]):

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.execute_query("MATCH(n) DETACH DELETE (n)",database_="neo4j")
        driver.execute_query("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.username IS UNIQUE",
            database_="neo4j")

        for conexao in conexoes:
            summary = driver.execute_query("""
                MERGE (a:User {username: $name})
                MERGE (b:User {username: $friendName})
                MERGE (a)-[:CONECTOU {desde: $date}]->(b)
                """,
                name=conexao.username_de, friendName=conexao.username_para,date= conexao.data_conexao,
                database_="neo4j",
            )
        if(summary.count>0): return f"Mensagem de sucesso. {len(conexoes)} conexoes adicionadas."


def buscar_conexoes(usuario=None):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records,summary,keys = driver.execute_query(""" 
            MATCH (a : User)-[:CONECTOU]-(b: User)
            WHERE a.username = $name
            RETURN [b.username] AS Conexao
                                       
            """,
            name=usuario,database_="neo4j")
        conexoes_encontradas = [record["Conexao"] for record in records]
    return conexoes_encontradas

def deletar_conexao(usuario1 :str, usuario2 : str):
    with GraphDatabase.driver(URI, auth= AUTH) as driver:
        records, summary, keys = driver.execute_query("""
            MATCH (a:User{username : $name1})-[r:CONECTOU]-(b:User {username : $name2})
            WITH a, b,r, r.desde AS data_conexao DELETE r
            RETURN a.username AS usuario_de, b.username AS usuario_para, data_conexao""",
            name1 = usuario1, name2 = usuario2, database_="neo4j")
        if(summary.counters.relationships_deleted > 0):
            record = records[0]
            conexao : Conexao = {
                "usuario_de" : record["usuario_de"],
                "usuario_para" : record["usuario_para"],
                "data_conexao" : record["data_conexao"]
            }
            return conexao
        else:
            print("Nenhuma conexao encontrada")
            return 