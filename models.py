from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/despi/OneDrive/Área de Trabalho/PROJETO FINAL/website_db.db'
db = SQLAlchemy(app)


ultima_revisao = datetime.strptime('2024-01-01', '%Y-%m-%d')
proxima_revisao = datetime.strptime('2024-07-01', '%Y-%m-%d')
ultima_inspecao = datetime.strptime('2023-12-01', '%Y-%m-%d')


class Veiculo(db.Model):
    __tablename__ = 'veiculo'
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String)
    modelo = db.Column(db.String)
    categoria = db.Column(db.String)
    transmissao = db.Column(db.String)
    tipo = db.Column(db.String)
    capacidade_pessoas = db.Column(db.Integer)
    imagem = db.Column(db.String)
    valor_diaria = db.Column(db.Float)
    ultima_revisao = db.Column(db.String)
    proxima_revisao = db.Column(db.String)
    ultima_inspecao = db.Column(db.String)


# Adicione o código para adicionar veículos dentro do contexto da aplicação Flask
with app.app_context():
    # Crie um novo veículo
    novo_veiculo = Veiculo(
        marca='Marca3',
        modelo='Modelo3',
        categoria='Categoria3',
        transmissao='Transmissao3',
        tipo='Tipo3',
        capacidade_pessoas=5,
        imagem='https://th.bing.com/th/id/R.0381713662a29f8d2ab63c600369fa5a?rik=LvFj9i6ZannmLg&riu=http%3a%2f%2frotanews176.com.br%2fwp-content%2fuploads%2f2021%2f03%2f1-195.jpg&ehk=6TBMQYrfC4wNs1505w%2b%2foa8i1xcqTACHaTs1NqcUhus%3d&risl=&pid=ImgRaw&r=0',
        valor_diaria=100.00,
        ultima_revisao='2024-01-01',
        proxima_revisao='2024-07-01',
        ultima_inspecao='2023-12-01'
    )

# Adicione o veículo ao banco de dados
    db.session.add(novo_veiculo)
    db.session.commit()
