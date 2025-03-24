"""
Módulo de configurações da API Zenvia.

Este módulo carrega variáveis de ambiente e define constantes relacionadas
à integração com a API Zenvia para validação de templates.
As credenciais são carregadas de um arquivo .env usando python-dotenv.
"""

import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env para o ambiente
load_dotenv()

# URL base da API Zenvia para templates
ZENVIA_URL = "https://api.zenvia.com/v2/templates"

# Token de autenticação para a API Zenvia (carregado de variável de ambiente)
ZENVIA_TOKEN = os.getenv("ZENVIA_TOKEN")

# Número de telefone utilizado como remetente nas mensagens
SENDER_PHONE = os.getenv("SENDER_PHONE")

# Email utilizado para receber atualizações sobre o status do template
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

# Cabeçalhos padrão para requisições à API Zenvia
HEADERS = {
    "Content-Type": "application/json",
    "X-API-TOKEN": ZENVIA_TOKEN
}