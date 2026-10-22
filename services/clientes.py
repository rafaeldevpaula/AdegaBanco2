import mysql.connector
from database.banco_de_dados import BancoDeDados
from interface import InterfaceTerminal
from validadores import Validador


class GerenciadorClientes:
    def __init__(self):
        self.banco = BancoDeDados()

    def cadastrar(self):
        InterfaceTerminal.exibir_titulo("CADASTRAR NOVO CLIENTE")
        nome = Validador.pedir_texto("Nome: ", "Nome", tamanho_maximo=100, obrigatorio=True)
        cpf = Validador.pedir_cpf()
        telefone = Validador.pedir_telefone(obrigatorio=False)
        email = Validador.pedir_email(obrigatorio=False)

        comando_sql = "INSERT INTO cliente (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)"
        try:
            self.banco.executar(comando_sql, (nome, cpf, telefone, email))
            InterfaceTerminal.sucesso("Cliente cadastrado com sucesso!")
        except mysql.connector.Error as erro:
            if erro.errno == 1062:
                InterfaceTerminal.erro(f"Já existe um cliente cadastrado com o CPF '{cpf}'.")
            else:
                InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
        InterfaceTerminal.pausar()

    def listar(self):
        InterfaceTerminal.exibir_titulo("LISTA DE CLIENTES CADASTRADOS")
        comando_sql = """
            SELECT id_cliente, nome, cpf, telefone, email
            FROM cliente
            ORDER BY nome
        """
        try:
            clientes = self.banco.consultar(comando_sql)
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
            InterfaceTerminal.pausar()
            return

        if not clientes:
            InterfaceTerminal.aviso("Nenhum cliente cadastrado no momento.")
            InterfaceTerminal.pausar()
            return

        cabecalhos = ["ID", "NOME", "CPF", "TELEFONE", "E-MAIL"]
        linhas_formatadas = []
        for cliente in clientes:
            linhas_formatadas.append([
                cliente[0],
                cliente[1],
                cliente[2],
                cliente[3] if cliente[3] else "Não informado",
                cliente[4] if cliente[4] else "Não informado",
            ])

        InterfaceTerminal.exibir_tabela(cabecalhos, linhas_formatadas)
        InterfaceTerminal.pausar()

    def atualizar(self):
        InterfaceTerminal.exibir_titulo("ATUALIZAR DADOS DO CLIENTE")
        id_cliente = Validador.pedir_inteiro("ID do cliente a atualizar: ", "ID do cliente", valor_minimo=1)

        resultado = self.banco.consultar(
            "SELECT id_cliente, nome, telefone, email, cpf FROM cliente WHERE id_cliente = %s",
            (id_cliente,),
        )
        if not resultado:
            InterfaceTerminal.aviso(f"Nenhum cliente encontrado com o ID {id_cliente}.")
            InterfaceTerminal.pausar()
            return

        cliente = resultado[0]
        nome_atual = cliente[1]
        telefone_atual = cliente[2]
        email_atual = cliente[3]
        cpf_atual = cliente[4]

        print(f"\nCliente: {nome_atual} (CPF: {cpf_atual})")
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
                self.banco.executar("UPDATE cliente SET nome = %s WHERE id_cliente = %s", (novo_nome, id_cliente))
                InterfaceTerminal.sucesso("Nome atualizado com sucesso!")

            elif opcao == "2":
                novo_telefone = Validador.pedir_telefone(obrigatorio=False)
                self.banco.executar("UPDATE cliente SET telefone = %s WHERE id_cliente = %s", (novo_telefone, id_cliente))
                InterfaceTerminal.sucesso("Telefone atualizado com sucesso!")

            elif opcao == "3":
                novo_email = Validador.pedir_email(obrigatorio=False)
                self.banco.executar("UPDATE cliente SET email = %s WHERE id_cliente = %s", (novo_email, id_cliente))
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

                comando_sql = "UPDATE cliente SET nome = %s, telefone = %s, email = %s WHERE id_cliente = %s"
                self.banco.executar(comando_sql, (novo_nome, novo_telefone, novo_email, id_cliente))
                InterfaceTerminal.sucesso("Dados do cliente atualizados com sucesso!")

            else:
                InterfaceTerminal.aviso("Opção inválida.")

        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")

        InterfaceTerminal.pausar()

    def remover(self):
        InterfaceTerminal.exibir_titulo("REMOVER CLIENTE")
        id_cliente = Validador.pedir_inteiro("ID do cliente a ser removido: ", "ID do cliente", valor_minimo=1)
        cliente = self.banco.consultar("SELECT id_cliente, nome FROM cliente WHERE id_cliente = %s", (id_cliente,))
        if not cliente:
            InterfaceTerminal.aviso(f"Nenhum cliente encontrado com o ID {id_cliente}.")
            InterfaceTerminal.pausar()
            return

        nome_cliente = cliente[0][1]

        pedidos = self.banco.consultar("SELECT id_pedido FROM pedido WHERE id_cliente = %s", (id_cliente,))
        if pedidos:
            InterfaceTerminal.erro(f"O cliente '{nome_cliente}' não pode ser removido pois possui {len(pedidos)} pedido(s) registrado(s).")
            InterfaceTerminal.pausar()
            return

        endereco = self.banco.consultar("SELECT id_endereco FROM endereco WHERE id_cliente = %s", (id_cliente,))
        if endereco:
            print(f"\nAtenção: O cliente '{nome_cliente}' possui um endereço cadastrado.")
            confirmar = input("Deseja remover o endereço e excluir o cliente permanentemente? (S/N): ").strip().upper()
            if confirmar != "S":
                InterfaceTerminal.aviso("Operação cancelada pelo usuário.")
                InterfaceTerminal.pausar()
                return

            try:
                self.banco.executar("DELETE FROM endereco WHERE id_cliente = %s", (id_cliente,))
                self.banco.executar("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
                InterfaceTerminal.sucesso(f"Cliente '{nome_cliente}' e seu endereço foram removidos com sucesso!")
            except mysql.connector.Error as erro:
                InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
        else:
            confirmar = input(f"\nTem certeza que deseja remover o cliente '{nome_cliente}'? (S/N): ").strip().upper()
            if confirmar != "S":
                InterfaceTerminal.aviso("Operação cancelada pelo usuário.")
                InterfaceTerminal.pausar()
                return

            try:
                self.banco.executar("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
                InterfaceTerminal.sucesso(f"Cliente '{nome_cliente}' removido com sucesso!")
            except mysql.connector.Error as erro:
                InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")

        InterfaceTerminal.pausar()
