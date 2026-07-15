import database
import utils
from flask import Blueprint, jsonify, request
from sqlalchemy import text

compras_bp = Blueprint('compras_bp', __name__)

chaves_obrigatorias = ['dia', 'produto_id', 'preco', 'qtd', 'fornecedor']

# Rota para adicionar compra ou listar compras
@compras_bp.route('/api/compras', methods=['GET', 'POST'])
def compras():
    # Com uma conexão da engine feita, execute o bloco
    with database.engine.connect() as conn:

        # Se o método for GET
        if request.method == 'GET':
            # Quantos dias verá, se for 0, retorna todos os registros
            dias = request.args.get('dias')

            # Recebe todas as linhas no dado intervalo
            compras = utils.get_all_or_abort(conn, 'compras', dias)
            return jsonify([utils.type_casted_dict(dict(row._mapping)) for row in compras]) # Lista de registros de compras

        # Se o método for POST
        else:
            # Recebe os dados enviados
            registro = request.json

            # Valida se todos os campos foram preenchidos e não há nenhum campo inválido
            utils.is_request_ok(registro, chaves_obrigatorias, chaves_obrigatorias)

            # Valida se tem preco_de_venda positivo
            utils.is_request_non_negative(registro)

            # Verifica se existe um produto com o ID fornecido
            utils.get_line_or_abort(conn, 'produtos', registro.get('produto_id'))

            conn.execute(text("insert into compras(dia, produto_id, preco, qtd, fornecedor) values (:dia, :produto_id, :preco, :qtd, :fornecedor)"),{
                'dia': registro.get('dia'),
                'produto_id': registro.get('produto_id'),
                'preco': registro.get('preco'),
                'qtd': registro.get('qtd'),
                'fornecedor': registro.get('fornecedor')
            })
            conn.commit()
            return jsonify({'message': 'Compra cadastrado com sucesso!'})


# Rota para alterar compra ou deletar compra
@compras_bp.route('/api/compras/<int:compra_id>', methods=['PUT', 'GET', 'DELETE'])
def compra(compra_id):
    # Com uma conexão da engine feita, execute o bloco
    with database.engine.connect() as conn:

        # Se o método for PUT
        if request.method == 'PUT':
            # Recebe os dados
            data = request.json

            # Busca a linha na tabela pelo id
            utils.get_line_or_abort(conn, 'compras', compra_id)

            # Valida se os dados recebidos são campos válidos
            utils.is_request_ok(data, chaves_obrigatorias)

            # Valida se tem preco_de_venda positivo
            utils.is_request_non_negative(data)

            # Se houver alteração no ID, verifica se o ID do produto é valido
            if 'produto_id' in data:
                utils.get_line_or_abort(conn, 'produtos', data.get('produto_id'))

            # Criar string com todos os campos, seguidos por "= :campo" separados por ","
            campos_update = ', '.join([f"{campo} = :{campo}" for campo in data.keys()])
            # Adicionar o item 'id' ao dicionário 'data'
            data['id'] = compra_id

            conn.execute(text(f'update compras set {campos_update} where id = :id'),
                         data)
            conn.commit()
            return jsonify({'message': 'Compra atualizada com sucesso!'})

        # Se o método for GET
        elif request.method == 'GET':
            # Busca a linha pelo ID
            compra = utils.get_line_or_abort(conn, 'compras', compra_id)
            
            # Retorna um dicionario convertendo o tipo decimal para float
            return jsonify(utils.type_casted_dict(dict(compra._mapping)))

        # Se o método for DELETE
        else:
            # Busca a linha na tabela pelo ID
            utils.get_line_or_abort(conn, 'compras', compra_id)

            conn.execute(text("delete from compras where id = :id"),
                         {'id': compra_id})
            conn.commit()
            return jsonify({'message': 'Compra deletada com sucesso!'})
