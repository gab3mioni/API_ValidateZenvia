# API de Validação de Templates Zenvia

## Tecnologias Utilizadas
- **Linguagem:** Python 3.11
- **Framework Web:** Flask 2.2.3
- **Banco de Dados:** SQLite 3.45.1
- **ORM:** Flask-SQLAlchemy 3.0.3
- **Bibliotecas Adicionais:**
    - requests 2.28.2 (cliente HTTP)
    - python-dotenv 1.0.0 (carregamento de variáveis de ambiente)
    
## Visão Geral

Esta aplicação oferece uma API para integração com a plataforma Zenvia, permitindo o envio de templates de mensagens para validação, monitoramento automático de status de aprovação e exportação de relatórios em formato CSV.

## Configuração e Instalação

Pré-requisitos
- Python 3.11 ou superior
- Pip (gerenciador de pacotes Python)
- Git


1. Clone o Repositório localmente
```bash
git clone https://github.com/gab3mioni/API_ValidateZenvia.git
cd API_ValidateZenvia
```

2. Criando e Ativando Ambiente Virtual

É recomendado utilizar um ambiente virtual para isolar as dependências do projeto:

```bash
# Criando o ambiente virtual
python -m venv venv

# Ativando o ambiente virtual
# No Windows:
venv\Scripts\activate

# No Linux/macOS:
source venv/bin/activate
```

Após ativar o ambiente virtual, você verá o nome dele no início do prompt de comando, indicando que está ativo.

3. Instale as dependências

Com o ambiente virtual ativado, instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente

Execute o comando no terminal

```bash
cp .env.example .env
```

Edite o arquivo .env com suas credenciais da Zenvia:

```markdown
ZENVIA_TOKEN=seu_token_da_zenvia
SENDER_PHONE=seu_telefone_remetente
SENDER_EMAIL=seu_email
CHANNEL=WHATSAPP
```

5. Execute a API

Certifique-se de que o ambiente virtual está ativado e execute:

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`.

## Estrutura do Projeto

```markdown
API_ValidateZenvia/
├── app.py                  # Ponto de entrada da aplicação
├── config/                 
│   ├── database.py         # Configuração do banco de dados
│   └── settings.py         # Configurações da API Zenvia
├── models/                 
│   └── template.py         # Modelo de Template
├── routes/                 # Rotas da API
│   └── template_routes.py  # Rota para envio de templates
├── services/               
│   └── zenvia_service.py   # Integração com a API Zenvia
├── utils/                 
│   └── helpers.py          # Funções auxiliares
├── csv_output/             # Diretório para arquivos CSV exportados
├── venv/                   # Ambiente virtual (não versionado)
└── instance/               # Diretório do banco de dados SQLite
    └── templates.db        # Banco de dados SQLite
```

## Endpoints

Enviar template para validação

- URL: `/enviar-template`
- Método: POST
- Corpo da requisição:
```json
{
  "name": "nome_do_template",
  "text": "Conteúdo do template com {{variaveis}} se necessário"
}
```

- Resposta de sucesso:

```json
{
  "id": "template_id",
  "status": "WAITING_APPROVAL",
  "motivo_rejeicao": ""
}
```

## Testando a aplicação

Enviando um Template para Validação

Usando `curl`:

```curl -X POST http://localhost:5000/enviar-template \
  -H "Content-Type: application/json" \
  -d '{"name":"template_teste","text":"Este é um template de teste com {{variavel}}."}
  ```

Ou usando ferramentas como Postman/Insomnia para enviar o JSON ao endpoint.

## Verificando o BBanco de Dados

O SQLite não requer configuração adicional. Para explorar o banco de dados:

```bash
sqlite3 instance/templates.db
sqlite> SELECT * FROM templates;
```