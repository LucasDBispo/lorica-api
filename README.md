# Lorica Vehicle Management / Gestão Veicular

## EN-US

### Overview
Lorica is a vehicle management tool designed to help users control expenses related to vehicle ownership. In Brazil, vehicles are the second largest source of family expenses, and Lorica aims to simplify tracking fuel, maintenance, taxes, and other costs.

**This repository contains only the backend API.** 

Live API: [https://lorica-api-1.onrender.com/](https://lorica-api-1.onrender.com/)

### Technologies
* Python 3.13
* FastAPI
* SQLAlchemy & PostgreSQL
* Docker & Docker Compose
* JWT Authentication with OAuth2

### How to Run
The easiest way to run the project is using Docker:
```bash
docker compose up --build
```
Access the API at: `http://localhost:8000/` (Swagger docs are at the root).

---

## PT-BR 

### Visão Geral 
Antes de tudo, vamos falar sobre o contexto do projeto. No Brasil, veículos são bens bastante populares e representam a segunda maior fonte de gastos no orçamento das famílias (Serasa, 2024). O Lorica surge como uma ferramenta de auxílio para o gerenciamento de despesas como abastecimento, manutenção, taxas e financiamentos.

**Neste repositório você encontrará apenas o backend do projeto**. 
Acesse a versão em produção: [https://lorica-api-1.onrender.com/](https://lorica-api-1.onrender.com/)

### Funcionalidades 
* Cadastro de Usuário e Veículos
* Registro de Despesas:
    * Abastecimento e Recarga 
    * Taxas Governamentais (IPVA, Licenciamento)
    * Oficina e Consertos 
    * Financiamentos e Parcelas
    * Estacionamento e Pedágio

### Tecnologias empregadas
* Python 3.13 (uv / pyproject.toml)
* FastAPI
* SQLAlchemy (PostgreSQL)
* Docker & Docker Compose
* Autenticação JWT com OAuth2

### Como executar 

#### **1. Execução via Docker (Recomendado)** 
Na pasta raiz do projeto, execute: 
```bash
docker compose up --build 
```
Acesse a API em: `http://localhost:8000/`

#### **2. Execução Local (Desenvolvimento)** 
Para rodar a API fora do container (instalando as dependências na sua máquina), siga os passos:

**Requisitos:** 
* Python 3.13+
* Docker (apenas para o banco de dados)

1. **Inicie o banco de dados:**
   ```bash
   docker compose up -d postgres
   ```
   *Nota: O banco de dados estará disponível na porta `5433` do seu localhost.*

2. **Prepare o ambiente:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` baseado no `.env.example`. Certifique-se de que a `DATABASE_URL` aponta para `localhost:5433`.

4. **Inicialize o banco (Migrations/Seed):**
   ```bash
   python -m app.core.db.init_db
   python -m app.core.db.seed
   ```

5. **Execute a aplicação:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Documentação da API
* **Swagger UI (Docs):** [http://localhost:8000/](http://localhost:8000/)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)






