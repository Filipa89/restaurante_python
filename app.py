from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL  # Para a base de dados
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Configurações do MySQL usando variáveis de ambiente
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'restaurante_bd')

mysql = MySQL(app)  # Inicializa a extensão MySQL com as configurações do Flask

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cardapio')
def cardapio():
    try:
        cur = mysql.connection.cursor()
        
        # Consulta para pizzas
        cur.execute("SELECT * FROM pizzas")
        pizzas = cur.fetchall()
        
        # Consulta para massas
        cur.execute("SELECT * FROM massas")
        massas = cur.fetchall()
        
        cur.close()
    except Exception as e:
        print(f"Erro ao aceder ao banco de dados: {e}")
        pizzas = []
        massas = []
    
    return render_template('cardapio.html', pizzas=pizzas, massas=massas)


    '''
    # Definindo os itens do cardápio
    cardapio_items = [
        {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
          {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
          {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
          {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
          {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
          {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
          {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
          {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
          {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
          {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
          {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
          {
            'nome': 'Spaghetti à Carbonara',
            'descricao': 'Spaghetti com molho de creme, bacon crocante e queijo parmesão.',
            'preco': 'R$ 35,00'
        },
        {
            'nome': 'Salada Caesar',
            'descricao': 'Alface romana, croutons, queijo parmesão e molho Caesar.',
            'preco': 'R$ 25,00'
        },
        {
            'nome': 'Risoto de Funghi',
            'descricao': 'Risoto cremoso com cogumelos funghi e queijo parmesão.',
            'preco': 'R$ 40,00'
        },
        
        # Adicione mais itens conforme necessário
    ]
    return render_template('cardapio.html', items=cardapio_items)
'''

@app.route('/admin')
def admin():
    try:
        cur = mysql.connection.cursor()
        # Consulta para pizzas
        cur.execute("SELECT * FROM pizzas")
        pizzas = cur.fetchall()
        # Consulta para massas
        cur.execute("SELECT * FROM massas")
        massas = cur.fetchall()    
        cur.close()
    except Exception as e:
        print(f"Erro ao aceder ao banco de dados: {e}")
        pizzas = []
        massas = []
    return render_template('admin.html', pizzas=pizzas, massas=massas)

@app.route('/delete_massa/<int:id>', methods=['POST'])
def delete_massa(id):
    try:
        print(f"Tentando apagar massa com ID: {id}")
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM massas WHERE id = %s', (id,))
        massa = cur.fetchone()
        if not massa:
            print("ID não encontrado.")
            return redirect(url_for('admin'))

        cur.execute('DELETE FROM massas WHERE id = %s', (id,))
        mysql.connection.commit()
        print("Registro apagado com sucesso.")
        return redirect(url_for('admin'))
    except Exception as e:
        print(f"Erro ao apagar massa: {e}")
        return redirect(url_for('admin'))
    finally:
        cur.close()

# Define o caminho da pasta onde as imagens serão salvas
UPLOAD_FOLDER = 'static/imgs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/inserir_produto', methods=['POST'])
def inserir_produto():
    try:
        # Captura os dados do formulário
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        imagem = request.files['imagem']
        
        # Valida e salva a imagem
        if imagem and imagem.filename != '':
            # Gera um nome seguro para o arquivo
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            # Se a imagem não estiver disponível ou inválida
            return "Erro: Imagem inválida.", 400

        # Salva o produto no banco de dados com o nome do arquivo da imagem
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO massas (nome, descricao, preco, imagem)
            VALUES (%s, %s, %s, %s)
        ''', (nome, descricao, preco, filename))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin'))  # Redireciona para a página de listagem após inserção
    except Exception as e:
        print(f"Erro ao inserir produto: {e}")
        return "Erro ao inserir produto.", 500
    
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']
        # Lógica para processar o formulário
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO mensagens (nome, email, mensagem)
            VALUES (%s, %s, %s)
        ''', (nome, email, mensagem))
        mysql.connection.commit()
        cur.close()
        # Redirecionamento após o envio do formulário
        return render_template('obrigado.html', nome=nome)
    return render_template('contacto.html')

@app.route('/reservas', methods=['GET', 'POST'])
def reservas():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        data = request.form['data']
        horario = request.form['horario']
        pessoas = request.form['pessoas']
        # Aqui você pode adicionar a lógica para processar a reserva, como salvar em um banco de dados
        return render_template('reserva_confirmada.html', nome=nome)
    return render_template('reservas.html')

@app.route('/galeria')
def galeria():
    galeria_fotos = [
        {'url': 'images/chef.jpg', 'descricao': 'Chef Cintia'},
        {'url': 'images/carbonara.jpg', 'descricao': 'Prato de Spaghetti à Carbonara'},
        {'url': 'images/entardecer.jpg', 'descricao': 'Ambiente ao Entardecer'},
        # Adicione mais fotos conforme necessário
    ]
    return render_template('galeria.html', fotos=galeria_fotos)

if __name__ == '__main__':
    app.run(debug=True)
