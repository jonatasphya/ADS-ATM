import socket
import locale
import ast
from datetime import date

locale.setlocale(locale.LC_ALL, '')

usuarioServ = "smith"
senhaServ = "123456"

def deposito(dicionario):
    global saldo
    valor_deposito = float(dicionario["valor_deposito"])
    saldo += valor_deposito
    tr = '{"id": "deposito", "data":"'+str(date.today().strftime('%d/%m/%Y'))+'", "valor":"'+locale.currency(valor_deposito, grouping=True, symbol= True)+'", "saldo":"'+locale.currency(saldo, grouping=True, symbol= True)+'"}'
    transacao.append(tr)
    msg = '{"id": "sucesso_deposito", "mensagem":"DEPOSITO DE R$ '+locale.currency(valor_deposito, grouping=True, symbol= True)+' REALIZADO COM SUCESSO. SALDO ATUAL: '+locale.currency(saldo, grouping=True, symbol= True)+'", "saldo":"'+locale.currency(saldo, grouping=True, symbol= True)+'"}'   
    print('RETORNO: ', msg)
    return msg

def login(dicionario):
    usuario = dicionario["usuario"]
    senha = dicionario["senha"]
    print('{} quer fazer login'.format(usuario))
    if(usuario == usuarioServ and senha == senhaServ):
        msg = '{"id": "sucesso_login", "mensagem":"LOGADO COM SUCESSO"}'
    else:
        msg = '{"id": "falha_login", "mensagem":"FALHA NO LOGIN, TENTE NOVAMENTE"}'
    print('RETORNO: ', msg)
    return msg

def saque(dicionario):
    global saldo, transacao
    valor_saque = float(dicionario["valor_saque"])
    if(valor_saque <= saldo):
        saldo = saldo - valor_saque
        tr = '{"id": "saque", "data":"'+str(date.today().strftime('%d/%m/%Y'))+'", "valor":"'+locale.currency(valor_saque, grouping=True, symbol= True)+'", "saldo":"'+locale.currency(saldo, grouping=True, symbol= True)+'"}'
        transacao.append(tr)
        msg = '{"id": "sucesso_saque", "mensagem":"SAQUE DE '+locale.currency(valor_saque, grouping=True, symbol= True)+' REALIZADO COM SUCESSO. SALDO ATUAL: '+locale.currency(saldo, grouping=True, symbol= True)+'", "saldo":"'+locale.currency(saldo, grouping=True, symbol= True)+'"}'
    else:
        msg = '{"id": "falha_saque", "mensagem":"SALDO INSUFICIENTE PARA O SAQUE DE '+locale.currency(valor_saque, grouping=True, symbol= True)+'", "saldo":"'+locale.currency(saldo, grouping=True, symbol= True)+'"}'
    print('RETORNO: ', msg)
    return msg

transacao = []

def registroTransacao():
    msg = ''
    if(len(transacao) != 0):   
        for acao in transacao:
            msg += acao + '\n'
    else:
        msg = "sem_dados"
    print('RETORNO: \n', msg)
    return msg

def autenticacao(dicionario):
    if(dicionario["senha"] == senhaServ):
        msg = '{"id": "autenticacao_aceita"}'
    else:
        msg = '{"id": "autenticacao_rejeitada"}'
    return msg


HOST = 'localhost'
PORTA = 60000          
conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conexao.bind((HOST, PORTA))
conexao.listen()

print('Aguardando conexão')

conexao, endereco = conexao.accept()
print('Conectado', endereco)

saldo = 0.0

while True:
    dados = conexao.recv(1024)
    dados = dados.decode()
    
    dados_dicionario = ast.literal_eval(dados)
    id = dados_dicionario["id"]

    if(id == 'login'):
        conexao.sendall(login(dados_dicionario).encode())
    elif(id == 'deposito'):
        conexao.sendall(deposito(dados_dicionario).encode())
    elif(id == 'saque'):
        conexao.sendall(saque(dados_dicionario).encode())
    elif(id == 'transacao'):
        conexao.send(registroTransacao().encode())
    elif(id == 'autenticacao'):
        conexao.send(autenticacao(dados_dicionario).encode())
    elif(id == 'sair'):
        print("SOLICITAÇÃO DO USUÁRIO PARA SAIR! SAINDO...")
        conexao.close()
        break

    
    
    

    

    
        
 
        


