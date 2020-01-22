from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from models import Pessoas, Atividades, Usuarios

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

#USUARIOS = {
#    'rafael':'123',
#    'thiago':'4321'
#}

#@auth.verify_password
#def verificacao(login, senha):
#    print('validando usuario')
#    print(USUARIOS.get(login) == senha)
#   if not (login, senha):
#        return False
#    return USUARIOS.get(login) == senha


@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()


class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()

        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status':'error',
                'mensagem':'pessoa nao encontrada!'
            }
        return response

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        #dados = json.loads(request.data)
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = 'Pessoa {} excluida com sucesso!'.format(pessoa.nome)
        pessoa.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}

class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas ]
        return(response)

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id': i.id, 'pessoa': i.pessoa.nome, 'nome': i.nome} for i in atividades]
        return (response)

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa, status=dados['status'])
        atividade.save()
        response = {
            'pessoa': atividade.pessoa.nome,
            'nome': atividade.nome,
            'id': atividade.id
        }
        return response


class ListaAtividadesPessoa(Resource):
    def get(self, pessoa):
        dados = Pessoas.query.filter_by(nome=pessoa).first()
        try:
            atividades = Atividades.query.filter_by(pessoa_id=dados.id)
            response = [{'id': i.id, 'pessoa': i.pessoa.nome, 'nome': i.nome} for i in atividades]
        except AttributeError:
            response = {
                'status':'error',
                'mensagem':'pessoa nao encontrada!'
            }
        return (response)

class AlterarAtividades(Resource):
    def get(self, id):
        dados = Atividades.query.filter(id=id)
        response = [{'id': i.id, 'pessoa': i.pessoa.nome, 'nome': i.nome} for i in dados]
        return response

api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')
api.add_resource(ListaAtividadesPessoa, '/atividades/<string:pessoa>/')

if __name__ == '__main__':
    app.run(debug=True)