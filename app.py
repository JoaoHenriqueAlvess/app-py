#app.py
from decimal import Decimal
from models import create_session, Cliente, Produto, Pedido, ItemPedido

DB_URL = "sqlite:///loja_jogos.db"
session = create_session(DB_URL)

def cadastrar_Cliente():
    nome = input("Nome do Cliente: ").strip()
    email = input("Email do Cliente: ").strip()
    telefone = input("Telefone do CLiente: ").strip() or None
    
    cliente = Cliente(nome=nome, email=email, telefone=telefone)
    session.add(cliente)
    session.commit()
    print(F"Cliente Cadastrado: {cliente}")

def cadastrar_produto():
    nome_produto = input("Nome do Produto: ").strip()
    preco = Decimal(input("Preço do Produto (Ex: 199.99): ")).replace(",", ".")
    estoque = int(input("Estoque: "))

    produto = Produto(nome_produto=nome_produto, preco=preco, estoque=estoque)
    session.add(produto)
    session.commit()
    print(F"Produto Cadastrado: {nome_produto}")

def criar_pedido():
    cliente_id = int(input("Digite o ID ao cliente: "))
    pedido = Pedido(cliente_id=cliente_id)
    session.add(pedido)
    session.flush() #garante o id do pedido antes antes de insetir o pedido
    
    print("Adicione items (Entes em produto_ID para finalizar) :")
    while True:
        val = input("Produto ID(Entes para sair ): ").strip()
        if not val:
           break
        produto_id = int(val)
        quantidade = int(input("Quantidade: "))
 
       #Buscar produto para pegar preço e validar o estoque 
       produto = session.get(Produto, produto_id)
    
       if produto is None:
          print("Produto não encontrado.")
          continue 
    
        if produto.estoque < quantidade:
          print(F"Estoque insuficiente. Quantidade Disponivel: {produto.estoque}")

    #debita do estoaue
    produto.estoque -= quantidade 

    item = itemPedido(
        pedido_id = pedido.id,
        produto_id = produto_id,
        quantidade = quantidade,
        preco_unit = produto.preco

    )
    session.add(item)
session.commit()
