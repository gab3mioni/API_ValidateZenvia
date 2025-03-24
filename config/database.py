"""
Módulo de configuração do banco de dados.

Este módulo configura a conexão com o banco de dados SQLite usando SQLAlchemy.
Ele define o objeto de banco de dados global e fornece funções para inicializar
a conexão com o banco de dados na aplicação Flask.
"""

from flask_sqlalchemy import SQLAlchemy

# Objeto SQLAlchemy global para interação com o banco de dados
db = SQLAlchemy()

def init_db(app):
    """
    Inicializa a conexão com o banco de dados para a aplicação Flask.
    
    Esta função configura o SQLAlchemy para usar um banco de dados SQLite,
    desativa o rastreamento de modificações e cria as tabelas definidas
    nos modelos, caso ainda não existam.
    
    Args:
        app: Instância da aplicação Flask para configurar.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///templates.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()