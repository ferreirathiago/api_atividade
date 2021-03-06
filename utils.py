from models import Pessoas, db_session, Usuarios

def insere_pessoas():
    pessoa = Pessoas(nome='Thiago', idade='35')
    print (pessoa)
    pessoa.save()

def consulta_pessoa():
    pessoa = Pessoas.query.all()
    print(pessoa)
    pessoa = Pessoas.query.filter_by(nome='Thiago')
    #print(pessoa.idade)
    for p in pessoa:
        print(p.idade)

def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Thiago').first()
    pessoa.idade = 21
    pessoa.save()

def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Thiago').first()
    pessoa.delete()

def insere_usuario(login, senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()

def consulta_todos_usuarios():
    usuario = Usuarios.query.all()
    print(usuario)

if __name__ == '__main__':
    #insere_pessoas()
    #altera_pessoa()
    #exclui_pessoa()
    #consulta_pessoa()
    insere_usuario('thiago', '12345')
    insere_usuario('rafael', '123')
    consulta_todos_usuarios()