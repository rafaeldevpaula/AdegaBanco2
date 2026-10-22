import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

os.system("")


class InterfaceTerminal:
    RESET = "\033[0m"
    NEGRITO = "\033[1m"
    VERDE = "\033[92m"
    VERMELHO = "\033[91m"
    AMARELO = "\033[93m"
    AZUL = "\033[94m"
    CIANO = "\033[96m"

    @classmethod
    def limpar_tela(cls):
        os.system("cls" if os.name == "nt" else "clear")
        print("\033[H\033[2J\033[3J", end="", flush=True)

    @classmethod
    def pausar(cls):
        input(f"\n{cls.AMARELO}Pressione ENTER para voltar ao menu...{cls.RESET}")

    @classmethod
    def exibir_titulo(cls, texto):
        cls.limpar_tela()
        largura = 76
        print(f"{cls.CIANO}{cls.NEGRITO}{'=' * largura}")
        print(texto.center(largura))
        print(f"{'=' * largura}{cls.RESET}\n")

    @classmethod
    def sucesso(cls, mensagem):
        print(f"\n{cls.VERDE}{cls.NEGRITO}[OK] {mensagem}{cls.RESET}")

    @classmethod
    def erro(cls, mensagem):
        print(f"\n{cls.VERMELHO}{cls.NEGRITO}[ERRO] {mensagem}{cls.RESET}")

    @classmethod
    def aviso(cls, mensagem):
        print(f"\n{cls.AMARELO}[AVISO] {mensagem}{cls.RESET}")

    @classmethod
    def exibir_tabela(cls, cabecalhos, linhas):
        if not linhas:
            cls.aviso("Nenhum registro encontrado.")
            return

        larguras = [len(str(c)) for c in cabecalhos]
        for linha in linhas:
            for i, valor in enumerate(linha):
                larguras[i] = max(larguras[i], len(str(valor)))

        borda = "+" + "+".join("-" * (largura + 2) for largura in larguras) + "+"

        print(f"{cls.CIANO}{borda}")
        linha_cabecalho = "| " + " | ".join(str(c).center(larguras[i]) for i, c in enumerate(cabecalhos)) + " |"
        print(f"{cls.NEGRITO}{linha_cabecalho}")
        print(f"{borda}{cls.RESET}")

        for linha in linhas:
            linha_dados = "| " + " | ".join(str(valor).ljust(larguras[i]) for i, valor in enumerate(linha)) + " |"
            print(linha_dados)

        print(f"{cls.CIANO}{borda}{cls.RESET}")
        print(f"Total: {cls.NEGRITO}{len(linhas)}{cls.RESET} registro(s) encontrado(s).\n")

    @classmethod
    def exibir_menu_principal(cls):
        cls.limpar_tela()
        linha_divisoria = "=" * 76
        print(f"{cls.CIANO}{cls.NEGRITO}{linha_divisoria}")
        print("SISTEMA DE GESTAO - ADEGA PASSARELA".center(76))
        print(f"{linha_divisoria}{cls.RESET}")
        print(f" {cls.AMARELO}[ CLIENTES ]{cls.RESET}                        {cls.AMARELO}[ ENDERECOS ]{cls.RESET}")
        print("  1. Cadastrar Cliente                 5. Cadastrar Endereco")
        print("  2. Atualizar Cliente                 6. Atualizar Endereco")
        print("  3. Listar Clientes                   7. Consultar Endereco por Cliente")
        print("  4. Remover Cliente                   8. Remover Endereco")
        print()
        print(f" {cls.AMARELO}[ FORNECEDORES ]{cls.RESET}                    {cls.AMARELO}[ PRODUTOS & ESTOQUE ]{cls.RESET}")
        print("  9. Cadastrar Fornecedor             13. Cadastrar Produto")
        print("  10. Atualizar Fornecedor            14. Atualizar Preco do Produto")
        print("  11. Listar Fornecedores             15. Atualizar Estoque do Produto")
        print("  12. Remover Fornecedor              16. Remover Produto")
        print("                                      17. Consultar Produtos em Estoque")
        print(f" {cls.AMARELO}[ PEDIDOS ]{cls.RESET}")
        print("  18. Cadastrar Novo Pedido")
        print("  19. Atualizar Status de Pedido")
        print("  20. Consultar Resumo de Pedidos")
        print("  21. Consultar Detalhes do Pedido (Itens)")
        print()
        print("-" * 76)
        print(f"  {cls.VERMELHO}0. Sair do Sistema{cls.RESET}")
        print(f"{cls.CIANO}{linha_divisoria}{cls.RESET}")
