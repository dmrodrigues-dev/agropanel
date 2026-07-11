import database
import utils
from flask import Blueprint, jsonify, request
from sqlalchemy import text

estatisticas_bp = Blueprint('estatisticas', __name__)


# Rota para retornar as estatísticas de um mês
@estatisticas_bp.route('/api/estatisticas', methods=['GET'])
def estatisticas_gerais():

    # Recebe argumentos da rota
    mes = request.args.get('mes')
    ano = request.args.get('ano')

    # Com uma conexão da engine feita, execute o bloco
    with database.engine.connect() as conn:

        # Valida mes e ano e recebe um filtro para a query
        filtro = utils.month_and_year_validation(mes, ano)

        # Busca a soma da multiplicação de quantidade e do valor de cada compra
        query = conn.execute(text("select coalesce(sum(preco*qtd), 0) from compras where to_char(dia, 'MM-YYYY') = :filtro "), {'filtro': filtro})
        despesa = query.fetchone()[0]

        # Busca a soma da multiplicação de quantidade e do valor de cada venda
        query = conn.execute(text("select coalesce(sum(preco*qtd), 0) from vendas where to_char(dia, 'MM-YYYY') = :filtro "), {'filtro': filtro})
        receita = query.fetchone()[0]

        # Calcula lucro
        lucro = receita - despesa

        # Busca quais 10 produtos mais renderam no mes
        query = conn.execute(text("select p.nome as nome, sum(v.qtd*v.preco) as valor from vendas as v " \
        "join produtos as p on v.produto_id = p.id " \
        "where to_char(v.dia, 'MM-YYYY') = :filtro " \
        "group by v.produto_id, p.nome order by valor desc limit 10;"), {'filtro': filtro})
        # Lista de tuplas no formato ('nome', valor)
        raw_vendaveis = query.fetchall()
        vendaveis = [utils.type_casted_dict(dict(row._mapping)) for row in raw_vendaveis]

        # Retorno
        return jsonify(utils.type_casted_dict({
            'receita': receita,
            'despesa': despesa,
            'lucro': lucro,
            'vendaveis': vendaveis
        }))
