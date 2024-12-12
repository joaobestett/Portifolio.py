import re
import bcrypt
from tkinter import messagebox

def validar_entrada_usuario(nome, email, senha):
    if not nome or not email or not senha:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return False
    if not validar_email(email):
        messagebox.showerror("Erro", "Email inválido.")
        return False
    return True

def validar_email(email):
    return re.match(r'^[^@]+@[^@]+\\.[^@]+$', email) is not None

def hash_senha(senha):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt)

def validar_entrada_produto(nome, preco, marca, modelo, quantidade):
    if not nome or not preco or not marca or not modelo or not quantidade:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return False
    try:
        float(preco)
        int(quantidade)
    except ValueError:
        messagebox.showerror("Erro", "Preço deve ser um número e quantidade deve ser um inteiro.")
        return False
    return True

def exibir_mensagem(tipo, mensagem):
    if tipo == "erro":
        messagebox.showerror("Erro", mensagem)
    else:
        messagebox.showinfo("Sucesso", mensagem)