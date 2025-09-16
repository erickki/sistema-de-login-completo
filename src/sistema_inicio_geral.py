import sqlite3

banco_dados = 'data/banco_dados_roxho.db'

def verificar_login_sistema(entrada_email, entrada_senha):
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'SELECT senha_sistema FROM contas_sistema WHERE email_empresa = ?', (entrada_email,)
        )
        resultado_senha = cursor.fetchone()
        if not resultado_senha:
            return 'email não localizado'
        else:
            if entrada_senha == resultado_senha[0]:
                return 'senha valida'
            else:
                return 'senha incorreta'
    except:
        return 'erro sistema login'
    finally:
        conn.close

def verificar_registro_sistema(entrada_matricula, entrada_email, entrada_senha):
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'SELECT matricula FROM dados_funcionarios WHERE matricula = ?', (entrada_matricula,)
        )
        resultado_matricula = cursor.fetchone()
        if not resultado_matricula:
            return 'matricula não localizada'
        else:
            cursor.execute(
                'SELECT senha_sistema FROM contas_sistema WHERE email_empresa = ?', (entrada_email,)
            )
            resultado_senha = cursor.fetchone()
            if resultado_senha:
                return 'email já cadastrado'
            else:
                cursor.execute(
                    'SELECT id_funcionario, nome_completo FROM dados_funcionarios WHERE matricula = ?', (entrada_matricula,)
                )
                resultado_id_nome = cursor.fetchone()
                cursor.execute(
                    'INSERT INTO contas_sistema (id_funcionario, nome_completo, matricula, email_empresa, senha_sistema) VALUES (?, ?, ?, ?, ?)', (resultado_id_nome[0], resultado_id_nome[1], entrada_matricula, entrada_email, entrada_senha)
                )
                conn.commit()
                return 'registro feito'
    except:
        return 'erro sistema registro'
    finally:
        conn.close