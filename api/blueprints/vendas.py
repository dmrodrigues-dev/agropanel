import database
import utils
from flask import Blueprint, jsonify, request

vendas_bp = Blueprint('vendas', __name__)

chaves_obrigatorias = ['dia', 'produto_id', 'preco', 'qtd'] # Ultimo campo, "comprador" é opcional

# Rota para adicionar venda ou listar vendas
@vendas_bp.route('/api/vendas', methods=['GET', 'POST'])
def vendas():
    # Cria cursor e conexão com DB
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        # Se o método for GET
        if request.method == 'GET':
            # Quantos dias verá, se for 0, retorna todos os registros
            dias = request.args.get('dias')

            # Recebe todas as linhas no dado intervalo
            vendas = utils.get_all_or_abort(cursor, 'vendas', dias)
            lista_vendas = []

            # Adiciona na lista um dicionário para cada venda
            for venda in vendas:
                lista_vendas.append({
                    'id': venda[0],
                    'dia': venda[1].strftime('%Y-%m-%d'),
                    'produto_id': venda[2],
                    'preco': venda[3],
                    'qtd': venda[4],
                    'comprador': venda[5]
                })

            return jsonify(lista_vendas)

        # Se o método for POST
        else:
            # Recebe os dados
            registro = request.json

            # Verifica se os campos do novo registros são aceitaveis e se todos os obrigatórios estão preenchidos
            utils.is_request_ok(registro, chaves_obrigatorias+['comprador'], chaves_obrigatorias)


            cursor.execute("insert into vendas values (null, %s, %s, %s, %s, %s)",
                                    (registro.get('dia'),
                                     registro.get('produto_id'),
                                     registro.get('preco'),
                                     registro.get('qtd'),
                                     registro.get('comprador', '')))
            db.commit()
            return jsonify({'message': 'Venda cadastrada com sucesso!'})

    finally:
        # Fecha a conexão com o banco e o cursor
        cursor.close()
        db.close()


# Rota para alterar venda ou deletar vendas
@vendas_bp.route('/api/vendas/<int:venda_id>', methods=['PUT', 'GET', 'DELETE'])
def venda(venda_id):
    # Cria conexão com banco e cursor
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        # Se o método for PUT
        if request.method == 'PUT':
            # Recebe os dados
            data = request.json

            # Busca a linha na tabela pelo ID
            utils.get_line_or_abort(cursor, 'vendas', venda_id)

            # Verifica se o campo alterado é válido
            utils.is_request_ok(data, chaves_obrigatorias+['comprador'])


            # Cria string com todos os campos, seguidos por "= %s" separados por ","
            campos_update = ', '.join([f"{campo} = %s" for campo in data.keys()])
            # Cria lista com os valores enviados
            valores = list(data.values())
            # Adiciona o id no final da lista de valores, pois será usado para fazer a seleção da linha
            valores.append(venda_id)

            cursor.execute(f'update vendas set {campos_update} where id = %s', tuple(valores))
            db.commit()
            return jsonify({'message': 'Venda atualizada com sucesso!'})

        # Se o método for GET
        elif request.method == 'GET':
            # Busca a linha pelo ID
            venda = utils.get_line_or_abort(cursor, 'vendas', venda_id)
            
            return jsonify({
                    'id': venda[0],
                    'dia': venda[1].strftime('%Y-%m-%d'),
                    'produto_id': venda[2],
                    'preco': venda[3],
                    'qtd': venda[4],
                    'comprador': venda[5]
                })

        # Se o método for DELETE
        else:
            # Busca a linha pelo id
            utils.get_line_or_abort(cursor, 'vendas', venda_id)

            cursor.execute("delete from vendas where id = %s", (venda_id,))
            db.commit()
            return jsonify({'message': 'Venda deletada com sucesso!'})

    finally:
        cursor.close()
        db.close()