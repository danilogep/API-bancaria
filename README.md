# API Bancária Assíncrona com FastAPI e SQLModel

Este projeto é uma API RESTful assíncrona, construída com FastAPI, para gerenciar operações bancárias simples. A aplicação permite o cadastro de usuários, autenticação via JSON Web Tokens (JWT), e a realização de depósitos, saques e consulta de extratos.

Esta implementação utiliza **SQLModel** para unificar a definição de modelos de banco de dados e esquemas de validação da API, resultando em um código mais limpo, moderno e com menos duplicidade.

## ✨ Funcionalidades Principais

-   **Cadastro e Autenticação de Usuários:** Sistema seguro de criação de usuários e login com tokens JWT.
-   **Operações de Transação:** Endpoints para registrar depósitos e saques.
-   **Consulta de Extrato:** Endpoint para visualizar o saldo e o histórico de transações de uma conta.
-   **Operações Assíncronas:** Uso completo dos recursos `async`/`await` do Python para alta performance.
-   **Validação de Dados:** Regras de negócio implementadas para não permitir transações com valores negativos ou saques com saldo insuficiente.
-   **Documentação Automática:** Geração de documentação interativa da API com Swagger UI (`/docs`) e ReDoc (`/redoc`).

## 🛠️ Tecnologias Utilizadas

-   **Python 3.12+**
-   **FastAPI:** Framework web moderno e de alta performance para a construção da API.
-   **SQLModel:** Biblioteca que combina Pydantic e SQLAlchemy, usada para modelagem de dados, validação e interação com o banco.
-   **Uvicorn:** Servidor ASGI para executar a aplicação.
-   **Bcrypt:** Biblioteca usada diretamente para o hashing seguro de senhas.
-   **Python-JOSE:** Para a criação e verificação de JSON Web Tokens (JWT).
-   **Aiosqlite:** Driver de banco de dados para permitir operações assíncronas com o SQLite.
-   **Poetry:** Ferramenta para gerenciamento de dependências e ambientes virtuais.

## 📁 Estrutura do Projeto

O projeto é organizado de forma modular para promover a separação de responsabilidades: