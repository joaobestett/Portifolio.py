from tkinter import messagebox, filedialog
import tkinter as tk
import bcrypt
import pymongo
from ttkthemes import ThemedTk
import pandas as pd
from pymongo import MongoClient


client = MongoClient("mongodb+srv://eueeu:*******.@teste.xxclhzb.mongodb.net/?retryWrites=true&w=majority&appName=Teste")
db = client.Users
collection_users = db.Users
collection_products = db.Products


def validar_entrada_usuario(nome, email, senha):
    if not nome or not email or not senha:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return False
    return True

def hash_senha(senha):
    salt = bcrypt.gensalt()
    senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return senha_hashed

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


def adicionar_usuario(nome, email, senha):
    usuario = {
        "nome": nome,
        "email": email,
        "senha": senha
    }
    try:
        result = collection_users.insert_one(usuario)
        messagebox.showinfo("Sucesso", f'Usuário adicionado com ID: {result.inserted_id}')
    except pymongo.errors.DuplicateKeyError:
        messagebox.showerror("Erro", "O email fornecido já está em uso.")

def visualizar_usuarios():
    usuarios = list(collection_users.find())
    return usuarios

def buscar_usuario(email):
    usuario = collection_users.find_one({"email": email})
    if usuario:
        return usuario
    else:
        messagebox.showerror("Erro", "Usuário não encontrado")
        return None

def remover_usuario(email):
    result = collection_users.delete_one({"email": email})
    if result.deleted_count:
        messagebox.showinfo("Sucesso", "Usuário removido com sucesso.")
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")

def atualizar_usuario(email, novo_nome, nova_senha):
    nova_senha_hashed = hash_senha(nova_senha)
    result = collection_users.update_one(
        {"email": email},
        {"$set": {"nome": novo_nome, "senha": nova_senha_hashed}}
    )
    if result.matched_count:
        messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
    else:
        messagebox.showerror("Erro", "Usuário não encontrado")


def adicionar_produto(nome, preco, marca, modelo, quantidade):
    produto = {
        "nome": nome,
        "preco": float(preco),
        "marca": marca,
        "modelo": modelo,
        "quantidade": int(quantidade)
    }
    result = collection_products.insert_one(produto)
    messagebox.showinfo("Sucesso", f'Produto adicionado com ID: {result.inserted_id}')

def visualizar_produtos():
    produtos = list(collection_products.find())
    return produtos

def buscar_produto(nome):
    produto = collection_products.find_one({"nome": nome})
    if produto:
        return produto
    else:
        messagebox.showerror("Erro", "Produto não encontrado")
        return None

def remover_produto(nome):
    result = collection_products.delete_one({"nome": nome})
    if result.deleted_count:
        messagebox.showinfo("Sucesso", "Produto removido com sucesso.")
    else:
        messagebox.showerror("Erro", "Produto não encontrado.")

def atualizar_produto(nome, novo_preco, nova_marca, novo_modelo, nova_quantidade):
    try:
        result = collection_products.update_one(
            {"nome": nome},
            {"$set": {
                "preco": float(novo_preco),
                "marca": nova_marca,
                "modelo": novo_modelo,
                "quantidade": int(nova_quantidade)
            }}
        )
        if result.matched_count:
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Produto não encontrado")
    except ValueError:
        messagebox.showerror("Erro", "Preço deve ser um número e quantidade deve ser um inteiro.")


def adicionar_usuario_gui():
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()
    if validar_entrada_usuario(nome, email, senha):
        senha_hashed = hash_senha(senha)
        adicionar_usuario(nome, email, senha_hashed)

def visualizar_usuarios_gui():
    usuarios = visualizar_usuarios()
    lista_usuarios.delete(0, tk.END)
    for usuario in usuarios:
        lista_usuarios.insert(tk.END, f'ID: {usuario["_id"]}, Nome: {usuario["nome"]}, Email: {usuario["email"]}')

