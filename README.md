Site para Aluguel de Carros

Este projeto é um sistema web de aluguel de carros desenvolvido com Flask, que permite aos usuários visualizar, reservar e gerenciar veículos disponíveis. O sistema possui funcionalidades de autenticação de usuários, gerenciamento de reservas e exibição de veículos com informações detalhadas.

Funcionalidades Principais:

Cadastro e Login de Usuários:
Os usuários podem se registrar com um nome de usuário, email e senha, além de fornecer um número de telefone.
Implementação de autenticação segura, incluindo a criptografia de senhas.

Exibição de Veículos:
Os veículos disponíveis são mostrados na página inicial, com três veículos selecionados aleatoriamente.
Os usuários podem filtrar a busca por modelo, marca, categoria, tipo de transmissão, tipo de veículo e capacidade de passageiros.

Gerenciamento de Reservas:
Os usuários podem selecionar um veículo e realizar uma reserva, especificando a data de início e a data de fim da locação.
O sistema valida as datas inseridas e calcula automaticamente o valor total da reserva com base no preço diário do veículo.

Confirmação e Cancelamento de Reservas:
Após a realização da reserva, uma página de confirmação exibe detalhes da locação, como datas e custo total.
Os usuários podem cancelar reservas existentes, que irão liberar o veículo para novas locações.

Painel do Usuário:
Os usuários têm acesso a um painel onde podem visualizar e gerenciar suas reservas, além de atualizar suas informações de perfil, como nome de usuário, email e telefone.

Administração de Veículos:
O sistema permite adicionar novos veículos ao banco de dados com informações detalhadas, como marca, modelo, categoria, tipo de transmissão, capacidade de passageiros e valor diário.

Tecnologias Usadas:
Python: Linguagem de programação principal para o desenvolvimento do backend.
Flask: Framework web utilizado para construir a aplicação.
SQLAlchemy: ORM (Object Relational Mapper) para gerenciamento de banco de dados.
SQLite: Banco de dados utilizado para armazenar informações de usuários, veículos e reservas.
Flask-Login: Gerenciamento de sessões de usuário para autenticação.
HTML/CSS: Para construção das interfaces de usuário.
