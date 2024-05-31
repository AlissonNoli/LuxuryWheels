from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, date
import random
from flask_login import current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = '456'  # Chave secreta para usar o flash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/despi/OneDrive/Área de Trabalho/PROJETO FINAL/website_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Configuração do Flask-Login para carregar um usuário
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Criar o contexto da aplicação Flask
with app.app_context():
    # Criar as tabelas no banco de dados
    db.create_all()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    reservas = db.relationship('Reserva', backref='cliente', lazy=True)

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False


class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    transmissao = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    capacidade_pessoas = db.Column(db.Integer, nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    valor_diaria = db.Column(db.Float, nullable=False)
    ultima_revisao = db.Column(db.String)
    proxima_revisao = db.Column(db.String)
    ultima_inspecao = db.Column(db.String)
    disponivel = db.Column(db.Integer, default=1)
    reservas = db.relationship('Reserva', back_populates='veiculo', lazy=True)


class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey(
        'veiculo.id'), nullable=False)
    cliente_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    forma_pagamento_id = db.Column(db.Integer, db.ForeignKey(
        'forma_pagamento.id'), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    veiculo = db.relationship('Veiculo', back_populates='reservas', lazy=True)
    forma_pagamento = db.relationship(
        'FormaPagamento', backref='reservas')


class FormaPagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)


# Rota para a página inicial, exibindo três veículos disponíveis de forma aleatória
@app.route("/")
def index():
    # Consultar os veículos disponíveis
    veiculos_disponiveis = Veiculo.query.filter_by(disponivel=1).all()

    # Embaralhar a lista de veículos disponíveis
    random.shuffle(veiculos_disponiveis)

    # Selecionar os três primeiros veículos após a mistura
    veiculos_aleatorios = veiculos_disponiveis[:3]

    return render_template("index.html", veiculos=veiculos_aleatorios)


# Rota de registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        phone = request.form["phone"]

        # Verifica se a senha e a confirmação de senha são iguais
        if password != confirm_password:
            flash('As senhas não coincidem.', 'error')
            return render_template("register.html")

        # Verifica se já existe um usuário com o mesmo nome de usuário ou e-mail
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Nome de usuário ou e-mail já existe.', 'error')
            return render_template('register.html')

        # Cria um novo usuário com senha criptografada
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email,
                        password=hashed_password, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template("register.html")


# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Verifica as credenciais do usuário
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)  # Loga o usuário
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('perfil_cliente'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'error')

    return render_template('login.html')


# Rota para logout
@app.route("/logout")
@login_required
def logout():
    logout_user()  # Desloga o usuário
    flash('Logout bem-sucedido!', 'success')
    return redirect(url_for('index'))


# Rota para adicionar veiculos
@app.route("/adicionar_veiculo", methods=["GET", "POST"])
def adicionar_veiculo():
    if request.method == "POST":
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        categoria = request.form["categoria"]
        transmissao = request.form["transmissao"]
        tipo = request.form["tipo"]
        capacidade_pessoas = request.form["capacidade_pessoas"]
        imagem = request.form["imagem"]
        valor_diaria = request.form["valor_diaria"]
        ultima_revisao = request.form["ultima_revisao"]
        proxima_revisao = request.form["proxima_revisao"]
        ultima_inspecao = request.form["ultima_inspecao"]

        novo_veiculo = Veiculo(marca=marca, modelo=modelo, categoria=categoria, transmissao=transmissao,
                               tipo=tipo, capacidade_pessoas=capacidade_pessoas, imagem=imagem,
                               valor_diaria=valor_diaria, ultima_revisao=ultima_revisao,
                               proxima_revisao=proxima_revisao, ultima_inspecao=ultima_inspecao)

        db.session.add(novo_veiculo)
        db.session.commit()

        flash('Veículo adicionado com sucesso!', 'success')
        return redirect(url_for('veiculos'))

    return render_template("adicionar_veiculo.html")


ultima_revisao = datetime.strptime('2024-01-01', '%Y-%m-%d')
proxima_revisao = datetime.strptime('2024-07-01', '%Y-%m-%d')
ultima_inspecao = datetime.strptime('2023-12-01', '%Y-%m-%d')


