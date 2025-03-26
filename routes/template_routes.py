"""
Módulo de rotas para gerenciamento de templates.

Este módulo define as rotas da API relacionadas ao envio de templates
para validação na plataforma Zenvia, incluindo o processamento dos dados
do template e a comunicação com o serviço da Zenvia.
"""

from flask import Blueprint, request, jsonify
from services.zenvia_service import enviar_template
from utils.helpers import atualizar_exemplos
from config.settings import SENDER_PHONE, SENDER_EMAIL, CHANNEL

# Blueprint para rotas de templates
template_routes = Blueprint("template_routes", __name__)

@template_routes.route("/enviar-template", methods=["POST"])
def enviar_template_route():
    """
    Envia um novo template para validação na Zenvia.
    
    Esta função recebe os dados do template via requisição POST,
    valida os campos obrigatórios, formata o template conforme as
    especificações da API Zenvia, atualiza os exemplos de variáveis
    se necessário, e envia o template para validação.
    
    O template é configurado com a categoria UTILITY, canal WHATSAPP,
    e utiliza o número de telefone e email configurados no arquivo de ambiente.
    
    Returns:
        tuple: Um par contendo a resposta JSON e o código de status HTTP.
            Em caso de sucesso, retorna os dados do template e código 200.
            Em caso de erro, retorna uma mensagem de erro e o código apropriado.
    """
    data = request.json

    if "name" not in data or "text" not in data:
        return jsonify({"erro": "Campos 'name' e 'text' são obrigatórios"}), 400

    template_data = {
        "components": {
            "body": {
                "type": "TEXT_FIXED",
                "text": data["text"]
            }
        },
        "category": "UTILITY",
        "channel": CHANNEL or "WHATSAPP",
        "name": data["name"],
        "locale": "pt_BR",
        "senderId": SENDER_PHONE,
        "notificationEmail": SENDER_EMAIL,
        "examples": {}
    }
    
    if "buttons" in data and data["buttons"]:
        button_items = []
        
        for button in data["buttons"]:
            if isinstance(button, dict) and "text" in button and "type" in button:
                button_text = button["text"]
                button_type = button["type"]
                
                button_obj = {
                    "type": button_type,
                    "text": button_text,
                    "payload": button_text
                }
                
                if button_type == "URL" and "url" in button:
                    button_obj["url"] = button["url"]
                elif button_type == "PHONE_NUMBER" and "phone_number" in button:
                    button_obj["phoneNumber"] = button["phone_number"]
                
                button_items.append(button_obj)
            else:
                # Para compatibilidade, se o botão for apenas uma string, assume QUICK_REPLY
                if isinstance(button, str):
                    button_items.append({
                        "type": "QUICK_REPLY",
                        "text": button,
                        "payload": button
                    })
        
        if button_items:
            template_data["components"]["buttons"] = {
                "items": button_items,
                "type": "MIXED"
            }

    template_data = atualizar_exemplos(template_data)
    resultado, status_code, erro = enviar_template(template_data)

    if erro:
        return jsonify({"erro": "Falha ao enviar template", "detalhes": erro}), status_code

    return jsonify(resultado)