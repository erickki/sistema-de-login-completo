from flask import Flask, redirect, url_for, render_template, request

from src.sistema_inicio_geral import verificar_login_sistema
from src.sistema_inicio_geral import verificar_registro_sistema

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/erro_no_login', methods=['POST'])
def erro_no_login():
    entrada_email = request.form.get('entrada_email')
    entrada_senha = request.form.get('entrada_senha')
    if entrada_email or entrada_senha:
        verificacao = verificar_login_sistema(entrada_email, entrada_senha)
        if verificacao == 'email não localizado':
            return render_template('login.html', erro='Email não localizado!')
        elif verificacao == 'senha valida':
            return redirect(url_for('login'))
        elif verificacao == 'senha incorreta':
            return render_template('login.html', erro='Senha incorreta!')
        elif verificacao == 'erro sistema login':
            return render_template('login.html', erro='Erro sistema: no login!')
        else:
            return render_template('login.html', erro='Erro sistema: na tela login!')
    else:
        return render_template('login.html', erro='Preencha todos os campos!')
    
@app.route('/esqueci-a-senha')
def esqueci_a_senha():
    return render_template('esqueci_a_senha.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/erro_no_registro', methods=['POST'])
def erro_no_registro():
    entrada_matricula = request.form.get('entrada_matricula')
    entrada_email = request.form.get('entrada_email')
    entrada_senha = request.form.get('entrada_senha')
    entrada_senha2 = request.form.get('entrada_senha2')
    if entrada_matricula or entrada_email or entrada_senha or entrada_senha2:
        if entrada_senha == entrada_senha2:
            verificacao = verificar_registro_sistema(entrada_matricula, entrada_email, entrada_senha)
            if verificacao == 'matricula não localizada':
                return render_template('registro.html', erro='Matrícula não localizada!')
            elif verificacao == 'email já cadastrado':
                return render_template('registro.html', erro='Email já cadastrado!')
            elif verificacao == 'registro feito':
                return redirect(url_for('login'))
            elif verificacao == 'erro sistema registro':
                return render_template('registro.html', erro='Erro sistema: no registro!')
            else:
                return render_template('registro.html', erro='Erro sistema: na tela registro!')
        else:
            return render_template('registro.html', erro='As senhas precisam ser iguais!')
    else:
        return render_template('registro.html', erro='Preencha todos os campos!')

if __name__ == '__main__':
    app.run(debug=True)