from flask import Flask, jsonify, request
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

db =mysql.connector.connect(
    host=os.getenv('DB_HOST_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_DATABASE')
)

cursor = db.cursor()

@app.route('/')
def hello_world():
    return '<h1>Hello world!</h1>'


# Rota para adicionar produtos
@app.route('/api/produtos/add', methods=['POST'])
def add_produto():
    produto = request.json

    if not 'nome' in produto:
        return jsonify({'message': 'Insira um nome válido para o produto'}), 400

    cursor.execute("insert into produtos values (null, %s)", (produto.get('nome'),))
    db.commit()
    return jsonify({'message': 'Produto cadastrado com sucesso!'})


# Rota para alterar o nome de algum produto
@app.route('/api/produtos/update/<int:product_id>', methods=['PUT'])
def update_produto(product_id):
    data = request.json
    cursor.execute("select * from produtos where id = %s", (product_id,))
    produto = cursor.fetchone()

    if not produto:
        return jsonify({'message': 'Produto não encontrado'}), 404
    if not 'nome' in data:
        return jsonify({'message': 'Insira um novo nome válido'}), 400

    cursor.execute('update produtos set nome = %s where id = %s', (data['nome'], product_id))
    db.commit()
    return jsonify({'message': 'Produto atualizado com sucesso!'})


# Rota para deletar produto
@app.route('/api/produtos/delete/<int:product_id>', methods=['DELETE'])
def del_produto(product_id):
    cursor.execute("select * from produtos where id = %s", (product_id,))
    produto = cursor.fetchone()

    if not produto:
        return jsonify({'message': 'Produto não encontrado'}), 404

    cursor.execute("delete from produtos where id = %s", (product_id,))
    db.commit()
    return jsonify({'message': 'Produto deletado com sucesso!'})


# Rota para listar produtos cadastrados
@app.route('/api/produtos', methods=['GET'])
def ver_produtos():
    cursor.execute('select * from produtos')
    produtos = cursor.fetchall()
    lista_produtos = []

    for produto in produtos:
        lista_produtos.append({
            'id': produto[0],
            'nome': produto[1]
        })

    return jsonify(lista_produtos)


# Rota para buscar produto pelo id
@app.route('/api/produtos/<int:product_id>', methods=['GET'])
def buscar_produto(product_id):
    cursor.execute("select * from produtos where id = %s", (product_id,))
    produto = cursor.fetchone()

    if not produto:
        return jsonify({'message': 'Produto não encontrado'}), 404

    return jsonify({'id': produto[0], 'nome': produto[1]})


chaves_compras = ('dia', 'produto_id', 'preco', 'qtd', 'fornecedor')
# Rota para adicionar registro de compra
@app.route('/api/compras/add', methods=['POST'])
def add_compra():
    registro = request.json

    for chave in chaves_compras:
        if chave not in registro:
            return jsonify({'message': 'Todos os campos obrigatórios devem ser preenchidos'}), 400

    cursor.execute("insert into compras values (null, %s, %s, %s, %s, %s)",
                   (registro.get('dia'),
                    registro.get('produto_id'),
                    registro.get('preco'),
                    registro.get('qtd'),
                    registro.get('fornecedor')))
    db.commit()
    return jsonify({'message': 'Registro cadastrado com sucesso!'})


# Rota para alterar um campo de uma compra
@app.route('/api/compras/update/<int:compra_id>', methods=['PUT'])
def update_compra(compra_id):
    data = request.json
    cursor.execute("select * from compras where id = %s", (compra_id,))
    compra = cursor.fetchone()

    if not data:
        return jsonify({'message': 'Nenhum dado enviado'}), 400
    if not compra:
        return jsonify({'message': 'Compra não encontrado'}), 404
    for campo in data:
        if campo not in chaves_compras:
            return jsonify({'message': 'Campo inválido inserido'}), 400

    campos_update = ', '.join([f"{campo} = %s" for campo in data.keys()])
    valores = list(data.values())
    valores.append(compra_id)

    cursor.execute(f'update compras set {campos_update} where id = %s', tuple(valores))
    db.commit()
    return jsonify({'message': 'Compra atualizada com sucesso!'})


# Rota para deletar compra
@app.route('/api/compras/delete/<int:compra_id>', methods=['DELETE'])
def del_compra(compra_id):
    cursor.execute("select * from compras where id = %s", (compra_id,))
    compra = cursor.fetchone()

    if not compra:
        return jsonify({'message': 'Compra não encontrada'}), 404

    cursor.execute("delete from compras where id = %s", (compra_id,))
    db.commit()
    return jsonify({'message': 'Compra deletada com sucesso!'})


# Rota para retornar compras dos ultimos n dias
@app.route('/api/compras', methods=['GET'])
def ver_compras():
    dias = request.args.get('dias')

    if not dias:
        cursor.execute("select * from compras")
    else:
        cursor.execute("select * from compras where dia >= curdate() - interval %s day", (int(dias),))

    compras = cursor.fetchall()
    lista_compras = []

    for compra in compras:
        lista_compras.append({
            'id': compra[0],
            'dia': compra[1],
            'produto_id': compra[2],
            'preco': compra[3],
            'qtd': compra[4],
            'fornecedor': compra[5]
        })

    return jsonify(lista_compras)


chaves_vendas = ('dia', 'produto_id', 'preco', 'qtd') # Ultimo campo, "comprador" é opcional
# Rota para adicionar registro de venda
@app.route('/api/vendas/add', methods=['POST'])
def add_venda():
    registro = request.json

    for chave in chaves_vendas:
        if chave not in registro:
            return jsonify({'message': 'Todos os campos obrigatórios devem ser preenchidos'}), 400

    cursor.execute("insert into vendas values (null, %s, %s, %s, %s, %s)",
                   (registro.get('dia'),
                    registro.get('produto_id'),
                    registro.get('preco'),
                    registro.get('qtd'),
                    registro.get('comprador', '')))
    db.commit()
    return jsonify({'message': 'Venda cadastrado com sucesso!'})


# Rota para alterar um campo de uma venda
@app.route('/api/vendas/update/<int:venda_id>', methods=['PUT'])
def update_venda(venda_id):
    data = request.json
    cursor.execute("select * from vendas where id = %s", (venda_id,))
    venda = cursor.fetchone()

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

    cursor.execute(f'update vendas set {campos_update} where id = %s', tuple(valores))
    db.commit()
    return jsonify({'message': 'Venda atualizada com sucesso!'})


# Rota para deletar venda
@app.route('/api/vendas/delete/<int:venda_id>', methods=['DELETE'])
def del_venda(venda_id):
    cursor.execute("select * from vendas where id = %s", (venda_id,))
    venda = cursor.fetchone()

    if not venda:
        return jsonify({'message': 'Venda não encontrado'}), 404

    cursor.execute("delete from vendas where id = %s", (venda_id,))
    db.commit()
    return jsonify({'message': 'Venda deletada com sucesso!'})


# Rota para retornar vendas dos ultimos n dias
@app.route('/api/vendas', methods=['GET'])
def ver_vendas():
    dias = request.args.get('dias')

    if not dias:
        cursor.execute("select * from vendas")
    else:
        cursor.execute("select * from vendas where dia >= curdate() - interval %s day", (int(dias),))

    vendas = cursor.fetchall()
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


if __name__ == "__main__":
    app.run(debug=True)