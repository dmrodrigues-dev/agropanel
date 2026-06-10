from api import database
from flask import Blueprint, jsonify, request

vendas_bp = Blueprint('vendas', __name__)

chaves_obrigatorias = ('dia', 'produto_id', 'preco', 'qtd') # Ultimo campo, "comprador" é opcional

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

            if not dias:
                cursor.execute("select * from vendas")
            else:
                cursor.execute("select * from vendas where dia >= curdate() - interval %s day", (int(dias),))

            vendas = cursor.fetchall()
            lista_vendas = []

            # Adiciona na lista um dicionário para cada venda
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

        # Se o método for POST
        else:
            # Recebe os dados
            registro = request.json

            # Se estiver faltando alguma chave obrigatória no request, retorna 400
            for chave in chaves_obrigatorias:
                if chave not in registro:
                    return jsonify({'message': 'Todos os campos obrigatórios devem ser preenchidos'}), 400

            cursor.execute("insert into vendas values (null, %s, %s, %s, %s, %s)",
                                    (registro.get('dia'),
                                     registro.get('produto_id'),
                                     registro.get('preco'),
                                     registro.get('qtd'),
                                     registro.get('comprador', '')))
            db.commit()
            return jsonify({'message': 'Venda cadastrada com sucesso!'})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

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
            cursor.execute("select * from vendas where id = %s", (venda_id,))
            venda = cursor.fetchone()

            # Se não houver dados do request, ou linha com o id fornecido, ou alguma chave que não exista na tabela, retorna error 400 ou 404
            if not data:
                return jsonify({'message': 'Nenhum dado enviado'}), 400
            if not venda:
                return jsonify({'message': 'Venda não encontrada'}), 404
            for campo in data:
                if campo not in chaves_obrigatorias and campo != 'comprador':
                    return jsonify({'message': 'Campo inválido inserido'}), 400

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
            cursor.execute("select * from vendas where id = %s", (venda_id,))
            venda = cursor.fetchone()

            # Se não houver linha com o ID fornecido, retorna 404
            if not venda:
                return jsonify({'message': 'Venda não encontrada'}), 404
            
            return jsonify({
                    'id': venda[0],
                    'dia': venda[1],
                    'produto_id': venda[2],
                    'preco': venda[3],
                    'qtd': venda[4],
                    'comprador': venda[5]
                })

        # Se o método for DELETE
        else:
            # Busca a linha pelo id
            cursor.execute("select * from vendas where id = %s", (venda_id,))
            venda = cursor.fetchone()

            # Se não achar a linha, retorna 404
            if not venda:
                return jsonify({'message': 'Venda não encontrada'}), 404

            cursor.execute("delete from vendas where id = %s", (venda_id,))
            db.commit()
            return jsonify({'message': 'Venda deletada com sucesso!'})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

    finally:
        cursor.close()
        db.close()