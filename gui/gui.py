from tkinter import messagebox, filedialog
import tkinter as tk
from ttkthemes import ThemedTk
from database.database import Database
from utils.utils import validar_entrada_usuario, validar_entrada_produto, hash_senha

db = Database()

def adicionar_usuario_gui():
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()
    if validar_entrada_usuario(nome, email, senha):
        senha_hashed = hash_senha(senha)
        try:
            db.add_user({"nome": nome, "email": email, "senha": senha_hashed})
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

def visualizar_usuarios_gui():
    usuarios = db.get_users()
    lista_usuarios.delete(0, tk.END)
    for usuario in usuarios:
        lista_usuarios.insert(tk.END, f'ID: {usuario["_id"]}, Nome: {usuario["nome"]}, Email: {usuario["email"]}')

def buscar_usuario_gui():
    email = entry_email.get()
    usuario = db.get_user_by_email(email)
    if usuario:
        messagebox.showinfo("Usuário Encontrado",
                            f'ID: {usuario["_id"]}\nNome: {usuario["nome"]}\nEmail: {usuario["email"]}')
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")

def remover_usuario_gui():
    email = entry_email.get()
    result = db.delete_user(email)
    if result.deleted_count:
        messagebox.showinfo("Sucesso", "Usuário removido com sucesso.")
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")

def atualizar_usuario_gui():
    email = entry_email.get()
    nome = entry_nome.get()
    senha = entry_senha.get()
    updates = {"nome": nome}
    if senha:
        updates["senha"] = hash_senha(senha)
    result = db.update_user(email, updates)
    if result.matched_count:
        messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")

def adicionar_produto_gui():
    nome = entry_nome_produto.get()
    preco = entry_preco_produto.get()
    marca = entry_marca_produto.get()
    modelo = entry_modelo_produto.get()
    quantidade = entry_quantidade_produto.get()
    if validar_entrada_produto(nome, preco, marca, modelo, quantidade):
        try:
            db.add_product({
                "nome": nome,
                "preco": float(preco),
                "marca": marca,
                "modelo": modelo,
                "quantidade": int(quantidade)
            })
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

def visualizar_produtos_gui():
    produtos = db.get_products()
    lista_produtos.delete(0, tk.END)
    for produto in produtos:
        lista_produtos.insert(tk.END, f'ID: {produto["_id"]}, Nome: {produto["nome"]}, Preço: {produto["preco"]}, Marca: {produto["marca"]}, Modelo: {produto["modelo"]}, Quantidade: {produto["quantidade"]}')

def buscar_produto_gui():
    nome = entry_nome_produto.get()
    produto = db.get_product_by_name(nome)
    if produto:
        messagebox.showinfo("Produto Encontrado",
                            f'ID: {produto["_id"]}\nNome: {produto["nome"]}\nPreço: {produto["preco"]}\nMarca: {produto["marca"]}\nModelo: {produto["modelo"]}\nQuantidade: {produto["quantidade"]}')
    else:
        messagebox.showerror("Erro", "Produto não encontrado.")

def remover_produto_gui():
    nome = entry_nome_produto.get()
    result = db.delete_product(nome)
    if result.deleted_count:
        messagebox.showinfo("Sucesso", "Produto removido com sucesso.")
    else:
        messagebox.showerror("Erro", "Produto não encontrado.")

def atualizar_produto_gui():
    nome = entry_nome_produto.get()
    preco = entry_preco_produto.get()
    marca = entry_marca_produto.get()
    modelo = entry_modelo_produto.get()
    quantidade = entry_quantidade_produto.get()
    updates = {
        "preco": float(preco),
        "marca": marca,
        "modelo": modelo,
        "quantidade": int(quantidade)
    }
    result = db.update_product(nome, updates)
    if result.matched_count:
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
    else:
        messagebox.showerror("Erro", "Produto não encontrado.")

# GUI Components
root = ThemedTk(theme="arc")
root.title("Sistema de Cadastro de Usuários e Produtos")

# User Section
tk.Label(root, text="Nome").grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Email").grid(row=1, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Senha").grid(row=2, column=0)
entry_senha = tk.Entry(root, show='*')
entry_senha.grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Adicionar Usuário", command=adicionar_usuario_gui).grid(row=3, column=0, columnspan=2, pady=5)
tk.Button(root, text="Visualizar Usuários", command=visualizar_usuarios_gui).grid(row=4, column=0, columnspan=2, pady=5)
tk.Button(root, text="Buscar Usuário", command=buscar_usuario_gui).grid(row=5, column=0, columnspan=2, pady=5)
tk.Button(root, text="Remover Usuário", command=remover_usuario_gui).grid(row=6, column=0, columnspan=2, pady=5)
tk.Button(root, text="Atualizar Usuário", command=atualizar_usuario_gui).grid(row=7, column=0, columnspan=2, pady=5)

lista_usuarios = tk.Listbox(root, width=50)
lista_usuarios.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# Product Section
tk.Label(root, text="Nome do Produto").grid(row=9, column=0)
entry_nome_produto = tk.Entry(root)
entry_nome_produto.grid(row=9, column=1, padx=5, pady=5)

tk.Label(root, text="Preço").grid(row=10, column=0)
entry_preco_produto = tk.Entry(root)
entry_preco_produto.grid(row=10, column=1, padx=5, pady=5)

tk.Label(root, text="Marca").grid(row=11, column=0)
entry_marca_produto = tk.Entry(root)
entry_marca_produto.grid(row=11, column=1, padx=5, pady=5)

tk.Label(root, text="Modelo").grid(row=12, column=0)
entry_modelo_produto = tk.Entry(root)
entry_modelo_produto.grid(row=12, column=1, padx=5, pady=5)

tk.Label(root, text="Quantidade").grid(row=13, column=0)
entry_quantidade_produto = tk.Entry(root)
entry_quantidade_produto.grid(row=13, column=1, padx=5, pady=5)

tk.Button(root, text="Adicionar Produto", command=adicionar_produto_gui).grid(row=14, column=0, columnspan=2, pady=5)
tk.Button(root, text="Visualizar Produtos", command=visualizar_produtos_gui).grid(row=15, column=0, columnspan=2, pady=5)
tk.Button(root, text="Buscar Produto", command=buscar_produto_gui).grid(row=16, column=0, columnspan=2, pady=5)
tk.Button(root, text="Remover Produto", command=remover_produto_gui).grid(row=17, column=0, columnspan=2, pady=5)
tk.Button(root, text="Atualizar Produto", command=atualizar_produto_gui).grid(row=18, column=0, columnspan=2, pady=5)


lista_produtos = tk.Listbox(root, width=50)
lista_produtos.grid(row=19, column=0, columnspan=2, padx=5, pady=5)