# Rota para exibir os veículos disponíveis
@app.route("/veiculos", methods=["GET", "POST"])
def veiculos():
    if request.method == "POST":
        # Verifique se o botão de "Limpar Filtro" foi enviado
        if "reset_button" in request.form:
            # Redirecione para a mesma página para limpar o filtro
            return redirect(url_for('veiculos'))

        modelo_marca = request.form.get("modelo_marca")
        categoria = request.form.get("categoria")
        transmissao = request.form.get("transmissao")
        tipo = request.form.get("tipo")
        capacidade_pessoas = request.form.get("capacidade_pessoas")
        valor_diaria = request.form.get("valor_diaria")

        # Comece a consulta com todos os veículos disponíveis
        query = Veiculo.query.filter_by(disponivel=1)

        # Adicione condições para cada campo de seleção
        if modelo_marca:
            # Divida a entrada em modelo e marca
            termos_pesquisa = modelo_marca.split()
            modelos = []
            marcas = []
            for termo in termos_pesquisa:
                # Verifique se o termo é um modelo ou uma marca (ou ambos)
                modelos += Veiculo.query.filter(
                    Veiculo.modelo.ilike(f"%{termo}%")).all()
                marcas += Veiculo.query.filter(
                    Veiculo.marca.ilike(f"%{termo}%")).all()

            # Combine as listas de modelos e marcas sem duplicatas
            veiculos_encontrados = list(set(modelos + marcas))
            # Atualize a consulta para incluir apenas os veículos encontrados
            query = query.filter(Veiculo.id.in_(
                [veiculo.id for veiculo in veiculos_encontrados]))

        if categoria:
            query = query.filter(Veiculo.categoria == categoria)
        if transmissao:
            query = query.filter(Veiculo.transmissao.ilike(transmissao))
        if tipo:
            query = query.filter(Veiculo.tipo == tipo)
        if capacidade_pessoas:
            if capacidade_pessoas == "1-4":
                query = query.filter(Veiculo.capacidade_pessoas <= 4)
            elif capacidade_pessoas == "5-6":
                query = query.filter(Veiculo.capacidade_pessoas.between(5, 6))

        if valor_diaria:
            query = query.filter(Veiculo.valor_diaria <= float(valor_diaria))

        veiculos = query.all()
        return render_template("veiculos.html", veiculos=veiculos)

    # Consultar os veículos disponíveis
    veiculos_disponiveis = Veiculo.query.filter_by(disponivel=1).all()

    # Filtrar os veículos que passaram na inspeção há menos de 12 meses
    veiculos_filtrados = []
    for veiculo in veiculos_disponiveis:
        if veiculo.ultima_inspecao:
            ultima_inspecao = datetime.strptime(
                veiculo.ultima_inspecao, '%Y-%m-%d')
            if (datetime.now() - ultima_inspecao) <= timedelta(days=365):
                veiculos_filtrados.append(veiculo)

    return render_template("veiculos.html", veiculos=veiculos_filtrados)


@app.route("/veiculos/<int:veiculo_id>")
def detalhes_veiculo(veiculo_id):
    # Consulta o veículo com o ID fornecido
    veiculo = db.session.query(Veiculo).get(veiculo_id)

    # Consulta as formas de pagamento no banco de dados
    formas_pagamento = FormaPagamento.query.all()

    # Se o veículo existir, renderiza o template com os detalhes do veículo
    return render_template("detalhes_veiculo.html", veiculo=veiculo, formas_pagamento=formas_pagamento)


# Rota para processar a reserva
@app.route("/reservas/<int:veiculo_id>", methods=["POST"])
def processar_reserva(veiculo_id):
    if not current_user.is_authenticated:
        flash('Você precisa estar logado para fazer uma reserva.', 'error')
        return redirect(url_for('login'))

    veiculo = Veiculo.query.get_or_404(veiculo_id)

    if request.method == "POST":
        cliente_id = current_user.id
        data_inicio = datetime.strptime(
            request.form["data_inicio"], '%Y-%m-%d')
        data_fim = datetime.strptime(request.form["data_fim"], '%Y-%m-%d')
        forma_pagamento = request.form["forma_pagamento"]

        # Verificar se a data de início é anterior à data de fim
        if data_inicio >= data_fim:
            flash('A data de início deve ser anterior à data de término.', 'error')
            return redirect(url_for('index'))

        # Calcular a diferença em dias entre a data de início e a data de fim
        dias_reserva = (data_fim - data_inicio).days

        # Verificar se a data de início está no passado
        if data_inicio < datetime.now():
            flash('A data de início deve ser no futuro.', 'error')
            return redirect(url_for('index'))

        # Calcular o valor total da reserva
        valor_total = veiculo.valor_diaria * dias_reserva

        # Criar um objeto Reserva com os dados recebidos
        nova_reserva = Reserva(
            veiculo_id=veiculo.id,
            cliente_id=cliente_id,
            data_inicio=data_inicio,
            data_fim=data_fim,
            forma_pagamento_id=forma_pagamento,  # Corrigido para forma_pagamento_id
            valor_total=valor_total
        )

        # Define o veículo como indisponível
        veiculo.disponivel = 0

        try:
            # Adicionar a nova reserva ao banco de dados
            db.session.add(nova_reserva)
            db.session.commit()

            # Redirecionar para uma página de confirmação após a reserva ser concluída
            return redirect(url_for('confirmacao_reserva', reserva_id=nova_reserva.id))
        except Exception as e:
            # Em caso de erro, faça o rollback da transação
            db.session.rollback()
            flash(
                'Erro ao processar reserva. Por favor, tente novamente mais tarde.', 'error')
            app.logger.error(f"Erro ao processar reserva: {str(e)}")
            return redirect(url_for('index'))


