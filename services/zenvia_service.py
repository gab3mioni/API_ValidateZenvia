"""
Serviço de integração com a API Zenvia.

Este módulo contém funções para enviar templates para validação na API Zenvia,
monitorar o status de aprovação desses templates e atualizar o banco de dados
com as informações recebidas. Inclui suporte para monitoramento assíncrono
usando threads.
"""

import time
import requests
from threading import Thread, Lock
from config.settings import ZENVIA_URL, HEADERS
from models.template import Template
from config.database import db

# Mutex para sincronização de acesso ao banco de dados em múltiplas threads
lock = Lock()
# Referência à aplicação Flask para uso em threads de monitoramento
app = None

def init_service(flask_app):
    """
    Inicializa o serviço Zenvia com a instância da aplicação Flask.
    
    Esta função armazena uma referência global à aplicação Flask, necessária
    para criar contextos de aplicação em threads de monitoramento.
    
    Args:
        flask_app: Instância da aplicação Flask.
    """
    global app
    app = flask_app

def enviar_template(template_data):
    """
    Envia um template para validação na API Zenvia.
    
    Esta função envia os dados do template para a API Zenvia, processa a resposta,
    armazena as informações no banco de dados e inicia uma thread de monitoramento
    caso o template esteja aguardando aprovação.
    
    Args:
        template_data (dict): Dicionário contendo os dados do template a ser enviado.
        
    Returns:
        tuple: Uma tupla contendo três elementos:
            - dict ou None: Dicionário com os dados do template em caso de sucesso, None em caso de erro.
            - int: Código de status HTTP da resposta.
            - dict ou None: Detalhes do erro em caso de falha, None em caso de sucesso.
    """
    response = requests.post(ZENVIA_URL, json=template_data, headers=HEADERS)
    if not response.ok:
        return None, response.status_code, response.json()
    
    resposta = response.json()
    motivo_rejeicao = ""
    if resposta.get("status") == "REJECTED" and resposta.get("comments"):
        comments = resposta.get("comments", [])
        if comments and len(comments) > 0:
            # Pega o último comentário (normalmente contém a razão da rejeição ou aprovação)
            ultimo_comentario = comments[-1]
            if isinstance(ultimo_comentario, dict) and "text" in ultimo_comentario:
                motivo_rejeicao = ultimo_comentario["text"]
            elif isinstance(ultimo_comentario, str):
                motivo_rejeicao = ultimo_comentario
    
    novo_template = Template(
        template_id=resposta["id"],
        status=resposta["status"],
        motivo_rejeicao=motivo_rejeicao
    )

    with lock:
        db.session.add(novo_template)
        db.session.commit()

    if novo_template.status == "WAITING_APPROVAL":
        Thread(target=monitorar_status, args=(novo_template.id,)).start()

    return novo_template.to_dict(), 200, None

def monitorar_status(template_id):
    """
    Monitora o status de um template enviado para a Zenvia.
    
    Esta função executa em uma thread separada e consulta periodicamente
    o status do template na API Zenvia. Quando o status muda, atualiza o
    registro correspondente no banco de dados. A thread termina quando o
    template atinge um estado final (aprovado ou rejeitado).
    
    Args:
        template_id (str): ID do template a ser monitorado.
    """
    global app
    if not app:
        return
        
    with app.app_context():
        while True:
            time.sleep(30)
            url = f"{ZENVIA_URL}/{template_id}"
            response = requests.get(url, headers=HEADERS)

            if response.status_code != 200:
                continue

            status = response.json()["status"]
            comments = response.json().get("comments", [])
            motivo_rejeicao = ""
            
            if response.json().get("status") == "REJECTED" and response.json().get("comments"):
                comments = response.json().get("comments", [])
                if comments and len(comments) > 0:
                    # Pega o último comentário (normalmente contém a razão da rejeição)
                    ultimo_comentario = comments[-1]
                    if isinstance(ultimo_comentario, dict) and "text" in ultimo_comentario:
                        motivo_rejeicao = ultimo_comentario["text"]
                    elif isinstance(ultimo_comentario, str):
                        motivo_rejeicao = ultimo_comentario

            with lock:
                template = Template.query.get(template_id)
                if template:
                    template.status = status
                    if status == "REJECTED":
                        template.motivo_rejeicao = motivo_rejeicao
                    db.session.commit()

            if status not in ["WAITING_APPROVAL", "WAITING_REVIEW"]:
                break