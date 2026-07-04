import database
import utils
from flask import Blueprint, jsonify, request

estatisticas_bp = Blueprint('estatisticas', __name__)


# Rota para retornar as estatísticas de um mês
@estatisticas_bp.route('/api/estatisticas', methods=['GET'])
def estatisticas_gerais():
    # Conecta na pool e cria o cursor
    db = database.pool.get_connection()
    cursor = db.cursor()

    # Recebe argumentos da rota
    mes = request.args.get('mes')
    ano = request.args.get('ano')

    try:
        # Valida mes e ano e recebe um filtro para a query
        filtro = utils.month_and_year_validation(mes, ano)

        # Busca a soma da multiplicação de quantidade e do valor de cada compra
        cursor.execute("select coalesce(sum(preco*qtd), 0) from compras where date_format(dia, '%m-%Y') = %s ", (filtro,))
        despesa = cursor.fetchone()[0]

        # Busca a soma da multiplicação de quantidade e do valor de cada venda
        cursor.execute("select coalesce(sum(preco*qtd), 0) from vendas where date_format(dia, '%m-%Y') = %s ", (filtro,))
        receita = cursor.fetchone()[0]

        # Calcula lucro
        lucro = receita - despesa

        # Busca quais 10 produtos mais renderam no mes
        cursor.execute("select p.nome, sum(v.qtd*v.preco) as valor from vendas as v " \
        "join produtos as p on v.produto_id = p.id " \
        "where date_format(v.dia, '%m-%Y') = %s " \
        "group by v.produto_id order by valor desc limit 10;", (filtro,))
        # Lista de tuplas no formato ('nome', valor)
        raw_vendaveis = cursor.fetchall()
        vendaveis = []

        for item in raw_vendaveis:
            vendaveis.append({'nome': item[0], 'valor':item[1]})

        # Retorno
        return jsonify({
            'receita': receita,
            'despesa': despesa,
            'lucro': lucro,
            'vendaveis': vendaveis
        })

    finally:
        cursor.close()
        db.close()