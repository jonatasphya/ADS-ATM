#REFERÊNCIAS
#https://www.tutorialspoint.com/python/python_gui_programming.htm
#https://python-guide-pt-br.readthedocs.io/pt_BR/latest/scenarios/json.html
#https://pythonprogramming.net/sockets-tutorial-python-3/
#https://www.youtube.com/watch?v=MeMCBdnhvQs&t=1007s
import socket
import locale
import ast
from tkinter import *
from tkinter import messagebox

locale.setlocale(locale.LC_ALL, '') 

HOST = 'localhost'  
PORTA = 60000          
conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conexao.connect((HOST, PORTA))

bg_color = "#000"
fg_color = "#3afc1c"
saldo = locale.currency(0.0, grouping=True, symbol=True)

def enviaRecebe(msg):
    conexao.send(msg.encode())
    dados = conexao.recv(1024)
    dados = dados.decode()
    dados_dicionario = ast.literal_eval(dados)
    return dados_dicionario

def execLogin():
    if(txb_usuario.get() != '' or txb_senha.get() != ''):
        msg  =  '{"id": "login", "usuario":"'+txb_usuario.get()+'", "senha":"'+txb_senha.get()+'"}'
        dados_dicionario = enviaRecebe(msg)
        if(dados_dicionario["id"] == 'sucesso_login'):
            messagebox.showinfo("SUCESSO", dados_dicionario["mensagem"])
            telaMenu()
            main.withdraw()
        elif(dados_dicionario["id"] == 'falha_login'):
            messagebox.showerror("ERRO", dados_dicionario["mensagem"])
    else:
        messagebox.showerror("ERRO", "PREENCHA OS DADOS DE LOGIN CORRENTAMENTE")

def execDeposito():
    global saldo
    
    if(txb_valorDeposito.get() != "0"):
        float(txb_valorDeposito.get().replace(",", "."))        
        msg = '{"id": "deposito", "valor_deposito":"'+txb_valorDeposito.get().replace(",", ".")+'"}'
        dados_dicionario = enviaRecebe(msg)
        saldo = "SALDO ATUAL: {}".format(dados_dicionario["saldo"])
        lbl_saldo.config(text = saldo)
        messagebox.showinfo("INFORMAÇÃO", dados_dicionario["mensagem"])
        deposito.destroy()
    else:
        messagebox.showerror("ERRO", "O VALOR DE SAQUE DEVER SER MAIOR QUE 0!")


def execSaque():
    global saldo
    if(txb_valorSaque.get() !=  "0"):
        float(txb_valorSaque.get().replace(",", "."))  
        msg = '{"id": "saque", "valor_saque":"'+txb_valorSaque.get().replace(",",".")+'"}'
        dados_dicionario = enviaRecebe(msg)
        if(dados_dicionario["id"] == "sucesso_saque"):
            saldo = "SALDO ATUAL: {}".format(dados_dicionario["saldo"])
            lbl_saldo.config(text = saldo)
            messagebox.showinfo("INFORMAÇÃO", dados_dicionario["mensagem"])
            saque.destroy()
        elif(dados_dicionario["id"] == "falha_saque"):
            messagebox.showerror("ERRO", dados_dicionario["mensagem"])
    else:
        messagebox.showerror("ERRO", "O VALOR DE SAQUE DEVER SER MAIOR QUE 0!")
    

def execTransacao():
    global saldo
    global list_transacao
    msg = '{"id": "transacao"}'
    conexao.send(msg.encode())
    dados = conexao.recv(1024)
    dados = dados.decode()
    cor = "#041c03"
    if(dados != 'sem_dados'):
        dados = dados.splitlines()
        for linha in dados:
            linha = ast.literal_eval(linha)
            if(linha["id"] == 'deposito'):
                operacao = 'D'
            elif(linha["id"] == 'saque'):
                operacao = 'S'
            list_transacao.insert(END, linha["data"] + ' | ' + operacao + ' | ' + linha["valor"] + ' | SALDO: ' + linha["saldo"])
            
            if(cor == "#041c03"):
                cor = "#0a2b08"
            elif(cor == "#0a2b08"):
                cor = "#041c03"

            list_transacao.itemconfig(END, {'bg':cor})
    else:
        transacao.destroy()
        messagebox.showerror("ERRO", "NENHUMA TRANSAÇÃO AINDA!")