def buscar_usuario_gui():
    email = entry_email.get()
    usuario = buscar_usuario(email)
    if usuario:
        messagebox.showinfo("Usuário Encontrado",
                            f'ID: {usuario["_id"]}\nNome: {usuario["nome"]}\nEmail: {usuario["email"]}')
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")

def remover_usuario_gui():
    email = entry_email.get()
    remover_usuario(email)

def atualizar_usuario_gui():
    email = entry_email.get()
    nome = entry_nome.get()
    senha = entry_senha.get()
    atualizar_usuario(email, nome, senha)


def adicionar_produto_gui():
    nome = entry_nome_produto.get()
    preco = entry_preco_produto.get()
    marca = entry_marca_produto.get()
    modelo = entry_modelo_produto.get()
    quantidade = entry_quantidade_produto.get()
    if validar_entrada_produto(nome, preco, marca, modelo, quantidade):
        adicionar_produto(nome, preco, marca, modelo, quantidade)

def visualizar_produtos_gui():
    produtos = visualizar_produtos()
    lista_produtos.delete(0, tk.END)
    for produto in produtos:
        lista_produtos.insert(tk.END, f'ID: {produto["_id"]}, Nome: {produto["nome"]}, Preço: {produto["preco"]}, Marca: {produto["marca"]}, Modelo: {produto["modelo"]}, Quantidade: {produto["quantidade"]}')

def buscar_produto_gui():
    nome = entry_nome_produto.get()
    produto = buscar_produto(nome)
    if produto:
        messagebox.showinfo("Produto Encontrado",
                            f'ID: {produto["_id"]}\nNome: {produto["nome"]}\nPreço: {produto["preco"]}\nMarca: {produto["marca"]}\nModelo: {produto["modelo"]}\nQuantidade: {produto["quantidade"]}')
    else:
        messagebox.showerror("Erro", "Produto não encontrado.")

def remover_produto_gui():
    nome = entry_nome_produto.get()
    remover_produto(nome)

def atualizar_produto_gui():
    nome = entry_nome_produto.get()
    preco = entry_preco_produto.get()
    marca = entry_marca_produto.get()
    modelo = entry_modelo_produto.get()
    quantidade = entry_quantidade_produto.get()
    atualizar_produto(nome, preco, marca, modelo, quantidade)

def exportar_para_csv():
    usuarios = visualizar_usuarios()
    produtos = visualizar_produtos()

    df_usuarios = pd.DataFrame(usuarios)
    df_produtos = pd.DataFrame(produtos)

    df_usuarios.to_csv('usuarios_exportados.csv', index=False)
    df_produtos.to_csv('produtos_exportados.csv', index=False)

    messagebox.showinfo("Sucesso", "Dados exportados com sucesso para 'usuarios_exportados.csv' e 'produtos_exportados.csv'")

def importar_de_csv():
    filepath_usuarios = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Selecione o arquivo CSV de Usuários")
    if not filepath_usuarios:
        return

    filepath_produtos = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Selecione o arquivo CSV de Produtos")
    if not filepath_produtos:
        return

    try:
        df_usuarios = pd.read_csv(filepath_usuarios)
        df_produtos = pd.read_csv(filepath_produtos)

        for _, row in df_usuarios.iterrows():
            adicionar_usuario(row['nome'], row['email'], row['senha'])

        for _, row in df_produtos.iterrows():
            adicionar_produto(row['nome'], row['preco'], row['marca'], row['modelo'], row['quantidade'])

        messagebox.showinfo("Sucesso", "Dados importados com sucesso do arquivo CSV.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao importar dados: {e}")


root = ThemedTk(theme="arc")
root.title("Sistema de Cadastro de Usuários e Produtos")


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


tk.Button(root, text="Exportar para CSV", command=exportar_para_csv).grid(row=20, column=0, columnspan=2, pady=5)
tk.Button(root, text="Importar de CSV", command=importar_de_csv).grid(row=21, column=0, columnspan=2, pady=5)


root.mainloop()


client.close()