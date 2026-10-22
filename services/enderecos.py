import mysql.connector
from database.banco_de_dados import BancoDeDados
from interface import InterfaceTerminal
from validadores import Validador


class GerenciadorEnderecos:
    def __init__(self):
        self.banco = BancoDeDados()

    def cadastrar(self):
        InterfaceTerminal.exibir_titulo("CADASTRAR ENDEREÇO DE CLIENTE")
        id_cliente = Validador.pedir_inteiro("ID do cliente: ", "ID do cliente", valor_minimo=1)

        cliente = self.banco.consultar("SELECT id_cliente, nome FROM cliente WHERE id_cliente = %s", (id_cliente,))
        if not cliente:
            InterfaceTerminal.erro(f"Nenhum cliente encontrado com o ID {id_cliente}.")
            InterfaceTerminal.pausar()
            return

        print(f"\nCliente selecionado: {cliente[0][1]}\n")

        endereco_existente = self.banco.consultar(
            "SELECT id_endereco FROM endereco WHERE id_cliente = %s", (id_cliente,)
        )
        if endereco_existente:
            InterfaceTerminal.aviso("Este cliente já possui um endereço cadastrado. Use a opção de Atualizar Endereço.")
            InterfaceTerminal.pausar()
            return

        rua = Validador.pedir_texto("Rua / Avenida: ", "Rua", tamanho_maximo=100, obrigatorio=True)
        numero = Validador.pedir_numero_endereco()
        bairro = Validador.pedir_texto("Bairro: ", "Bairro", tamanho_maximo=50, obrigatorio=True)
        cidade = Validador.pedir_texto("Cidade: ", "Cidade", tamanho_maximo=50, obrigatorio=True)
        complemento = Validador.pedir_texto("Complemento (opcional): ", "Complemento", tamanho_maximo=100, obrigatorio=False)
        cep = Validador.pedir_cep()

        comando_sql = """
            INSERT INTO endereco (id_cliente, rua, numero, bairro, cidade, complemento, cep)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.banco.executar(
                comando_sql,
                (id_cliente, rua, numero, bairro, cidade, complemento, cep),
            )
            InterfaceTerminal.sucesso("Endereço cadastrado com sucesso!")
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
        InterfaceTerminal.pausar()

    def atualizar(self):
        InterfaceTerminal.exibir_titulo("ATUALIZAR ENDEREÇO DE CLIENTE")
        id_cliente = Validador.pedir_inteiro("ID do cliente dono do endereço: ", "ID do cliente", valor_minimo=1)

        endereco_atual = self.banco.consultar(
            """
            SELECT cliente.nome, endereco.rua, endereco.numero, endereco.bairro, 
                   endereco.cidade, endereco.complemento, endereco.cep
            FROM endereco
            INNER JOIN cliente ON cliente.id_cliente = endereco.id_cliente
            WHERE endereco.id_cliente = %s
            """,
            (id_cliente,),
        )
        if not endereco_atual:
            InterfaceTerminal.aviso(f"Não foi encontrado nenhum endereço para o cliente de ID {id_cliente}.")
            InterfaceTerminal.pausar()
            return

        dados = endereco_atual[0]
        nome_cliente = dados[0]
        rua_atual = dados[1]
        numero_atual = dados[2]
        bairro_atual = dados[3]
        cidade_atual = dados[4]
        complemento_atual = dados[5]
        cep_atual = dados[6]

        print(f"\nEndereço atual de: {nome_cliente}")
        print(f" 1. Rua / Avenida: {rua_atual}")
        print(f" 2. Número:        {numero_atual}")
        print(f" 3. Bairro:        {bairro_atual}")
        print(f" 4. Cidade:        {cidade_atual}")
        print(f" 5. Complemento:   {complemento_atual if complemento_atual else 'Sem complemento'}")
        print(f" 6. CEP:           {cep_atual}")
        print("-" * 55)
        print("Qual campo você deseja atualizar?")
        print(" [ 1 ] Rua / Avenida")
        print(" [ 2 ] Número")
        print(" [ 3 ] Bairro")
        print(" [ 4 ] Cidade")
        print(" [ 5 ] Complemento")
        print(" [ 6 ] CEP")
        print(" [ 7 ] Todos os campos (passo a passo)")
        print(" [ 0 ] Cancelar e voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            InterfaceTerminal.aviso("Atualização cancelada.")
            InterfaceTerminal.pausar()
            return

        try:
            if opcao == "1":
                nova_rua = Validador.pedir_texto("Nova Rua / Avenida: ", "Rua", tamanho_maximo=100, obrigatorio=True)
                self.banco.executar("UPDATE endereco SET rua = %s WHERE id_cliente = %s", (nova_rua, id_cliente))
                InterfaceTerminal.sucesso("Rua atualizada com sucesso!")

            elif opcao == "2":
                novo_num = Validador.pedir_numero_endereco()
                self.banco.executar("UPDATE endereco SET numero = %s WHERE id_cliente = %s", (novo_num, id_cliente))
                InterfaceTerminal.sucesso("Número atualizado com sucesso!")

            elif opcao == "3":
                novo_bairro = Validador.pedir_texto("Novo Bairro: ", "Bairro", tamanho_maximo=50, obrigatorio=True)
                self.banco.executar("UPDATE endereco SET bairro = %s WHERE id_cliente = %s", (novo_bairro, id_cliente))
                InterfaceTerminal.sucesso("Bairro atualizado com sucesso!")

            elif opcao == "4":
                nova_cidade = Validador.pedir_texto("Nova Cidade: ", "Cidade", tamanho_maximo=50, obrigatorio=True)
                self.banco.executar("UPDATE endereco SET cidade = %s WHERE id_cliente = %s", (nova_cidade, id_cliente))
                InterfaceTerminal.sucesso("Cidade atualizada com sucesso!")

            elif opcao == "5":
                novo_comp = Validador.pedir_texto("Novo Complemento: ", "Complemento", tamanho_maximo=100, obrigatorio=False)
                self.banco.executar("UPDATE endereco SET complemento = %s WHERE id_cliente = %s", (novo_comp, id_cliente))
                InterfaceTerminal.sucesso("Complemento atualizado com sucesso!")

            elif opcao == "6":
                novo_cep = Validador.pedir_cep()
                self.banco.executar("UPDATE endereco SET cep = %s WHERE id_cliente = %s", (novo_cep, id_cliente))
                InterfaceTerminal.sucesso("CEP atualizado com sucesso!")

            elif opcao == "7":
                print("\n(Pressione ENTER para manter o valor atual)\n")
                rua = input(f"Nova Rua [{rua_atual}]: ").strip() or rua_atual
                numero = input(f"Novo Número [{numero_atual}]: ").strip() or numero_atual
                bairro = input(f"Novo Bairro [{bairro_atual}]: ").strip() or bairro_atual
                cidade = input(f"Nova Cidade [{cidade_atual}]: ").strip() or cidade_atual
                comp_dig = input(f"Novo Complemento [{complemento_atual or 'Vazio'}]: ").strip()
                complemento = complemento_atual if comp_dig == "" else (None if comp_dig == "-" else comp_dig)
                cep_dig = input(f"Novo CEP [{cep_atual}]: ").strip()
                cep = cep_atual if cep_dig == "" else Validador.validar_cep(cep_dig)[1]

                comando_sql = """
                    UPDATE endereco 
                    SET rua = %s, numero = %s, bairro = %s, cidade = %s, complemento = %s, cep = %s 
                    WHERE id_cliente = %s
                """
                self.banco.executar(comando_sql, (rua, numero, bairro, cidade, complemento, cep, id_cliente))
                InterfaceTerminal.sucesso("Endereço completo atualizado com sucesso!")

            else:
                InterfaceTerminal.aviso("Opção inválida.")

        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")

        InterfaceTerminal.pausar()

    def consultar_por_cliente(self):
        InterfaceTerminal.exibir_titulo("CONSULTAR ENDEREÇO DE CLIENTE")
        id_cliente = Validador.pedir_inteiro("ID do cliente: ", "ID do cliente", valor_minimo=1)

        comando_sql = """
            SELECT cliente.nome, endereco.rua, endereco.numero, endereco.bairro, 
                   endereco.cidade, endereco.complemento, endereco.cep
            FROM endereco
            INNER JOIN cliente ON cliente.id_cliente = endereco.id_cliente
            WHERE endereco.id_cliente = %s
        """
        try:
            resultados = self.banco.consultar(comando_sql, (id_cliente,))
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")
            InterfaceTerminal.pausar()
            return

        if resultados:
            cabecalhos = ["CLIENTE", "LOGRADOURO", "Nº", "BAIRRO", "CIDADE", "COMPLEMENTO", "CEP"]
            linhas = []
            for r in resultados:
                linhas.append([
                    r[0],
                    r[1],
                    r[2],
                    r[3],
                    r[4],
                    r[5] if r[5] else "Sem complemento",
                    r[6],
                ])
            print()
            InterfaceTerminal.exibir_tabela(cabecalhos, linhas)
        else:
            InterfaceTerminal.aviso(f"Nenhum endereço cadastrado para o cliente de ID {id_cliente}.")
        InterfaceTerminal.pausar()

    def remover(self):
        InterfaceTerminal.exibir_titulo("REMOVER ENDEREÇO DE CLIENTE")
        id_cliente = Validador.pedir_inteiro("ID do cliente dono do endereço a remover: ", "ID do cliente", valor_minimo=1)

        endereco = self.banco.consultar(
            """
            SELECT cliente.nome, endereco.rua, endereco.numero, endereco.bairro, endereco.cidade
            FROM endereco
            INNER JOIN cliente ON cliente.id_cliente = endereco.id_cliente
            WHERE endereco.id_cliente = %s
            """,
            (id_cliente,),
        )
        if not endereco:
            InterfaceTerminal.aviso(f"Nenhum endereço cadastrado para o cliente de ID {id_cliente}.")
            InterfaceTerminal.pausar()
            return

        dados = endereco[0]
        print(f"\nEndereço de {dados[0]}: {dados[1]}, Nº {dados[2]} - {dados[3]}, {dados[4]}")
        confirmacao = input("\nTem certeza que deseja remover este endereço? (S/N): ").strip().upper()
        if confirmacao != "S":
            InterfaceTerminal.aviso("Operação cancelada pelo usuário.")
            InterfaceTerminal.pausar()
            return

        try:
            self.banco.executar("DELETE FROM endereco WHERE id_cliente = %s", (id_cliente,))
            InterfaceTerminal.sucesso("Endereço removido com sucesso!")
        except mysql.connector.Error as erro:
            InterfaceTerminal.erro(f"Falha no banco de dados: {erro.msg}")

        InterfaceTerminal.pausar()
