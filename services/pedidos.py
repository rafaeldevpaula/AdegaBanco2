import mysql.connector
from database.banco_de_dados import BancoDeDados
from interface import InterfaceTerminal
from validadores import Validador


class GerenciadorPedidos:
    def __init__(self):
        self.banco = BancoDeDados()

    def cadastrar(self):
        InterfaceTerminal.exibir_titulo("CADASTRAR NOVO PEDIDO")
        id_cliente = Validador.pedir_inteiro("ID do cliente comprador: ", "ID do cliente", valor_minimo=1)

        cliente = self.banco.consultar("SELECT id_cliente, nome FROM cliente WHERE id_cliente = %s", (id_cliente,))
        if not cliente:
            InterfaceTerminal.erro(f"Cliente com ID {id_cliente} não encontrado.")
            InterfaceTerminal.pausar()
            return

        print(f"\nCliente selecionado: {cliente[0][1]}")

        conexao = self.banco.conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO pedido (id_cliente, status, valor_total) VALUES (%s, 'Pendente', 0.00)",
            (id_cliente,),
        )
        id_pedido = cursor.lastrowid
        conexao.commit()
        cursor.close()
        conexao.close()

        valor_total = 0.0
        itens_adicionados = 0

        while True:
            print(f"\n--- Adicionar Item ao Pedido #{id_pedido} ---")
            id_produto = Validador.pedir_inteiro("ID do produto: ", "ID do produto", valor_minimo=1)
            produto = self.banco.consultar(
                "SELECT id_produto, nome, preco, estoque FROM produto WHERE id_produto = %s",
                (id_produto,),
            )

            if not produto:
                InterfaceTerminal.aviso("Produto não encontrado.")
            elif produto[0][3] <= 0:
                InterfaceTerminal.aviso(f"O produto '{produto[0][1]}' está com estoque esgotado!")
            else:
                nome_prod = produto[0][1]
                preco_prod = float(produto[0][2])
                estoque_prod = produto[0][3]
                print(f"Produto: {nome_prod} | Preço: R$ {preco_prod:.2f} | Estoque disponível: {estoque_prod} un")

                qtd = Validador.pedir_inteiro(
                    f"Quantidade (máx {estoque_prod}): ", "Quantidade", valor_minimo=1
                )
                if qtd > estoque_prod:
                    InterfaceTerminal.aviso(f"Quantidade indisponível. Estoque disponível: {estoque_prod} unidades.")
                else:
                    subtotal = preco_prod * qtd
                    try:
                        self.banco.executar(
                            "INSERT INTO item_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)",
                            (id_pedido, id_produto, qtd, preco_prod),
                        )
                        self.banco.executar(
                            "UPDATE produto SET estoque = estoque - %s WHERE id_produto = %s",
                            (qtd, id_produto),
                        )
                        valor_total += subtotal
                        itens_adicionados += 1
                        InterfaceTerminal.sucesso(f"Item '{nome_prod}' adicionado! Subtotal: R$ {subtotal:.2f}")
                    except mysql.connector.Error as erro:
                        InterfaceTerminal.erro(f"Falha ao inserir item: {erro.msg}")

            continuar = input("\nDeseja adicionar outro produto a este pedido? (S/N): ").strip().upper()
            if continuar != "S":
                break

        if itens_adicionados == 0:
            self.banco.executar("DELETE FROM pedido WHERE id_pedido = %s", (id_pedido,))
            InterfaceTerminal.aviso(f"Nenhum item foi adicionado. Pedido #{id_pedido} cancelado.")
        else:
            self.banco.executar(
                "UPDATE pedido SET valor_total = %s WHERE id_pedido = %s",
                (valor_total, id_pedido),
            )
            InterfaceTerminal.sucesso(
                f"Pedido #{id_pedido} finalizado com sucesso! Total: R$ {valor_total:.2f} ({itens_adicionados} itens)."
            )

        InterfaceTerminal.pausar()

    def atualizar_status(self):
        InterfaceTerminal.exibir_titulo("ATUALIZAR STATUS DO PEDIDO")
        id_pedido = Validador.pedir_inteiro("ID do pedido: ", "ID do pedido", valor_minimo=1)

        pedido = self.banco.consultar(
            "SELECT id_pedido, status, valor_total FROM pedido WHERE id_pedido = %s",
            (id_pedido,),
        )
        if not pedido:
            InterfaceTerminal.aviso(f"Nenhum pedido encontrado com o ID {id_pedido}.")
            InterfaceTerminal.pausar()
            return

        status_atual = pedido[0][1]
        valor_total = float(pedido[0][2])
        print(f"\nPedido #{id_pedido} | Status atual: '{status_atual}' | Valor: R$ {valor_total:.2f}\n")

        novo_status = Validador.pedir_status_pedido()

        if novo_status == status_atual:
            InterfaceTerminal.aviso("O novo status informado é idêntico ao status atual.")
            InterfaceTerminal.pausar()
            return

        comando_sql = "UPDATE pedido SET status = %s WHERE id_pedido = %s"
        try:
            self.banco.executar(comando_sql, (novo_status, id_pedido))
            InterfaceTerminal.sucesso(f"Status do pedido #{id_pedido} atualizado para '{novo_status}' com sucesso!")
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
        InterfaceTerminal.pausar()

    def listar(self):
        InterfaceTerminal.exibir_titulo("LISTA DE PEDIDOS ATIVOS")
        comando_sql = """
            SELECT pedido.id_pedido, cliente.nome, pedido.status, pedido.valor_total,
                   COUNT(item_pedido.id_produto)
            FROM pedido
            INNER JOIN cliente ON cliente.id_cliente = pedido.id_cliente
            LEFT JOIN item_pedido ON item_pedido.id_pedido = pedido.id_pedido
            WHERE pedido.status <> 'Cancelado'
            GROUP BY pedido.id_pedido, cliente.nome, pedido.status, pedido.valor_total
            ORDER BY pedido.data_pedido DESC
        """
        try:
            pedidos = self.banco.consultar(comando_sql)
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
            InterfaceTerminal.pausar()
            return

        if not pedidos:
            InterfaceTerminal.aviso("Nenhum pedido ativo encontrado no momento.")
            InterfaceTerminal.pausar()
            return

        cabecalhos = ["Nº PEDIDO", "CLIENTE", "STATUS", "VALOR TOTAL", "ITENS"]
        linhas = []
        for p in pedidos:
            linhas.append([
                f"#{p[0]}",
                p[1],
                p[2],
                f"R$ {float(p[3]):.2f}",
                f"{p[4]} item(ns)",
            ])

        InterfaceTerminal.exibir_tabela(cabecalhos, linhas)
        InterfaceTerminal.pausar()

    def consultar_detalhes(self):
        InterfaceTerminal.exibir_titulo("DETALHES DO PEDIDO")
        id_pedido = Validador.pedir_inteiro("ID do pedido: ", "ID do pedido", valor_minimo=1)

        pedido = self.banco.consultar(
            """
            SELECT pedido.id_pedido, cliente.nome, cliente.cpf, pedido.status, 
                   pedido.valor_total, DATE_FORMAT(pedido.data_pedido, '%d/%m/%Y %H:%i')
            FROM pedido
            INNER JOIN cliente ON cliente.id_cliente = pedido.id_cliente
            WHERE pedido.id_pedido = %s
            """,
            (id_pedido,),
        )
        if not pedido:
            InterfaceTerminal.aviso(f"Nenhum pedido encontrado com o ID {id_pedido}.")
            InterfaceTerminal.pausar()
            return

        dados = pedido[0]
        print(f"Pedido: #{dados[0]} | Data: {dados[5]} | Status: {dados[3]}")
        print(f"Cliente: {dados[1]} (CPF: {dados[2]})")
        print(f"Valor Total do Pedido: R$ {float(dados[4]):.2f}\n")

        comando_sql = """
            SELECT produto.id_produto, produto.nome, produto.categoria,
                   item_pedido.quantidade, item_pedido.preco_unitario,
                   (item_pedido.quantidade * item_pedido.preco_unitario) AS subtotal
            FROM item_pedido
            INNER JOIN produto ON produto.id_produto = item_pedido.id_produto
            WHERE item_pedido.id_pedido = %s
            ORDER BY produto.nome
        """
        try:
            itens = self.banco.consultar(comando_sql, (id_pedido,))
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
            InterfaceTerminal.pausar()
            return

        if not itens:
            InterfaceTerminal.aviso("Nenhum item cadastrado neste pedido.")
        else:
            cabecalhos = ["COD", "PRODUTO", "CATEGORIA", "QTD", "PREÇO UNIT.", "SUBTOTAL"]
            linhas = []
            for item in itens:
                linhas.append([
                    item[0],
                    item[1],
                    item[2],
                    f"{item[3]} un",
                    f"R$ {float(item[4]):.2f}",
                    f"R$ {float(item[5]):.2f}",
                ])
            InterfaceTerminal.exibir_tabela(cabecalhos, linhas)

        InterfaceTerminal.pausar()
