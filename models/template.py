"""
Modelo de Template para armazenamento em banco de dados.

Este módulo define a classe Template que representa um template
da Zenvia armazenado no banco de dados, contendo seu id, status
e motivo de rejeição, caso aplicável.
"""

from config.database import db
from datetime import datetime

class Template(db.Model):
    """
    Modelo de dados para templates da Zenvia.
    
    Esta classe define a estrutura da tabela 'templates' no banco de dados,
    armazenando informações sobre templates enviados para validação na Zenvia,
    incluindo seu status atual e possível motivo de rejeição.
    """
    
    __tablename__ = 'templates'
    
    id = db.Column(db.String(100), primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    motivo_rejeicao = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, template_id, status, motivo_rejeicao=""):
        """
        Inicializa um novo objeto Template.
        
        Args:
            template_id (str): ID único do template fornecido pela Zenvia.
            status (str): Status atual do template (ex: APPROVED, REJECTED, WAITING_APPROVAL).
            motivo_rejeicao (str, opcional): Motivo da rejeição do template, se aplicável.
        """
        self.id = template_id
        self.status = status
        self.motivo_rejeicao = motivo_rejeicao
    
    def to_dict(self):
        """
        Converte o objeto Template em um dicionário.
        
        Returns:
            dict: Dicionário contendo os atributos principais do template.
        """
        return {
            "id": self.id,
            "status": self.status,
            "motivo_rejeicao": self.motivo_rejeicao
        }