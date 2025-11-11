import psycopg2
from Modelos import Usuario


def conectar():
      conn = psycopg2.connect(
        host="192.168.15.86",
        database="postgres",
        user="postgres",
        password="pass123"
        )
      return conn


def inserir_usuarios(usuarios : list[Usuario]):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS usuarios CASCADE;")
  
    try:
        comandos_sql = [
        """
            CREATE TABLE usuarios (
                id BIGINT NOT NULL PRIMARY KEY,
                username VARCHAR NOT NULL,
                email VARCHAR NULL,
                password VARCHAR NOT NULL,
                join_date DATE
            );
            """,
            ]
        
        tuplas = []
        for usuario in usuarios:
            tuplas.append((usuario.id, usuario.username, usuario.email, usuario.password, usuario.join_date))
            
    
        for comando in comandos_sql:
            cursor.execute(comando)
        cursor.executemany("INSERT INTO usuarios (id, username, email, password, join_date) VALUES (%s, %s, %s, %s, %s)", tuplas)
        conn.commit()
        return f"Mensagem de sucesso. {len(tuplas)} usuarios foram adicionados."
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

    finally:
        conn.close()

def buscar_usuarios(usuario_id=None):
    try:
        conn = conectar()
        cursor = conn.cursor()
        if(usuario_id is None):
            query = "SELECT username, id FROM usuarios"
            cursor.execute(query)
            resultado = cursor.fetchall()
            return resultado
          
        else:
            query = f"SELECT username, id FROM usuarios WHERE id = {usuario_id}"
            print(query)
            cursor.execute(query)
            resultado = cursor.fetchall()
            return resultado
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"
    finally:
        conn.close()