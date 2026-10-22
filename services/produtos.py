import mysql.connector
from database.banco_de_dados import BancoDeDados
from interface import InterfaceTerminal
from validadores import Validador


class GerenciadorProdutos:
    def __init__(self):
        self.banco = BancoDeDados()

    def cadastrar(self):
        InterfaceTerminal.exibir_titulo("CADASTRAR NOVO PRODUTO")
        nome = Validador.pedir_texto("Nome do Produto: ", "Nome", tamanho_maximo=100, obrigatorio=True)
        categoria = Validador.pedir_texto("Categoria (ex: Cerveja, Destilado, Refrigerante, Petisco): ", "Categoria", tamanho_maximo=50, obrigatorio=True)
        marca = Validador.pedir_texto("Marca / Fabricante (opcional): ", "Marca", tamanho_maximo=50, obrigatorio=False)
        preco = Validador.pedir_preco("Preço unitário (R$): ")
        estoque = Validador.pedir_inteiro("Quantidade inicial em estoque: ", "Estoque", valor_minimo=0)
        id_fornecedor = Validador.pedir_inteiro("ID do fornecedor: ", "ID do fornecedor", valor_minimo=1)

        fornecedor = self.banco.consultar("SELECT id_fornecedor, nome FROM fornecedor WHERE id_fornecedor = %s", (id_fornecedor,))
        if not fornecedor:
            InterfaceTerminal.erro(f"Fornecedor com ID {id_fornecedor} não encontrado. Cadastre o fornecedor primeiro.")
            InterfaceTerminal.pausar()
            return

        print(f"\nFornecedor selecionado: {fornecedor[0][1]}")

        comando_sql = """
            INSERT INTO produto (nome, categoria, marca, preco, estoque, id_fornecedor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.banco.executar(
                comando_sql,
                (nome, categoria, marca, preco, estoque, id_fornecedor),
            )
            InterfaceTerminal.sucesso("Produto cadastrado com sucesso!")
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
        InterfaceTerminal.pausar()

    def atualizar_preco(self):
        InterfaceTerminal.exibir_titulo("ATUALIZAR PREÇO DO PRODUTO")
        id_produto = Validador.pedir_inteiro("ID do produto: ", "ID do produto", valor_minimo=1)

        produto = self.banco.consultar("SELECT id_produto, nome, preco FROM produto WHERE id_produto = %s", (id_produto,))
        if not produto:
            InterfaceTerminal.aviso(f"Nenhum produto encontrado com o ID {id_produto}.")
            InterfaceTerminal.pausar()
            return

        print(f"\nProduto: {produto[0][1]} | Preço atual: R$ {float(produto[0][2]):.2f}\n")
        digitado = input("Novo preço unitário (R$) [ENTER para manter]: ").strip()
        if not digitado:
            InterfaceTerminal.aviso("Preço mantido sem alterações.")
            InterfaceTerminal.pausar()
            return

        valido, novo_preco = Validador.validar_preco(digitado)
        if not valido:
            InterfaceTerminal.erro(novo_preco)
            InterfaceTerminal.pausar()
            return

        comando_sql = "UPDATE produto SET preco = %s WHERE id_produto = %s"
        try:
            self.banco.executar(comando_sql, (novo_preco, id_produto))
            InterfaceTerminal.sucesso(f"Preço atualizado para R$ {novo_preco:.2f} com sucesso!")
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
        InterfaceTerminal.pausar()

    def atualizar_estoque(self):
        InterfaceTerminal.exibir_titulo("ATUALIZAR ESTOQUE DO PRODUTO")
        id_produto = Validador.pedir_inteiro("ID do produto: ", "ID do produto", valor_minimo=1)

        produto = self.banco.consultar("SELECT id_produto, nome, estoque FROM produto WHERE id_produto = %s", (id_produto,))
        if not produto:
            InterfaceTerminal.aviso(f"Nenhum produto encontrado com o ID {id_produto}.")
            InterfaceTerminal.pausar()
            return

        print(f"\nProduto: {produto[0][1]} | Estoque atual: {produto[0][2]} unidade(s)\n")
        digitado = input("Nova quantidade total em estoque [ENTER para manter]: ").strip()
        if not digitado:
            InterfaceTerminal.aviso("Estoque mantido sem alterações.")
            InterfaceTerminal.pausar()
            return

        valido, novo_estoque = Validador.validar_inteiro(digitado, "Estoque", valor_minimo=0)
        if not valido:
            InterfaceTerminal.erro(novo_estoque)
            InterfaceTerminal.pausar()
            return

        comando_sql = "UPDATE produto SET estoque = %s WHERE id_produto = %s"
        try:
            self.banco.executar(comando_sql, (novo_estoque, id_produto))
            InterfaceTerminal.sucesso(f"Estoque atualizado para {novo_estoque} unidade(s) com sucesso!")
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
        InterfaceTerminal.pausar()

    def remover(self):
        InterfaceTerminal.exibir_titulo("REMOVER PRODUTO")
        id_produto = Validador.pedir_inteiro("ID do produto a ser removido: ", "ID do produto", valor_minimo=1)

        produto = self.banco.consultar("SELECT id_produto, nome FROM produto WHERE id_produto = %s", (id_produto,))
        if not produto:
            InterfaceTerminal.aviso(f"Nenhum produto encontrado com o ID {id_produto}.")
            InterfaceTerminal.pausar()
            return

        confirmacao = input(f"\nTem certeza que deseja remover o produto '{produto[0][1]}'? (S/N): ").strip().upper()
        if confirmacao != "S":
            InterfaceTerminal.aviso("Operação cancelada pelo usuário.")
            InterfaceTerminal.pausar()
            return

        comando_sql = "DELETE FROM produto WHERE id_produto = %s"
        try:
            self.banco.executar(comando_sql, (id_produto,))
            InterfaceTerminal.sucesso(f"Produto '{produto[0][1]}' removido com sucesso!")
        except mysql.connector.Error as erro:
            if erro.errno == 1451:
                InterfaceTerminal.erro("Este produto não pode ser removido pois já possui histórico em pedidos.")
            else:
                InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
        InterfaceTerminal.pausar()

    def listar(self):
        InterfaceTerminal.exibir_titulo("PRODUTOS DISPONÍVEIS EM ESTOQUE")
        comando_sql = """
            SELECT produto.id_produto, produto.nome, produto.categoria, produto.marca, 
                   produto.preco, produto.estoque, fornecedor.nome
            FROM produto
            INNER JOIN fornecedor ON fornecedor.id_fornecedor = produto.id_fornecedor
            WHERE produto.estoque > 0
            ORDER BY produto.nome
        """
        try:
            produtos = self.banco.consultar(comando_sql)
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
            InterfaceTerminal.pausar()
            return

        if not produtos:
            InterfaceTerminal.aviso("Nenhum produto com estoque disponível no momento.")
            InterfaceTerminal.pausar()
            return

        cabecalhos = ["ID", "NOME DO PRODUTO", "CATEGORIA", "MARCA", "PREÇO (R$)", "ESTOQUE", "FORNECEDOR"]
        linhas = []
        for p in produtos:
            linhas.append([
                p[0],
                p[1],
                p[2],
                p[3] if p[3] else "Sem marca",
                f"R$ {float(p[4]):.2f}",
                f"{p[5]} un",
                p[6],
            ])

        InterfaceTerminal.exibir_tabela(cabecalhos, linhas)
        InterfaceTerminal.pausar()
