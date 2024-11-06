from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL  # Para a base de dados
import os, re
from werkzeug.utils import secure_filename
from collections import defaultdict


app = Flask(__name__)

# Configurações do MySQL usando variáveis de ambiente
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'restaurante_bd')

mysql = MySQL(app)  # Inicializa a extensão MySQL com as configurações do Flask

'''def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )'''

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cardapio')
def cardapio():
    try:
        cur = mysql.connection.cursor()
        
        # Consulta para produtos
        cur.execute("SELECT * FROM produtos")
        produtos = cur.fetchall()

        # Consulta para categorias
        cur.execute("SELECT * FROM categorias")
        categorias = cur.fetchall()

        # Dicionario de categorias
        categorias_dict = {categoria[0]: categoria[1] for categoria in categorias}
        ## Agrupar produtos por categoria
        produtos_por_categoria = defaultdict(list)
        for produto in produtos: produtos_por_categoria[produto[5]].append(produto)
        
        cur.close()
    except Exception as e:
        print(f"Erro ao aceder ao banco de dados: {e}")
        produtos = []
    
    return render_template('cardapio.html', categorias=categorias_dict, produtos=produtos, produtos_por_categoria=produtos_por_categoria)

@app.route('/admin')
def admin():
    try:
        cur = mysql.connection.cursor()

        # Consulta para categorias
        cur.execute("SELECT * FROM categorias")
        categorias = cur.fetchall()
        # Consulta para produtos
        cur.execute("SELECT * FROM produtos")
        produtos = cur.fetchall()
        # Consulta para contactos
        cur.execute("SELECT * FROM mensagens")
        mensagens = cur.fetchall()
        # Dicionario de categorias
        categorias_dict = {categoria[0]: categoria[1] for categoria in categorias}
        ## Agrupar produtos por categoria
        produtos_por_categoria = defaultdict(list)
        for produto in produtos: produtos_por_categoria[produto[5]].append(produto)
        
        cur.close()
    except Exception as e:
        print(f"Erro ao aceder ao banco de dados: {e}")
        produtos = []
    return render_template('admin.html', categorias=categorias_dict, produtos=produtos, produtos_por_categoria=produtos_por_categoria, mensagens=mensagens)

@app.route('/inserir_categoria', methods=['POST'])
def inserir_categoria():
    
    categoria_nome = request.form['categoria_nome']
    
    # Sanitizar o nome da categoria para o nome da tabela
    categoria_nome_sanitizado = re.sub(r'[^a-zA-Z0-9]', '_', categoria_nome.lower())
    
    # Verificar se o nome é reservado
    RESERVED_NAMES = [
        'select', 'insert', 'update', 'delete', 'drop', 'create', 'table', 'database', 'index', 'view', 'trigger', 'procedure', 'function'
    ]
    if categoria_nome_sanitizado in RESERVED_NAMES:
        return "Erro: Nome da categoria é reservado e não pode ser usado.", 400
    
    # Conectar ao banco de dados
    connection = mysql.connection
    cursor = connection.cursor()
    
    # Verificar se o nome da categoria já existe na tabela categorias
    cursor.execute("SELECT id FROM categorias WHERE nome = %s", (categoria_nome,))
    result = cursor.fetchone()
    if result:
        return "Erro: Nome da categoria indisponível.", 400
    
    # Inserir o nome da categoria na tabela categorias
    cursor.execute("INSERT INTO categorias (nome) VALUES (%s)", (categoria_nome,))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('admin'))

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
        id_categoria = request.form['categoria']
        
        # Imprime a categoria selecionada para depuração
        print(f"Categoria selecionada: {id_categoria}")
        
        # Valida e salva a imagem
        if imagem and imagem.filename != '':
            # Gera um nome seguro para o arquivo
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            # Se a imagem não estiver disponível ou inválida
            return "Erro: Imagem inválida.", 400

        # Conectar ao banco de dados
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO produtos (nome, descricao, preco, imagem, id_categoria)
            VALUES (%s, %s, %s, %s, %s)
        ''', (nome, descricao, preco, filename, id_categoria))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin'))  # Redireciona para a página de listagem após inserção
    except Exception as e:
        print(f"Erro ao inserir produto: {e}")
        return f"Erro ao inserir produto: {e}", 500

#FALTA DE CODIGO: @app.route('/alterar_produto/<int:id>', methods=['POST'])

@app.route('/delete_produto/<int:id>', methods=['POST'])
def delete_produtos(id):
    try:
        print(f"Tentando apagar prdutos com ID: {id}")
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM produtos WHERE id = %s', (id,))
        massa = cur.fetchone()
        if not massa:
            print("ID não encontrado.")
            return redirect(url_for('admin'))

        cur.execute('DELETE FROM produtos WHERE id = %s', (id,))
        mysql.connection.commit()
        print("Registro apagado com sucesso.")
        return redirect(url_for('admin'))
    except Exception as e:
        print(f"Erro ao apagar produto: {e}")
        return redirect(url_for('admin'))
    finally:
        cur.close()
    
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

@app.route('/tratar_mensagem/<int:id>', methods=['POST'])
def tratar_mensagem(id):
    try:
        # Conectar ao banco de dados
        cur = mysql.connection.cursor()
        
        # Verificar o estado atual da coluna 'tratado'
        cur.execute('SELECT tratado FROM mensagens WHERE id = %s', (id,))
        estado_atual = cur.fetchone()[0]
        
        # Alternar o valor de 'tratado'
        novo_estado = 1 if estado_atual is None else None
        
        # Atualizar a coluna 'tratado'
        cur.execute('''
            UPDATE mensagens
            SET tratado = %s
            WHERE id = %s
        ''', (novo_estado, id))
        
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin'))  # Redireciona para a página de listagem de mensagens
    except Exception as e:
        print(f"Erro ao tratar mensagem: {e}")
        return f"Erro ao tratar mensagem: {e}", 500

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
