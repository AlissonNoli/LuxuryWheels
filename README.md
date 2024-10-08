# Site para Aluguel de Carros

Este projeto é um sistema web de aluguel de carros desenvolvido com **Flask**, que permite aos usuários visualizar, reservar e gerenciar veículos disponíveis para locação. O sistema oferece uma interface intuitiva e segura, com autenticação de usuários, gerenciamento de reservas e exibição detalhada de veículos.

## Funcionalidades Principais

- **Cadastro e Login de Usuários:**
  - Os usuários podem se registrar com nome de usuário, email, senha e número de telefone.
  - Autenticação segura com criptografia de senhas.

- **Exibição de Veículos:**
  - A página inicial exibe três veículos aleatórios.
  - Filtros disponíveis por modelo, marca, categoria, tipo de transmissão, tipo de veículo e capacidade de passageiros.

- **Gerenciamento de Reservas:**
  - Usuários podem reservar veículos, especificando a data de início e fim da locação.
  - Validação automática das datas e cálculo do valor total da reserva com base no preço diário do veículo.

- **Confirmação e Cancelamento de Reservas:**
  - Após reservar, os detalhes da locação são exibidos, incluindo datas e custo total.
  - Os usuários podem cancelar reservas, liberando o veículo para novas locações.

- **Painel do Usuário:**
  - Acesso a um painel para gerenciar reservas e atualizar informações de perfil (nome, email e telefone).

- **Administração de Veículos:**
  - Permite adicionar novos veículos ao banco de dados, com informações detalhadas como marca, modelo, categoria, tipo de transmissão, capacidade de passageiros e preço diário.

## Tecnologias Usadas

- **Python:** Desenvolvimento do backend.
- **Flask:** Framework web utilizado para a construção da aplicação.
- **SQLAlchemy:** ORM (Object Relational Mapper) para gerenciamento do banco de dados.
- **SQLite:** Banco de dados utilizado para armazenar informações de usuários, veículos e reservas.
- **Flask-Login:** Gerenciamento de sessões de usuário para autenticação.
- **HTML/CSS:** Construção das interfaces de usuário.
