import database
import utils
from flask import Blueprint, jsonify, request
from sqlalchemy import text

vendas_bp = Blueprint('vendas', __name__)

chaves_obrigatorias = ['dia', 'produto_id', 'qtd'] # campos "preco" e "comprador" são opcionais

# Rota para adicionar venda ou listar vendas
@vendas_bp.route('/api/vendas', methods=['GET', 'POST'])
def vendas():
    # Com uma conexão da engine feita, execute o bloco
    with database.engine.connect() as conn:

        # Se o método for GET
        if request.method == 'GET':
            # Quantos dias verá, se for 0, retorna todos os registros
            dias = request.args.get('dias')

            # Recebe todas as linhas no dado intervalo
            vendas = utils.get_all_or_abort(conn, 'vendas', dias)
            return jsonify([utils.type_casted_dict(dict(row._mapping)) for row in vendas])

        # Se o método for POST
        else:
            # Recebe os dados
            registro = request.json

            # None para campos preco e comprador, caso sejam ""
            if str(registro.get('preco')).strip() == '':
                registro['preco'] = None
            if str(registro.get('comprador')).strip() == '':
                registro['comprador'] = None

            # Verifica se os campos do novo registros são aceitaveis e se todos os obrigatórios estão preenchidos
            utils.is_request_ok(registro, chaves_obrigatorias+['comprador', 'preco'], chaves_obrigatorias)

            # Valida se tem preco_de_venda positivo
            utils.is_request_non_negative(registro)

            # Verifica se existe um produto com o ID fornecido
            utils.get_line_or_abort(conn, 'produtos', registro.get('produto_id'))

            # Se o preco estiver vazio, busca o preço padrão na tabela produtos
            conn.execute(text("insert into vendas(dia, produto_id, preco, qtd, comprador) values (:dia, :produto_id, coalesce(:preco, (select preco_de_venda from produtos where id = :produto_id)), :qtd, :comprador)"),{
                'dia': registro.get('dia'),
                'produto_id': registro.get('produto_id'),
                'preco': registro.get('preco'),
                'qtd': registro.get('qtd'),
                'comprador': registro.get('comprador')
            })
            conn.commit()
            return jsonify({'message': 'Venda cadastrada com sucesso!'})


# Rota para alterar venda ou deletar vendas
@vendas_bp.route('/api/vendas/<int:venda_id>', methods=['PUT', 'GET', 'DELETE'])
def venda(venda_id):
    # Com uma conexão da engine feita, execute o bloco
    with database.engine.connect() as conn:

        # Se o método for PUT
        if request.method == 'PUT':
            # Recebe os dados
            data = request.json

            # Busca a linha na tabela pelo ID
            utils.get_line_or_abort(conn, 'vendas', venda_id)

            # Verifica se o campo alterado é válido
            utils.is_request_ok(data, chaves_obrigatorias+['comprador', 'preco'])

            # Valida se tem preco_de_venda positivo
            utils.is_request_non_negative(data)

            # Se houver alteração no ID, verifica se existe um produto com o ID fornecido
            if 'produto_id' in data:
                utils.get_line_or_abort(conn, 'produtos', data.get('produto_id'))

            # Cria string com todos os campos, seguidos por "= :campo" separados por ","
            campos_update = ', '.join([f"{campo} = :{campo}" for campo in data.keys()])
            # Adicionar o item 'id' ao dicionário 'data'
            data['id'] = venda_id

            conn.execute(text(f'update vendas set {campos_update} where id = :id'),
                         data)
            conn.commit()
            return jsonify({'message': 'Venda atualizada com sucesso!'})

        # Se o método for GET
        elif request.method == 'GET':
            # Busca a linha pelo ID
            venda = utils.get_line_or_abort(conn, 'vendas', venda_id)
            
            # Retorna um dicionario convertendo o tipo decimal para float
            return jsonify(utils.type_casted_dict(dict(venda._mapping)))

        # Se o método for DELETE
        else:
            # Busca a linha pelo id
            utils.get_line_or_abort(conn, 'vendas', venda_id)

            conn.execute(text("delete from vendas where id = :id"),
                         {'id': venda_id})
            conn.commit()
            return jsonify({'message': 'Venda deletada com sucesso!'})
