import sqlite3
import random
from plyer import notification

banco_dados = 'data/banco_dados_roxho.db'

def fazer_login(entrada_email, entrada_senha):
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT senha FROM usuarios_sistema_roxho WHERE email = ?", (entrada_email,)
        )
        resultado_senha = cursor.fetchone()
        if resultado_senha[0] == entrada_senha:
            return 'pode logar'
        else:
            return 'senha incorreta'
    except:
        return 'email não localizado'
    finally:
        conn.close()

def fazer_esqueci_senha(entrada_nome, entrada_email):
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT nome FROM usuarios_sistema_roxho WHERE email = ?",(entrada_email,)
        )
        resultao_nome = cursor.fetchone()
        if resultao_nome[0] == entrada_nome:
            codigo_gerado = random.randint(100000, 999999)
            cursor.execute(
                "UPDATE usuarios_sistema_roxho SET codigo_recuperacao = ? WHERE email = ?",(codigo_gerado, entrada_email)
            )
            conn.commit()
            conn.close()
            notification.notify(
                title="Código de Recuperação",
                message=f"Seu código é {codigo_gerado}",
                timeout=10
            )
            return 'codigo gerado'
        else:
            return 'nome incorreto'
    except:
        return 'email não localizado'
    finally:
        conn.close()

def fazer_resetar_senha(entrada_email, entrada_senha, entrada_codigo):
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT codigo_recuperacao FROM usuarios_sistema_roxho WHERE email = ?",(entrada_email,)
        )
        resultado_codigo = cursor.fetchone()
        if resultado_codigo[0] == entrada_codigo:
            retirar_codigo = ''
            cursor.execute(
                "UPDATE usuarios_sistema_roxho SET senha = ?, codigo_recuperacao = ? WHERE email = ?",(entrada_senha, retirar_codigo, entrada_email)
            )
            conn.commit()
            conn.close()
            return 'senha alterada'
        else:
            return 'codigo incorreto'
    except:
        return 'email não localizado'
    finally:
        conn.close()

def fazer_registro(entrada_nome, entrada_email, entrada_senha):
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT email FROM usuarios_sistema_roxho WHERE email = ?",(entrada_email,)
    )
    resultao_email = cursor.fetchone()
    if resultao_email:
        return 'email já cadastrado'
    else:
        cursor.execute(
            "INSERT INTO usuarios_sistema_roxho (nome, email, senha) VALUES (?, ?, ?)",(entrada_nome, entrada_email, entrada_senha)
        )
        conn.commit()
        conn.close()
        return 'registrado'