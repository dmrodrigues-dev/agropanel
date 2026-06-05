from api import database
from flask import Blueprint, jsonify, request

vendas_bp = Blueprint('vendas', __name__)

chaves_vendas = ('dia', 'produto_id', 'preco', 'qtd') # Ultimo campo, "comprador" é opcional
# Rota para adicionar registro de venda
@vendas_bp.route('/api/vendas/add', methods=['POST'])
def add_venda():
    registro = request.json

    for chave in chaves_vendas:
        if chave not in registro:
            return jsonify({'message': 'Todos os campos obrigatórios devem ser preenchidos'}), 400

    database.cursor.execute("insert into vendas values (null, %s, %s, %s, %s, %s)",
                   (registro.get('dia'),
                    registro.get('produto_id'),
                    registro.get('preco'),
                    registro.get('qtd'),
                    registro.get('comprador', '')))
    database.db.commit()
    return jsonify({'message': 'Venda cadastrado com sucesso!'})


# Rota para alterar um campo de uma venda
@vendas_bp.route('/api/vendas/update/<int:venda_id>', methods=['PUT'])
def update_venda(venda_id):
    data = request.json
    database.cursor.execute("select * from vendas where id = %s", (venda_id,))
    venda = database.cursor.fetchone()

    if not data:
        return jsonify({'message': 'Nenhum dado enviado'}), 400
    if not venda:
        return jsonify({'message': 'Venda não encontrada'}), 404
    for campo in data:
        if campo not in chaves_vendas and campo != 'comprador':
            return jsonify({'message': 'Campo inválido inserido'}), 400

    campos_update = ', '.join([f"{campo} = %s" for campo in data.keys()])
    valores = list(data.values())
    valores.append(venda_id)

    database.cursor.execute(f'update vendas set {campos_update} where id = %s', tuple(valores))
    database.db.commit()
    return jsonify({'message': 'Venda atualizada com sucesso!'})


# Rota para deletar venda
@vendas_bp.route('/api/vendas/delete/<int:venda_id>', methods=['DELETE'])
def del_venda(venda_id):
    database.cursor.execute("select * from vendas where id = %s", (venda_id,))
    venda = database.cursor.fetchone()

    if not venda:
        return jsonify({'message': 'Venda não encontrado'}), 404

    database.cursor.execute("delete from vendas where id = %s", (venda_id,))
    database.db.commit()
    return jsonify({'message': 'Venda deletada com sucesso!'})


# Rota para retornar vendas dos ultimos n dias
@vendas_bp.route('/api/vendas', methods=['GET'])
def ver_vendas():
    dias = request.args.get('dias')

    if not dias:
        database.cursor.execute("select * from vendas")
    else:
        database.cursor.execute("select * from vendas where dia >= curdate() - interval %s day", (int(dias),))

    vendas = database.cursor.fetchall()
    lista_vendas = []

    for venda in vendas:
        lista_vendas.append({
            'id': venda[0],
            'dia': venda[1],
            'produto_id': venda[2],
            'preco': venda[3],
            'qtd': venda[4],
            'comprador': venda[5]
        })

    return jsonify(lista_vendas)