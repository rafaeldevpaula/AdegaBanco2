import mysql.connector
from database.banco_de_dados import BancoDeDados
from interface import InterfaceTerminal
from validadores import Validador


class GerenciadorFornecedores:
    def __init__(self):
        self.banco = BancoDeDados()

    def cadastrar(self):
        InterfaceTerminal.exibir_titulo("CADASTRAR NOVO FORNECEDOR")
        nome = Validador.pedir_texto("Nome da empresa / fornecedor: ", "Nome", tamanho_maximo=100, obrigatorio=True)
        cnpj = Validador.pedir_cnpj()
        telefone = Validador.pedir_telefone(obrigatorio=False)
        email = Validador.pedir_email(obrigatorio=False)

        comando_sql = "INSERT INTO fornecedor (nome, cnpj, telefone, email) VALUES (%s, %s, %s, %s)"
        try:
            self.banco.executar(comando_sql, (nome, cnpj, telefone, email))
            InterfaceTerminal.sucesso("Fornecedor cadastrado com sucesso!")
        except mysql.connector.Error as erro:
            if erro.errno == 1062:
                InterfaceTerminal.erro(f"Já existe um fornecedor cadastrado com o CNPJ '{cnpj}'.")
            else:
                InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
        InterfaceTerminal.pausar()

    def listar(self):
        InterfaceTerminal.exibir_titulo("LISTA DE FORNECEDORES CADASTRADOS")
        comando_sql = """
            SELECT id_fornecedor, nome, cnpj, telefone, email
            FROM fornecedor
            ORDER BY nome
        """
        try:
            fornecedores = self.banco.consultar(comando_sql)
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
            InterfaceTerminal.pausar()
            return

        if not fornecedores:
            InterfaceTerminal.aviso("Nenhum fornecedor cadastrado no momento.")
            InterfaceTerminal.pausar()
            return

        cabecalhos = ["ID", "NOME DO FORNECEDOR", "CNPJ", "TELEFONE", "E-MAIL"]
        linhas_formatadas = []
        for f in fornecedores:
            linhas_formatadas.append([
                f[0],
                f[1],
                f[2] if f[2] else "Não informado",
                f[3] if f[3] else "Não informado",
                f[4] if f[4] else "Não informado",
            ])

        InterfaceTerminal.exibir_tabela(cabecalhos, linhas_formatadas)
        InterfaceTerminal.pausar()

    def atualizar(self):
        InterfaceTerminal.exibir_titulo("ATUALIZAR DADOS DO FORNECEDOR")
        id_fornecedor = Validador.pedir_inteiro("ID do fornecedor a atualizar: ", "ID do fornecedor", valor_minimo=1)

        resultado = self.banco.consultar(
            "SELECT id_fornecedor, nome, cnpj, telefone, email FROM fornecedor WHERE id_fornecedor = %s",
            (id_fornecedor,),
        )
        if not resultado:
            InterfaceTerminal.aviso(f"Nenhum fornecedor encontrado com o ID {id_fornecedor}.")
            InterfaceTerminal.pausar()
            return

        dados = resultado[0]
        nome_atual = dados[1]
        cnpj_atual = dados[2]
        telefone_atual = dados[3]
        email_atual = dados[4]

        print(f"\nFornecedor: {nome_atual} (CNPJ: {cnpj_atual})")
        print(f" 1. Nome:     {nome_atual}")
        print(f" 2. Telefone: {telefone_atual if telefone_atual else 'Não informado'}")
        print(f" 3. E-mail:   {email_atual if email_atual else 'Não informado'}")
        print("-" * 55)
        print("Qual campo você deseja atualizar?")
        print(" [ 1 ] Apenas o Nome")
        print(" [ 2 ] Apenas o Telefone")
        print(" [ 3 ] Apenas o E-mail")
        print(" [ 4 ] Todos os campos (passo a passo)")
        print(" [ 0 ] Cancelar e voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            InterfaceTerminal.aviso("Atualização cancelada.")
            InterfaceTerminal.pausar()
            return

        try:
            if opcao == "1":
                novo_nome = Validador.pedir_texto("Novo Nome: ", "Nome", tamanho_maximo=100, obrigatorio=True)
                self.banco.executar("UPDATE fornecedor SET nome = %s WHERE id_fornecedor = %s", (novo_nome, id_fornecedor))
                InterfaceTerminal.sucesso("Nome atualizado com sucesso!")

            elif opcao == "2":
                novo_telefone = Validador.pedir_telefone(obrigatorio=False)
                self.banco.executar("UPDATE fornecedor SET telefone = %s WHERE id_fornecedor = %s", (novo_telefone, id_fornecedor))
                InterfaceTerminal.sucesso("Telefone atualizado com sucesso!")

            elif opcao == "3":
                novo_email = Validador.pedir_email(obrigatorio=False)
                self.banco.executar("UPDATE fornecedor SET email = %s WHERE id_fornecedor = %s", (novo_email, id_fornecedor))
                InterfaceTerminal.sucesso("E-mail atualizado com sucesso!")

            elif opcao == "4":
                print("\n(Pressione ENTER para manter o valor atual)\n")
                digitado_nome = input(f"Novo Nome [{nome_atual}]: ").strip()
                novo_nome = digitado_nome if digitado_nome else nome_atual

                digitado_tel = input(f"Novo Telefone [{telefone_atual or 'Vazio'}]: ").strip()
                if digitado_tel == "":
                    novo_telefone = telefone_atual
                else:
                    _, novo_telefone = Validador.validar_telefone(digitado_tel, obrigatorio=False)

                digitado_email = input(f"Novo E-mail [{email_atual or 'Vazio'}]: ").strip()
                if digitado_email == "":
                    novo_email = email_atual
                else:
                    _, novo_email = Validador.validar_email(digitado_email, obrigatorio=False)

                comando_sql = "UPDATE fornecedor SET nome = %s, telefone = %s, email = %s WHERE id_fornecedor = %s"
                self.banco.executar(comando_sql, (novo_nome, novo_telefone, novo_email, id_fornecedor))
                InterfaceTerminal.sucesso("Dados do fornecedor atualizados com sucesso!")

            else:
                InterfaceTerminal.aviso("Opção inválida.")

        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")

        InterfaceTerminal.pausar()

    def remover(self):
        InterfaceTerminal.exibir_titulo("REMOVER FORNECEDOR")
        id_fornecedor = Validador.pedir_inteiro("ID do fornecedor a ser removido: ", "ID do fornecedor", valor_minimo=1)
        fornecedor = self.banco.consultar("SELECT id_fornecedor, nome FROM fornecedor WHERE id_fornecedor = %s", (id_fornecedor,))
        if not fornecedor:
            InterfaceTerminal.aviso(f"Nenhum fornecedor encontrado com o ID {id_fornecedor}.")
            InterfaceTerminal.pausar()
            return

        confirmacao = input(f"\nTem certeza que deseja remover o fornecedor '{fornecedor[0][1]}'? (S/N): ").strip().upper()
        if confirmacao != "S":
            InterfaceTerminal.aviso("Operação cancelada pelo usuário.")
            InterfaceTerminal.pausar()
            return

        try:
            self.banco.executar("DELETE FROM fornecedor WHERE id_fornecedor = %s", (id_fornecedor,))
            InterfaceTerminal.sucesso(f"Fornecedor '{fornecedor[0][1]}' removido com sucesso!")
        except mysql.connector.Error as erro:
            if erro.errno == 1451:
                InterfaceTerminal.erro("Este fornecedor não pode ser removido pois possui produtos cadastrados vinculados.")
            else:
                InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
        InterfaceTerminal.pausar()
