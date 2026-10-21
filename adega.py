import os
from typing import Any, cast

import mysql.connector

def conectar():
    return mysql.connector.connect(
        host=os.getenv("ADEGA_DB_HOST", "localhost"),
        port=int(os.getenv("ADEGA_DB_PORT", "3306")),
        user=os.getenv("ADEGA_DB_USER", "root"),
        password=os.getenv("ADEGA_DB_PASSWORD", ""),
        database=os.getenv("ADEGA_DB_NAME", "adega")
    )

def executar(sql, parametros=()):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(sql, parametros)
    conexao.commit()
    conexao.close()

def consultar(sql: str, parametros: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(sql, parametros)
    resultados = cast(list[tuple[Any, ...]], cursor.fetchall())
    conexao.close()
    return resultados



def cadastrar_cliente():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")
    
    sql = "INSERT INTO cliente (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)"
    executar(sql, (nome, cpf, telefone, email))
    print("Cliente cadastrado com sucesso!")

def listar_clientes():
    sql = """
        SELECT id_cliente, nome, cpf, telefone, email
        FROM cliente
        ORDER BY nome
    """
    clientes = consultar(sql)

    if not clientes:
        print("\nNenhum cliente cadastrado.")
        return

    print("\n--- Clientes Cadastrados ---")
    for cliente in clientes:
        print(
            f"ID: {cliente[0]} | Nome: {cliente[1]} | "
            f"CPF: {cliente[2]} | Telefone: {cliente[3] or 'N/A'} | "
            f"E-mail: {cliente[4] or 'N/A'}"
        )

def atualizar_cliente():
    id_cliente = int(input("ID do cliente a atualizar: "))
    nome = input("Novo Nome: ")
    telefone = input("Novo Telefone: ")
    email = input("Novo E-mail: ")
    
    sql = "UPDATE cliente SET nome = %s, telefone = %s, email = %s WHERE id_cliente = %s"
    executar(sql, (nome, telefone, email, id_cliente))
    print("Dados do cliente atualizados com sucesso!")

def cadastrar_endereco():
    id_cliente = int(input("ID do cliente: "))
    rua = input("Rua: ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    complemento = input("Complemento (opcional): ")
    cep = input("CEP: ")
    
    sql = """
        INSERT INTO endereco (id_cliente, rua, numero, bairro, cidade, complemento, cep)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    executar(sql, (id_cliente, rua, numero, bairro, cidade, complemento or None, cep))
    print("Endereço cadastrado com sucesso!")

def atualizar_endereco():
    id_cliente = int(input("ID do cliente dono do endereço: "))
    rua = input("Nova Rua: ")
    numero = input("Novo Número: ")
    bairro = input("Novo Bairro: ")
    cidade = input("Nova Cidade: ")
    complemento = input("Novo Complemento: ")
    cep = input("Novo CEP: ")
    
    sql = """
        UPDATE endereco 
        SET rua = %s, numero = %s, bairro = %s, cidade = %s, complemento = %s, cep = %s 
        WHERE id_cliente = %s
    """
    executar(sql, (rua, numero, bairro, cidade, complemento or None, cep, id_cliente))
    print("Endereço atualizado com sucesso!")

def consultar_endereco_cliente():
    id_cliente = int(input("ID do cliente para buscar o endereço: "))
    
    sql = """
        SELECT c.nome, e.rua, e.numero, e.bairro, e.cidade, e.complemento, e.cep
        FROM endereco AS e
        INNER JOIN cliente AS c ON c.id_cliente = e.id_cliente
        WHERE e.id_cliente = %s
    """
    resultados = consultar(sql, (id_cliente,))
    
    if resultados:
        print("\n--- Endereço Encontrado ---")
        for linha in resultados:
            print(f"Cliente: {linha[0]}")
            print(f"Rua: {linha[1]}, Nº {linha[2]}")
            print(f"Bairro: {linha[3]} | Cidade: {linha[4]}")
            print(f"Complemento: {linha[5] or 'N/A'}")
            print(f"CEP: {linha[6]}")
    else:
        print("\nNenhum endereço encontrado para este cliente.")


def cadastrar_fornecedor():
    nome = input("Nome: ")
    cnpj = input("CNPJ: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")
    
    sql = "INSERT INTO fornecedor (nome, cnpj, telefone, email) VALUES (%s, %s, %s, %s)"
    executar(sql, (nome, cnpj, telefone, email))
    print("Fornecedor cadastrado com sucesso!")

def listar_fornecedores():
    sql = """
        SELECT id_fornecedor, nome, cnpj, telefone, email
        FROM fornecedor
        ORDER BY nome
    """
    fornecedores = consultar(sql)

    if not fornecedores:
        print("\nNenhum fornecedor cadastrado.")
        return

    print("\n--- Fornecedores Cadastrados ---")
    for fornecedor in fornecedores:
        print(
            f"ID: {fornecedor[0]} | Nome: {fornecedor[1]} | "
            f"CNPJ: {fornecedor[2] or 'N/A'} | "
            f"Telefone: {fornecedor[3] or 'N/A'} | "
            f"E-mail: {fornecedor[4] or 'N/A'}"
        )

def atualizar_fornecedor():
    id_fornecedor = int(input("ID do fornecedor a atualizar: "))
    nome = input("Novo Nome: ")
    telefone = input("Novo Telefone: ")
    email = input("Novo E-mail: ")
    
    sql = "UPDATE fornecedor SET nome = %s, telefone = %s, email = %s WHERE id_fornecedor = %s"
    executar(sql, (nome, telefone, email, id_fornecedor))
    print("Dados do fornecedor atualizados com sucesso!")


def cadastrar_produto():
    nome = input("Nome: ")
    categoria = input("Categoria: ")
    marca = input("Marca: ")
    preco = float(input("Preço: ").replace(",", "."))
    estoque = int(input("Estoque: "))
    fornecedor = int(input("ID do fornecedor: "))
    
    sql = """
        INSERT INTO produto (nome, categoria, marca, preco, estoque, id_fornecedor)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    executar(sql, (nome, categoria, marca, preco, estoque, fornecedor))
    print("Produto cadastrado com sucesso!")

def atualizar_preco_produto():
    produto = int(input("ID do produto: "))
    novo_preco = float(input("Novo preço: ").replace(",", "."))
    
    sql = "UPDATE produto SET preco = %s WHERE id_produto = %s"
    executar(sql, (novo_preco, produto))
    print("Preço do produto atualizado com sucesso!")

def atualizar_estoque():
    produto = int(input("ID do produto: "))
    estoque = int(input("Novo estoque: "))
    
    sql = "UPDATE produto SET estoque = %s WHERE id_produto = %s"
    executar(sql, (estoque, produto))
    print("Estoque atualizado!")

def remover_produto():
    produto = int(input("ID do produto: "))
    
    sql = "DELETE FROM produto WHERE id_produto = %s"
    executar(sql, (produto,))
    print("Produto removido!")

def listar_produtos():
    sql = """
        SELECT p.id_produto, p.nome, p.categoria, p.marca, p.preco,
               p.estoque, f.nome AS fornecedor
        FROM produto AS p
        INNER JOIN fornecedor AS f ON f.id_fornecedor = p.id_fornecedor
        WHERE p.estoque > 0
        ORDER BY p.nome
    """
    linhas = consultar(sql)
    print("\n--- Produtos Encontrados ---")
    for linha in linhas:
        print(linha)


def atualizar_status_pedido():
    id_pedido = int(input("ID do pedido: "))
    novo_status = input("Novo Status (ex: Pago, Enviado, Cancelado): ")
    
    sql = "UPDATE pedido SET status = %s WHERE id_pedido = %s"
    executar(sql, (novo_status, id_pedido))
    print("Status do pedido atualizado!")

def listar_pedidos():
    sql = """
        SELECT pe.id_pedido, c.nome AS cliente, pe.status, pe.valor_total,
               COUNT(ip.id_produto) AS itens
        FROM pedido AS pe
        INNER JOIN cliente AS c ON c.id_cliente = pe.id_cliente
        LEFT JOIN item_pedido AS ip ON ip.id_pedido = pe.id_pedido
        WHERE pe.status <> 'Cancelado'
        GROUP BY pe.id_pedido, c.nome, pe.status, pe.valor_total
        ORDER BY pe.data_pedido DESC
    """
    linhas = consultar(sql)
    print("\n--- Pedidos Encontrados ---")
    for linha in linhas:
        print(linha)

def menu():
    while True:
        print("\n" + "="*45)
        print("             SISTEMA DE ADEGA")
        print("="*45)
        print(" [ 1 ] Cadastrar Cliente")
        print(" [ 2 ] Atualizar Cliente")
        print(" [ 3 ] Listar clientes e seus IDs")
        print("\n [ 4 ] Cadastrar Endereço")
        print(" [ 5 ] Atualizar Endereço")
        print(" [ 6 ] Consultar Endereço de Cliente")
        print("\n [ 7 ] Cadastrar Fornecedor")
        print(" [ 8 ] Atualizar Fornecedor")
        print(" [ 9 ] Listar fornecedores e seus IDs")
        print("\n [ 10 ] Cadastrar Produto")
        print(" [ 11 ] Atualizar Preço do Produto")
        print(" [ 12 ] Atualizar Estoque do Produto")
        print(" [ 13 ] Remover Produto")
        print("\n [ 14 ] Consultar Produtos")
        print(" [ 15 ] Atualizar Status de Pedido")
        print(" [ 16 ] Consultar Pedidos")
        print("-" * 45)
        print(" [ 0 ] Sair do Sistema")
        print("="*45)
        
        escolha = input("\n Escolha uma opção: ").strip()
        
        if escolha == "0":
            print("\nA encerrar o sistema...\n")
            break
        elif escolha == "1":
            cadastrar_cliente()
        elif escolha == "2":
            atualizar_cliente()
        elif escolha == "3":
            listar_clientes()
        elif escolha == "4":
            cadastrar_endereco()
        elif escolha == "5":
            atualizar_endereco()
        elif escolha == "6":
            consultar_endereco_cliente()
        elif escolha == "7":
            cadastrar_fornecedor()
        elif escolha == "8":
            atualizar_fornecedor()
        elif escolha == "9":
            listar_fornecedores()
        elif escolha == "10":
            cadastrar_produto()
        elif escolha == "11":
            atualizar_preco_produto()
        elif escolha == "12":
            atualizar_estoque()
        elif escolha == "13":
            remover_produto()
        elif escolha == "14":
            listar_produtos()
        elif escolha == "15":
            atualizar_status_pedido()
        elif escolha == "16":
            listar_pedidos()
        else:
            print("\n Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    menu()