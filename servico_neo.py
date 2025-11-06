from neo4j import GraphDatabase
from Modelos import Usuario, Conexao

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password123")

def inserir_conexoes(conexoes : list[Conexao]):

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.execute_query("CREATE CONSTRAINT FOR (u:User) REQUIRE u.username IS UNIQUE",
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
        if(summary): return f"Mensagem de sucesso. {len(conexoes)} conexoes adicionadas."

