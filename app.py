import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Em app encontra-se o nosso servidor web de Flask
app = Flask(__name__)
# Armazena a informação do PATH do projeto de acordo com o sistema utilizado
diretorio_base = os.path.abspath(os.path.dirname(__file__))
# Insere o caminho correto na URI segundo o direório base
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(diretorio_base, 'database/tarefas.db')
# Cursor para a base de dados SQLite
db = SQLAlchemy(app)


class Tarefa(db.Model):
    __tablename__ = "tarefas"
    # Identificador único de cada tarefa (não pode haver duas tarefas com o mesmo id, por isso é primary key)
    id = db.Column(db.Integer, primary_key=True)
    # Conteúdo da tarefa, um texto de máximo 200 caracteres
    conteúdo = db.Column(db.String(200))
    # Booleano que indica se uma tarefa foi feita ou não
    feita = db.Column(db.Boolean)


with app.app_context():
    # Criação das tabelas
    db.create_all()
    # Execução das tarefas pendentes da base de dados
    db.session.commit()


# A barra (o slash) conhece-se como a página de início (página home).
# Vamos definir para esta rota, o comportamento a seguir.
@app.route('/')
def home():
    # Consultamos e armazenamos todas as tarefas da base de dados
    todas_as_tarefas = Tarefa.query.all()
    # Agora na variável todas_as_tarefas estão armazenadas todas as tarefas. Vamos entregar esta variável ao template index.html
    return render_template("index.html", lista_de_tarefas=todas_as_tarefas)  # Carrega - se o template index.html


@app.route('/criar-tarefa', methods=['POST'])
def criar():
    # tarefa é um objeto da classe Tarefa (uma instância da classe)
    # id não é necessário atribuí-lo manualmente, porque a primary key gera-se automaticamente
    tarefa = Tarefa(conteúdo=request.form['conteúdo_tarefa'], feita=False)
    # Adicionar o objeto da Tarefa à base de dados
    db.session.add(tarefa)
    # Executar a operação pendente da base de dados
    db.session.commit()
    # Redireciona-nos à função home()
    return redirect(url_for('home'))


@app.route('/eliminar-tarefa/<id>')
def eliminar(id):
    # Pesquisa-se dentro da base de dados, aquele registro cujo id coincida com o proporcionado pelo parâmetro da rota. Quando se encontrar elimina-se
    tarefa = Tarefa.query.filter_by(id=int(id)).delete()
    # Executar a operação pendente da base de dados
    db.session.commit()
    # Redireciona-nos à função home() e se tudo correu bem, ao atualizar, a tarefa eliminada não vai aparecer na listagem
    return redirect(url_for('home'))


@app.route('/tarefa-feita/<id>')
def feita(id):
    # Obtém-se a tarefa que se procura
    tarefa = Tarefa.query.filter_by(id=int(id)).first()
    # Guardar na variável booleana da tarefa, o seu contrário
    tarefa.feita = not (tarefa.feita)
    # Executar a operação pendente da base de dados
    db.session.commit()
    # Redireciona-nos para a função home()
    return redirect(url_for('home'))


@app.route('/limpar', methods=['POST'])
def limpar():
    # Limpa todas as informações na base de dados
    db.drop_all()
    # Criação das tabelas novamente
    db.create_all()
    # Executar a operação pendente da base de dados
    db.session.commit()
    # Redireciona-nos à função home() e se tudo correu bem, ao atualizar, a tarefa eliminada não vai aparecer na listagem
    return redirect(url_for('home'))


if __name__ == '__main__':
    # O debug=True faz com que cada vez que reiniciemos o servidor ou modifiquemos o código,
    # o servidor de Flask reinicia-se sozinho
    app.run(debug=True)
