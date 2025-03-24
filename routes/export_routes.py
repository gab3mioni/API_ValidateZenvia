"""
Módulo de rotas para exportação de dados.

Este módulo define as rotas da API relacionadas à exportação de dados
dos templates para arquivos CSV, garantindo a correta codificação de
caracteres especiais e separação adequada das colunas.
"""

import csv
import os
import datetime
from io import StringIO
from flask import Blueprint, Response
from models.template import Template
from threading import Lock

# Blueprint para rotas de exportação
export_routes = Blueprint("export_routes", __name__)
lock = Lock()

@export_routes.route("/exportar-csv", methods=["GET"])
def exportar_csv():
    """
    Exporta todos os templates para um arquivo CSV.
    
    Esta função consulta todos os templates armazenados no banco de dados
    e gera um arquivo CSV contendo o ID, status e motivo de rejeição de cada template.
    O arquivo é salvo no diretório 'csv_output' com um timestamp no nome
    e também é retornado como resposta HTTP para download pelo cliente.
    
    O arquivo CSV é gerado com codificação UTF-8 e delimitador de ponto e vírgula
    para garantir compatibilidade com programas como o Excel.
    
    Returns:
        Response: Resposta HTTP contendo o arquivo CSV para download.
    """
    with lock:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv_output")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"status_templates_{timestamp}.csv"
        file_path = os.path.join(output_dir, filename)
        
        si = StringIO()
        si.write('\ufeff')  # BOM para UTF-8
        
        writer = csv.writer(si, delimiter=';')
        writer.writerow(["ID", "Status", "Motivo Rejeição"])

        templates = Template.query.all()
        for template in templates:
            writer.writerow([
                template.id,
                template.status,
                template.motivo_rejeicao or ""
            ])

        output = si.getvalue()
        
        # Salva o arquivo com o mesmo delimitador
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            f.write(output)
            
        si.close()

    return Response(
        output,
        mimetype="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f"attachment;filename={filename}",
            "Content-Type": "text/csv; charset=utf-8"
        }
    )