import sqlite3
import unicodedata

banco_dados = 'data/banco_dados_roxho.db'

# Função para remover acentos e caracteres especiais
def normalizar(texto: str) -> str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

# Função para gerar email
def gerar_email(nome_completo: str) -> str:
    if not nome_completo:
        return ""

    # Remove espaços extras e normaliza
    nome_completo = normalizar(nome_completo.strip())

    # Divide em palavras
    partes = nome_completo.split()
    if len(partes) < 2:
        return partes[0].lower() + "@roxho.com.br"

    primeiro_nome = partes[0].lower()
    ultimo_nome = partes[-1].lower()

    return f"{primeiro_nome}.{ultimo_nome}@roxho.com.br"

# Conectar ao banco
conn = sqlite3.connect(banco_dados)  # troque pelo nome do seu arquivo .db
cursor = conn.cursor()

# Buscar todos os nomes
cursor.execute("SELECT rowid, nome_completo FROM dados_funcionarios;")
linhas = cursor.fetchall()

# Atualizar emails
for rowid, nome in linhas:
    email = gerar_email(nome)
    cursor.execute(
        "UPDATE dados_funcionarios SET email_empresa = ? WHERE rowid = ?;",
        (email, rowid),
    )

# Salvar alterações
conn.commit()
conn.close()

print("✅ Emails gerados e salvos com sucesso!")
