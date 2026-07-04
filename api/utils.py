from flask import abort
from datetime import date

# Retorna uma linha, ou invoca errorhandler se não encontra-la
def get_line_or_abort(cursor, table, identificador):
    cursor.execute(f'select * from {table}'+' where id = %s', (identificador,))
    linha = cursor.fetchone()
    if not linha:
        abort(404, 'Registro não encontrado')
    else:
        return linha
    

# Retorna um vetor de linhas, ou invoca errorhandler se receber um intervalo de dias inválido
def get_all_or_abort(cursor, table, intervalo=False):
    if not intervalo or intervalo == '0':
        cursor.execute(f"select * from {table} order by id desc")
    elif intervalo and intervalo.isdigit():
        cursor.execute(f"select * from {table} "+"where dia >= curdate() - interval %s day order by id desc", (int(intervalo),))
    else:
        abort(400, 'Intervalo de dias inválido.')
    
    linhas = cursor.fetchall()
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