from flask import abort
from datetime import date
from sqlalchemy import text
from decimal import Decimal

# Retorna uma linha, ou invoca errorhandler se não encontra-la
def get_line_or_abort(conexao, table, identificador):
    query = conexao.execute(text(f'select * from {table}'+' where id = :identificador'), {'identificador':identificador})
    linha = query.fetchone()
    if not linha:
        abort(404, 'Registro não encontrado')
    else:
        return linha
    

# Retorna um vetor de linhas, ou invoca errorhandler se receber um intervalo de dias inválido
def get_all_or_abort(conexao, table, intervalo=False):
    if not intervalo or intervalo == '0':
        query = conexao.execute(text(f"select * from {table} order by id desc"))
    elif intervalo and intervalo.isdigit():
        query = conexao.execute(text(f"select * from {table} "+"where dia >= current_date - (:dias * interval '1 day') order by id desc"), {'dias':int(intervalo)})
    else:
        abort(400, 'Intervalo de dias inválido.')
        return
    
    linhas = query.fetchall()
    return linhas
    

# Verifica se os dados fornecidos estão de acordo com os requisitos, e invoca errorhandler, caso não
def is_request_ok(dados, chaves_possiveis, chaves_obrigatorias=False):
    if not dados:
        abort(400, 'Nenhum dado foi enviado.')

    for campo in dados:
        if campo not in chaves_possiveis:
            abort(400, 'Campo inválido inserido.')

    if chaves_obrigatorias:
        for chave in chaves_obrigatorias:
            if chave not in dados:
                abort(400, 'Campo obrigatório permaneceu vazio')
    

# Retorna uma string para filtrar uma query, ou invoca errorhandler se os parametros forem inválidos
def month_and_year_validation(mes, ano):
    if mes and ano:
        if mes.isdigit() and ano.isdigit() and (0 < int(mes) < 13) and (1999 < int(ano) < 2500):
            filtro = f"{int(mes):02d}-{ano}"
        else:
            abort(400, 'Data inválida.')
    else:
        filtro = date.today().strftime('%m-%Y')
    return filtro


# Type casting para float de todos os dados no formato decimal de um dicionario
def type_casted_dict(dicionario):
    for chave in dicionario.keys():
        
        if isinstance(dicionario[chave], Decimal):
            dicionario[chave] = float(dicionario[chave])

        elif isinstance(dicionario[chave], date):
            dicionario[chave] = dicionario[chave].strftime('%Y-%m-%d')

    return dicionario