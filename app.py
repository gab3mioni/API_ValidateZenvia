"""
Aplicação Flask para validação e gerenciamento de templates Zenvia.

Este módulo serve como ponto de entrada para a API de Validação de Templates Zenvia.
Ele inicializa a aplicação Flask, configura a conexão com o banco de dados,
configura serviços e registra os blueprints de rotas.

A aplicação fornece endpoints para:
- Enviar templates para validação na Zenvia
- Monitorar o status de aprovação dos templates
- Exportar dados dos templates para arquivos CSV
"""

from flask import Flask
from routes.template_routes import template_routes
from routes.export_routes import export_routes
from config.database import init_db
from services.zenvia_service import init_service

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Inicializa a conexão com o banco de dados e cria tabelas se não existirem
init_db(app)

# Inicializa o serviço Zenvia com o contexto da aplicação
init_service(app)

# Registra os blueprints de rotas
app.register_blueprint(template_routes)
app.register_blueprint(export_routes)

if __name__ == "__main__":
    """
    Executa a aplicação quando executada diretamente.
    
    A aplicação é executada na porta 5000 com o modo de depuração ativado.
    O modo de depuração deve ser desativado em ambientes de produção.
    """
    app.run(port=5000, debug=True)