"""
Módulo de funções auxiliares para manipulação de templates.

Este módulo contém funções utilitárias para encontrar variáveis em textos
de templates e atualizar os exemplos necessários para submissão à API Zenvia.
"""

import re

def encontrar_variaveis(texto):
    """
    Encontra todas as variáveis em um texto de template.
    
    Esta função usa expressões regulares para identificar padrões de variáveis
    no formato {{nome_variavel}} e retorna um conjunto com os nomes das variáveis
    encontradas, sem as chaves.
    
    Args:
        texto (str): Texto do template a ser analisado.
        
    Returns:
        set: Conjunto com os nomes de todas as variáveis encontradas no texto.
    """
    return set(re.findall(r'\{\{(\w+)\}\}', texto))

def atualizar_exemplos(data):
    """
    Atualiza o dicionário de exemplos no template com valores para todas as variáveis.
    
    Esta função analisa o texto do template, encontra todas as variáveis presentes
    e garante que cada variável tenha um valor de exemplo correspondente no
    dicionário de exemplos. Se uma variável não tiver um exemplo, o valor padrão
    "Exemplo" será utilizado.
    
    Args:
        data (dict): Dicionário contendo os dados do template, incluindo o texto
                     e o dicionário de exemplos existente.
        
    Returns:
        dict: Dicionário de dados do template com o campo "examples" atualizado.
    """
    texto = data["components"]["body"]["text"]
    variaveis = encontrar_variaveis(texto)
    exemplos = data.get("examples", {})
    
    for var in variaveis:
        exemplos.setdefault(var, "Exemplo")
    
    data["examples"] = exemplos
    return data