def execAutenticacao():
    try:
        if(operacao == 'saque'):
            float(txb_valorSaque.get().replace(",", "."))  
        elif(operacao == 'deposito'):
            float(txb_valorDeposito.get().replace(",", "."))       
        msg = '{"id": "autenticacao", "senha":"'+txb_senhaAutenticacao.get()+'"}'
        dados_dicionario = enviaRecebe(msg)
        if(dados_dicionario["id"] == "autenticacao_aceita"):
            if(operacao == 'saque'):
                autenticacao.destroy()
                execSaque()
            elif(operacao == 'deposito'):
                autenticacao.destroy()
                execDeposito()
        elif(dados_dicionario["id"] == "autenticacao_rejeitada"):
            messagebox.showerror("ERRO", "FALHA NA AUTENTICAÇÃO.")

    except ValueError:
        if(operacao == 'saque'):
            txb_valorSaque.delete(0, END)
        elif(operacao == 'deposito'):
            txb_valorDeposito.delete(0, END)
        messagebox.showerror("ERRO", "INSIRA APENAS NÚMEROS!")

#telas
def telaLogin():
    global main
    global txb_usuario
    global txb_senha
    global btn_Login
    main = Tk()
    main.resizable(False, False)
    frame = Frame()
    frame.config(bg=bg_color)
    main.geometry("500x300+300+300")
    main.config(bg = bg_color)
    main.title("LOGIN - 303 BANK")
    
    lbl_login = Label(frame, text="LOGIN NO 303 BANK", bg=bg_color, fg=fg_color, font=("Courier New", 15))
    lbl_usuario = Label(frame, text="USUÁRIO", bg=bg_color, fg=fg_color, font=("Courier New", 12))
    txb_usuario = Entry(frame, bg='#0a2b08', fg=fg_color, font=("Courier New", 12), insertbackground=fg_color)
    lbl_senha = Label(frame, text="SENHA", bg=bg_color, fg=fg_color, font=("Courier New", 12))
    txb_senha = Entry(frame, bg='#0a2b08', fg=fg_color, show='•', font=("Courier New", 12), insertbackground=fg_color)
    btn_Login = Button(frame, text="LOGIN", command=execLogin, bg="#0a2b08", fg=fg_color, font=("Courier New", 12), activebackground=fg_color, width = 15)

    lbl_login.grid(row= 0, column=0, columnspan=3, pady = 30)
    lbl_usuario.grid(row = 1, column = 0)
    txb_usuario.grid(row = 1, column = 1, pady = 5)
    lbl_senha.grid(row=2, column=0)
    txb_senha.grid(row=2, column=1)
    btn_Login.grid(row=3, column=0, columnspan=3, pady = 30)
    
    frame.pack()
    
def telaMenu():
    global menu
    global lbl_saldo
    menu = Toplevel()
    menu.geometry("500x300")
    menu.config(bg=bg_color)
    menu.title("303 BANK")
    menu.resizable(False, False)
    frame = Frame(menu, bg=bg_color)
    lbl_303 = Label(frame, text='303 BANK', bg=bg_color, fg=fg_color, font=("Courier New", 20, "bold"))
    lbl_saldo = Label(frame, text='SALDO ATUAL: {}'.format(saldo), bg=bg_color, fg=fg_color, font=("Courier New", 12))
    btn_Deposito = Button(frame, text="DEPOSITO", command=telaDeposito, bg="#0a2b08", fg=fg_color, font=("Courier New", 12), width = 15, activebackground=fg_color)
    btn_Saque = Button(frame, text="SAQUE", command=telaSaque, bg='#0a2b08', fg=fg_color, font=("Courier New", 12), width = 15, activebackground=fg_color)
    btn_Transacao = Button(frame, text="VER TRANSAÇÕES", command=telaTransacao, bg='#0a2b08', fg=fg_color, font=("Courier New", 12), width = 15, activebackground=fg_color)
    btn_Sair = Button(frame, text="SAIR", command=execSair, bg="#0a2b08", fg=fg_color, font=("Courier New", 12), width = 15, activebackground=fg_color)
    
    lbl_303.grid(row=0, column=0)
    lbl_saldo.grid(row=1, column=0, pady=20)
    btn_Deposito.grid(row=2, column=0, columnspan=2, pady=2)
    btn_Saque.grid(row=3, column=0, columnspan=2, pady=2)
    btn_Transacao.grid(row=4, column=0, columnspan=2, pady=2)
    btn_Sair.grid(row=5, column=0,  pady=2)

    menu.protocol("WM_DELETE_WINDOW", main.destroy)

    frame.pack()
    
