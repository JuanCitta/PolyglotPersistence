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
        cursor.close()
        conn.close()

def buscar_usuarios(usuario_id: str =None):
    try:
        conn = conectar()
        cursor = conn.cursor()
        if(usuario_id is None):
            query = "SELECT username, id FROM usuarios"
            cursor.execute(query)
            resultado = cursor.fetchall()
            
          
        else:
            query = f"SELECT username, id FROM usuarios WHERE id = %s"

            cursor.execute(query,(usuario_id))
            resultado = cursor.fetchall()
        
        return resultado
    
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"
    finally:
        cursor.close()
        conn.close()


def alterar_username(username : str,username_novo : str):
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """UPDATE usuarios SET username = %s
        usuarios WHERE id = %s"""
        cursor.execute(query,(username_novo,username))
        conn.commit()
        print(f"{cursor.rowcount} colunas atualizadas")

    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"
    finally:
        cursor.close()
        conn.close()

def alterar_password(username : str,password_novo : str):
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """UPDATE usuarios SET password = %s
        usuarios WHERE id = %s"""
        cursor.execute(query,(password_novo,username))
        conn.commit()
        print(f"{cursor.rowcount} colunas atualizadas")

    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"
    finally:
        cursor.close()
        conn.close()