import database
import utils
from flask import Blueprint, jsonify, request

compras_bp = Blueprint('compras_bp', __name__)

chaves_obrigatorias = ['dia', 'produto_id', 'preco', 'qtd', 'fornecedor']

# Rota para adicionar compra ou listar compras
@compras_bp.route('/api/compras', methods=['GET', 'POST'])
def compras():
    # Conecta no DB e cria um cursor
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        # Se o método for GET
        if request.method == 'GET':
            # Quantos dias verá, se for 0, retorna todos os registros
            dias = request.args.get('dias')

            compras = utils.get_all_or_abort(cursor, 'compras', dias)
            lista_compras = []

            # Adiciona dicionários na lista
            for compra in compras:
                lista_compras.append({
                    'id': compra[0],
                    'dia': compra[1].strftime('%Y-%m-%d'),
                    'produto_id': compra[2],
                    'preco': compra[3],
                    'qtd': compra[4],
                    'fornecedor': compra[5]
                })

            return jsonify(lista_compras) # Lista de registros de compras

        # Se o método for POST
        else:
            # Recebe os dados enviados
            registro = request.json

            # Valida se todos os campos foram preenchidos e não há nenhum campo inválido
            utils.is_request_ok(registro, chaves_obrigatorias, chaves_obrigatorias)

            cursor.execute("insert into compras values (null, %s, %s, %s, %s, %s)",
                                    (registro.get('dia'),
                                     registro.get('produto_id'),
                                     registro.get('preco'),
                                     registro.get('qtd'),
                                     registro.get('fornecedor')))
            db.commit()
            return jsonify({'message': 'Registro cadastrado com sucesso!'})

    finally:
        # Fecha o cursor e a conexão com o banco
        cursor.close()
        db.close()


# Rota para alterar compra ou deletar compra
@compras_bp.route('/api/compras/<int:compra_id>', methods=['PUT', 'GET', 'DELETE'])
def compra(compra_id):
    # Conecta no DB e cria um cursor
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        # Se o método for PUT
        if request.method == 'PUT':
            # Recebe os dados
            data = request.json

            # Busca a linha na tabela pelo id
            utils.get_line_or_abort(cursor, 'compras', compra_id)

            # Valida se os dados recebidos são campos válidos
            utils.is_request_ok(data, chaves_obrigatorias)


            # Criar string com todos os campos, seguidos por "= %s" separados por ","
            campos_update = ', '.join([f"{campo} = %s" for campo in data.keys()])
            # Cria lista com os valores enviados
            valores = list(data.values())
            # Adiciona o id no final da lista de valores, pois será usado para fazer a seleção da linha
            valores.append(compra_id)

            cursor.execute(f'update compras set {campos_update} where id = %s', tuple(valores))
            db.commit()
            return jsonify({'message': 'Compra atualizada com sucesso!'})

        # Se o método for GET
        elif request.method == 'GET':
            # Busca a linha pelo ID
            compra = utils.get_line_or_abort(cursor, 'compras', compra_id)
            
            return jsonify({
                'id': compra[0],
                'dia': compra[1].strftime('%Y-%m-%d'),
                'produto_id': compra[2],
                'preco': compra[3],
                'qtd': compra[4],
                'fornecedor': compra[5]
            })

        # Se o método for DELETE
        else:
            # Busca a linha na tabela pelo ID
            utils.get_line_or_abort(cursor, 'compras', compra_id)

            cursor.execute("delete from compras where id = %s", (compra_id,))
            db.commit()
            return jsonify({'message': 'Compra deletada com sucesso!'})

    finally:
        cursor.close()
        db.close()