def telaDeposito():
    global txb_valorDeposito
    global deposito
    global operacao
    deposito = Toplevel()
    deposito.geometry("350x160")
    deposito.configure(bg = bg_color)
    deposito.title("303 BANK - DEPOSITO")
    deposito.resizable(False, False)
    frame = Frame(deposito)
    frame.config(bg=bg_color)
    lbl_deposito = Label(frame, text="DEPOSITAR", bg=bg_color, fg=fg_color, font=("Courier New", 15))
    label = Label(frame, text="VALOR: R$", bg=bg_color, fg=fg_color, font=("Courier New", 12))
    txb_valorDeposito = Entry(frame, bg='#0a2b08', fg=fg_color, font=("Courier New", 12), insertbackground=fg_color)
    btn_enviaDeposito = Button(frame, text="DEPOSITAR", command=telaAutenticacao, bg="#0a2b08", fg=fg_color, font=("Courier New", 12), width = 15, activebackground=fg_color)

    lbl_deposito.grid(row=0, column = 0, columnspan=2, pady=20)
    label.grid(row=1, column=0)
    txb_valorDeposito.grid(row=1, column=1)
    btn_enviaDeposito.grid(row=2, column=0, columnspan=2, pady=10)

    frame.pack()

    operacao = "deposito"

def telaSaque():
    global txb_valorSaque
    global saque
    global operacao
    saque = Toplevel()
    saque.geometry("350x160")
    saque.configure(bg = bg_color)
    saque.title("303 BANK - SAQUE")
    saque.resizable(False, False)
    frame = Frame(saque)
    frame.config(bg = bg_color)
    lbl_saque = Label(frame, text="SACAR", bg=bg_color, fg=fg_color, font=("Courier New", 15))
    label = Label(frame, text="VALOR: R$", bg=bg_color, fg=fg_color, font=("Courier New", 12))
    txb_valorSaque = Entry(frame, bg='#0a2b08', fg=fg_color, font=("Courier New", 12), insertbackground=fg_color)
    btn_enviaSaque = Button(frame, text="SACAR", command=telaAutenticacao, bg="#0a2b08", fg=fg_color, font=("Courier New", 12), width = 15, activebackground=fg_color)
    
    lbl_saque.grid(row=0, column=0, columnspan=2, pady=20)
    label.grid(row=1, column=0)
    txb_valorSaque.grid(row=1, column=1)
    btn_enviaSaque.grid(row=2, column=0, columnspan=2, pady=10)

    frame.pack()

    operacao = 'saque'

def telaTransacao():
    global list_transacao
    global transacao
    transacao = Toplevel()
    transacao.geometry("500x300")
    transacao.configure(bg = bg_color)
    transacao.title("303 BANK - TRANSAÇÕES")
    transacao.resizable(False, False)
    frame = Frame(transacao)
    frame.config(bg = bg_color)
    lbl_transacao = Label(frame, text="TRANSAÇÕES", bg=bg_color, fg=fg_color, font=("Courier New", 15, "bold"))
    list_transacao = Listbox(frame, bg='#0a2b08', fg=fg_color, font=("Courier New", 10), height=11, width=55)
    btn_Sair = Button(frame, text="SAIR", command=transacao.destroy, bg="#0a2b08", fg=fg_color, font=("Courier New", 12), width = 15, activebackground=fg_color)

    lbl_transacao.grid(row=0, column=0, pady=10)
    list_transacao.grid(row=1, column=0)
    btn_Sair.grid(row=2, column=0, pady=15)

    frame.pack()
    execTransacao()

def telaAutenticacao():
    global txb_senhaAutenticacao
    global autenticacao
    autenticacao = Toplevel()
    autenticacao.geometry("350x160")
    autenticacao.configure(bg = bg_color)
    autenticacao.title("303 BANK - AUTENTICAR")
    autenticacao.resizable(False, False)
    frame = Frame(autenticacao)
    frame.config(bg = bg_color)
    lbl_autenticar = Label(frame, text="AUTENTICAÇÃO", bg=bg_color, fg=fg_color, font=("Courier New", 15))
    label = Label(frame, text="SENHA: ", bg=bg_color, fg=fg_color, font=("Courier New", 12))
    txb_senhaAutenticacao = Entry(frame, bg='#0a2b08', show='•', fg=fg_color, font=("Courier New", 12), insertbackground=fg_color)
    btn_autenticar = Button(frame, text="AUTENTICAR", command=execAutenticacao, bg='#0a2b08', fg=fg_color, font=("Courier New", 12), width = 15, activebackground=fg_color)
    
    lbl_autenticar.grid(row=0, column=0, columnspan=2, pady=20)
    label.grid(row=1, column=0)
    txb_senhaAutenticacao.grid(row=1, column=1)
    btn_autenticar.grid(row=2, column=0, columnspan=2, pady=10)

    frame.pack()
   
def execSair():
    msg = '{"id": "sair"}'
    conexao.send(msg.encode())
    conexao.close()
    main.destroy()

telaLogin()

main.mainloop()