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

def inserir_usuario(user):
    conn = conectar()
    cursor = conn.cursor()
  
    try:
        query = "INSERT INTO usuarios(id, username, email, password, join_date) VALUES(%s, %s, %s, %s, %s)"
        tupla = (user.id, user.username, user.email, user.password, user.join_date)
        cursor.execute(query,tupla)
        conn.commit()
        return f"Mensagem de sucesso. {len(tupla)} usuarios foram adicionados."

    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"

    finally:
        cursor.close()
        conn.close()

def buscar_usuario(username):
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM usuarios WHERE username = %s"
        cursor.execute(query,(username,))
        resultado = cursor.fetchone()
        retorno = Usuario(*resultado)
        return retorno
    
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"
    finally:
        cursor.close()
        conn.close()

def buscar_usuarios():
    try:
        conn = conectar()
        cursor = conn.cursor()
        usuarios = []
        query = "SELECT * FROM usuarios"
        cursor.execute(query)
        resultado = cursor.fetchall()
        for us in resultado:
            usuarios.append(Usuario(*us))
        return usuarios
        
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"
    finally:
        cursor.close()
        conn.close()

def quantidade_usuarios():
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """SELECT COUNT(*) FROM usuarios;"""
        cursor.execute(query)
        resultado = cursor.fetchall()[0]
        return resultado
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"
    finally:
        cursor.close()
        conn.close()

def usuario_aleatorio():
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """SELECT *
                    FROM usuarios
                    ORDER BY RANDOM()
                    LIMIT 1;"""
        cursor.execute(query)
        resultado = cursor.fetchone()
        user = Usuario(resultado[0],resultado[1],resultado[2],resultado[3],resultado[4])
        return user
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
         WHERE username = %s"""
        cursor.execute(query,(username_novo,username))
        conn.commit()
        return (f"{cursor.rowcount} colunas atualizadas")

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
         WHERE username = %s"""
        cursor.execute(query,(password_novo,username))
        conn.commit()
        return f"Sucesso, {username} alterou a senha. {cursor.rowcount} colunas atualizadas"
    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()

def remover_usuario(username : str, password: str):
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = "DELETE FROM usuarios where username = %s AND password = %s"
        cursor.execute(query,(username,password))
        conn.commit()
        return f"Sucesso, usuario {username} deletado "

    except Exception as e:
        print(e)
        return f"Erro na transacao com o banco {e}"
    finally:
        cursor.close()
        conn.close()