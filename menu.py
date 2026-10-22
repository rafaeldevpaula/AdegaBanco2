from interface import InterfaceTerminal
from services.clientes import GerenciadorClientes
from services.enderecos import GerenciadorEnderecos
from services.fornecedores import GerenciadorFornecedores
from services.pedidos import GerenciadorPedidos
from services.produtos import GerenciadorProdutos


class Menu:
    def __init__(self):
        self.clientes = GerenciadorClientes()
        self.enderecos = GerenciadorEnderecos()
        self.fornecedores = GerenciadorFornecedores()
        self.produtos = GerenciadorProdutos()
        self.pedidos = GerenciadorPedidos()

    def iniciar(self):
        while True:
            InterfaceTerminal.exibir_menu_principal()
            opcao = input(f"\n{InterfaceTerminal.NEGRITO}Escolha uma opcao: {InterfaceTerminal.RESET}").strip()

            if opcao == "0":
                InterfaceTerminal.limpar_tela()
                print(f"\n{InterfaceTerminal.VERDE}{InterfaceTerminal.NEGRITO}Sistema encerrado. Ate logo!\n{InterfaceTerminal.RESET}")
                break

            # Clientes (1 a 4)
            elif opcao == "1":
                self.clientes.cadastrar()
            elif opcao == "2":
                self.clientes.atualizar()
            elif opcao == "3":
                self.clientes.listar()
            elif opcao == "4":
                self.clientes.remover()

            # Endereços (5 a 8)
            elif opcao == "5":
                self.enderecos.cadastrar()
            elif opcao == "6":
                self.enderecos.atualizar()
            elif opcao == "7":
                self.enderecos.consultar_por_cliente()
            elif opcao == "8":
                self.enderecos.remover()

            # Fornecedores (9 a 12)
            elif opcao == "9":
                self.fornecedores.cadastrar()
            elif opcao == "10":
                self.fornecedores.atualizar()
            elif opcao == "11":
                self.fornecedores.listar()
            elif opcao == "12":
                self.fornecedores.remover()

            # Produtos (13 a 17)
            elif opcao == "13":
                self.produtos.cadastrar()
            elif opcao == "14":
                self.produtos.atualizar_preco()
            elif opcao == "15":
                self.produtos.atualizar_estoque()
            elif opcao == "16":
                self.produtos.remover()
            elif opcao == "17":
                self.produtos.listar()

            # Pedidos (18 a 21)
            elif opcao == "18":
                self.pedidos.cadastrar()
            elif opcao == "19":
                self.pedidos.atualizar_status()
            elif opcao == "20":
                self.pedidos.listar()
            elif opcao == "21":
                self.pedidos.consultar_detalhes()

            else:
                InterfaceTerminal.aviso("Opcao invalida! Escolha um numero de 0 a 21.")
                InterfaceTerminal.pausar()
