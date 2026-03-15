Uma API RESTful construída para gerenciamento de clientes (CRM) com foco em performance, validação estrita de dados e otimização de banco de dados relacional.

## Arquitetura e Decisões Técnicas

Este projeto foi desenvolvido para suportar testes de estresse com alto volume de dados, implementando táticas de engenharia para evitar gargalos de I/O (disco) e estouro de memória RAM:

* **Validação de Contratos:** Uso agressivo do Pydantic para garantir que nenhum dado malformado (e-mails inválidos, telefones fora do padrão E.164) alcance o banco de dados.
* **Otimização de Busca (B-Tree):** Indexação de colunas críticas no SQLite, eliminando varreduras completas de tabela (*Full Table Scans*) e reduzindo o tempo de resposta de `~6.0s` para `< 0.001s` em buscas não-exatas em uma base de 30.000 registros.
* **Paginação de Dados:** Implementação cirúrgica de `LIMIT` e `OFFSET` direto na query SQL para garantir um payload de rede previsível e proteger o servidor contra requisições massivas.
* **Seeding Massivo:** Script de carga integrado utilizando `executemany` para injeção otimizada de dezenas de milhares de registros em uma única transação de disco, evitando loop de I/O.

## Stack Tecnológico
* **Linguagem:** Python
* **Framework Web:** FastAPI
* **Banco de Dados:** SQLite (Nativo)
* **Validação de Dados:** Pydantic
* **Servidor ASGI:** Uvicorn
* **Geração de Dados (Stress Test):** Faker

## Como Executar Localmente

1. Clone este repositório:
```bash
git clone https://github.com/Bernarr-77/cadastro_leads.git
cd cadastro_leads
# Crie um ambiente virtual:

python -m venv venv

# No Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate

#Instale as dependências do ecossistema:
pip install fastapi[standart] pydantic[email] pydantic-extra-types phonenumbers faker

#Inicialize a infraestrutura do banco de dados (Criação da tabela e do arquivo leads.db):
python api/database.py

#Execute o script de seeding massivo para injetar 30.000 leads fictícios no banco e testar a performance de paginação e indexação:
python seed.py

#Navegue para a pasta da API e inicie o servidor ASGI:
cd api
fastapi dev main.py

#Acesse a documentação interativa (Swagger UI) para testar as rotas:
http://localhost:8000/docs