# Rota para a página de confirmação de reserva
@app.route("/confirmacao_reserva/<int:reserva_id>")
@login_required
def confirmacao_reserva(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)
    dias_reserva = (reserva.data_fim - reserva.data_inicio).days
    return render_template("confirmacao_reserva.html", reserva=reserva, dias_reserva=dias_reserva)


# Rota para acessar o perfil
@app.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil_cliente():
    # Obter o cliente atualmente autenticado
    user = current_user

    # Consultar as reservas do cliente
    reservas = Reserva.query.filter_by(cliente_id=user.id).all()

    if request.method == "POST":
        # Obter os dados do formulário
        nova_data_inicio = request.form.get("nova_data_inicio")
        nova_data_fim = request.form.get("nova_data_fim")
        reserva_id = request.form.get("reserva_id")

        if nova_data_inicio and nova_data_fim and reserva_id:
            # Localizar a reserva pelo ID
            reserva = Reserva.query.get(reserva_id)

            # Converter as strings de data em objetos de data do Python
            nova_data_inicio = datetime.strptime(
                nova_data_inicio, "%Y-%m-%d").date()
            nova_data_fim = datetime.strptime(nova_data_fim, "%Y-%m-%d").date()

            # Verificar se as novas datas estão no futuro
            if nova_data_inicio < date.today() or nova_data_fim < date.today():
                flash('As datas de reserva não podem estar no passado.', 'error')
            # Verificar se a nova data de início é anterior à nova data de fim
            elif nova_data_inicio >= nova_data_fim:
                flash(
                    'A nova data de início deve ser anterior à nova data de término.', 'error')
            else:
                # Calcular a diferença em dias entre a nova data de início e a nova data de fim
                dias_reserva = (nova_data_fim - nova_data_inicio).days

                # Calcular o novo valor total da reserva
                novo_valor_total = reserva.veiculo.valor_diaria * dias_reserva

                # Atualizar as datas e o valor total da reserva
                reserva.data_inicio = nova_data_inicio
                reserva.data_fim = nova_data_fim
                reserva.valor_total = novo_valor_total

                # Commit das mudanças no banco de dados
                db.session.commit()

                # Flash de sucesso
                flash('As datas da reserva foram atualizadas com sucesso.', 'success')

        # Redirecionar para a página de perfil após a atualização
        return redirect(url_for("perfil_cliente"))

    # Se o método for GET, renderizar o template com as informações atuais do cliente e suas reservas
    return render_template("perfil.html", user=user, reservas=reservas)


# Rota para cancelar uma reserva
@app.route("/cancelar_reserva/<int:reserva_id>", methods=["POST"])
@login_required
def cancelar_reserva(reserva_id):
    # Obter a reserva a ser cancelada
    reserva = Reserva.query.get_or_404(reserva_id)

    # Verificar se o usuário atual é o dono da reserva
    if current_user.id != reserva.cliente_id:
        # Se não for, redirecionar para a página de perfil
        return redirect(url_for("perfil_cliente"))

    # Define o veículo associado à reserva como disponível
    veiculo = reserva.veiculo
    veiculo.disponivel = 1

    # Remover a reserva do banco de dados
    db.session.delete(reserva)
    db.session.commit()

    # Redirecionar de volta para a página de perfil
    return redirect(url_for("perfil_cliente"))


if __name__ == "__main__":
    app.run(debug=True)
