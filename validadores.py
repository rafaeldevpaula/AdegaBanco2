class Validador:
    @staticmethod
    def validar_texto(texto_digitado, nome_campo, tamanho_maximo=100, obrigatorio=True):
        texto_limpo = texto_digitado.strip()
        if not texto_limpo:
            if obrigatorio:
                return False, f"O campo '{nome_campo}' não pode ficar em branco."
            return True, None

        if len(texto_limpo) > tamanho_maximo:
            return False, f"O campo '{nome_campo}' deve ter no máximo {tamanho_maximo} caracteres."

        return True, texto_limpo

    @staticmethod
    def validar_cpf(cpf_digitado):
        numeros = "".join(caractere for caractere in cpf_digitado if caractere.isdigit())

        if len(numeros) != 11:
            return False, "O CPF deve conter exatamente 11 dígitos numéricos."

        if numeros == numeros[0] * 11:
            return False, "CPF inválido (dígitos repetidos)."

        cpf_formatado = f"{numeros[0:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:11]}"
        return True, cpf_formatado

    @staticmethod
    def validar_cnpj(cnpj_digitado):
        numeros = "".join(caractere for caractere in cnpj_digitado if caractere.isdigit())

        if len(numeros) != 14:
            return False, "O CNPJ deve conter exatamente 14 dígitos numéricos."

        if numeros == numeros[0] * 14:
            return False, "CNPJ inválido (dígitos repetidos)."

        cnpj_formatado = f"{numeros[0:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:14]}"
        return True, cnpj_formatado

    @staticmethod
    def validar_cep(cep_digitado):
        numeros = "".join(caractere for caractere in cep_digitado if caractere.isdigit())

        if len(numeros) != 8:
            return False, "O CEP deve conter exatamente 8 dígitos numéricos (ex: 01310-100 ou 01310100)."

        cep_formatado = f"{numeros[0:5]}-{numeros[5:8]}"
        return True, cep_formatado

    @staticmethod
    def validar_telefone(telefone_digitado, obrigatorio=False):
        telefone_limpo = telefone_digitado.strip()
        if not telefone_limpo:
            if obrigatorio:
                return False, "O telefone é obrigatório."
            return True, None

        numeros = "".join(caractere for caractere in telefone_limpo if caractere.isdigit())

        if len(numeros) not in (10, 11):
            return False, "O telefone deve conter DDD + número (10 dígitos para fixo ou 11 para celular)."

        if len(numeros) == 11:
            telefone_formatado = f"({numeros[0:2]}) {numeros[2:7]}-{numeros[7:11]}"
        else:
            telefone_formatado = f"({numeros[0:2]}) {numeros[2:6]}-{numeros[6:10]}"

        return True, telefone_formatado

    @staticmethod
    def validar_email(email_digitado, obrigatorio=False):
        email_limpo = email_digitado.strip().lower()
        if not email_limpo:
            if obrigatorio:
                return False, "O e-mail é obrigatório."
            return True, None

        if " " in email_limpo or "@" not in email_limpo or "." not in email_limpo:
            return False, "E-mail inválido. Deve conter '@' e um domínio (ex: usuario@email.com)."

        partes = email_limpo.split("@")
        if len(partes) != 2 or not partes[0] or not partes[1]:
            return False, "E-mail com formato inválido."

        dominio = partes[1]
        if "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
            return False, "Domínio do e-mail inválido (ex: gmail.com, hotmail.com)."

        if len(email_limpo) > 100:
            return False, "O e-mail deve ter no máximo 100 caracteres."

        return True, email_limpo

    @staticmethod
    def validar_numero_endereco(numero_digitado):
        numero_limpo = numero_digitado.strip().upper()
        if not numero_limpo:
            return False, "O número do endereço é obrigatório (digite o número ou 'S/N')."

        if len(numero_limpo) > 10:
            return False, "O número deve ter no máximo 10 caracteres."

        return True, numero_limpo

    @staticmethod
    def validar_inteiro(valor_digitado, nome_campo, valor_minimo=0):
        valor_limpo = valor_digitado.strip()
        if not valor_limpo.isdigit():
            return False, f"O campo '{nome_campo}' deve ser um número inteiro válido."

        numero = int(valor_limpo)
        if numero < valor_minimo:
            return False, f"O campo '{nome_campo}' deve ser maior ou igual a {valor_minimo}."

        return True, numero

    @staticmethod
    def validar_preco(preco_digitado):
        preco_limpo = preco_digitado.strip().replace(",", ".")
        try:
            valor = float(preco_limpo)
        except ValueError:
            return False, "Preço inválido. Digite um valor numérico (ex: 49.90 ou 49,90)."

        if valor < 0:
            return False, "O preço do produto não pode ser negativo."

        return True, round(valor, 2)

    @classmethod
    def pedir_texto(cls, mensagem, nome_campo, tamanho_maximo=100, obrigatorio=True):
        while True:
            digitado = input(mensagem)
            valido, resultado = cls.validar_texto(digitado, nome_campo, tamanho_maximo, obrigatorio)
            if valido:
                return resultado
            print(f"[Aviso] {resultado}")

    @classmethod
    def pedir_cpf(cls):
        while True:
            digitado = input("CPF (apenas 11 números ou com pontuação): ")
            valido, resultado = cls.validar_cpf(digitado)
            if valido:
                return resultado
            print(f"[Aviso] {resultado}")

    @classmethod
    def pedir_cnpj(cls):
        while True:
            digitado = input("CNPJ (apenas 14 números ou com pontuação): ")
            valido, resultado = cls.validar_cnpj(digitado)
            if valido:
                return resultado
            print(f"[Aviso] {resultado}")

    @classmethod
    def pedir_cep(cls):
        while True:
            digitado = input("CEP (8 números ou ex: 01001-000): ")
            valido, resultado = cls.validar_cep(digitado)
            if valido:
                return resultado
            print(f"[Aviso] {resultado}")

    @classmethod
    def pedir_telefone(cls, obrigatorio=False):
        while True:
            digitado = input("Telefone com DDD (ex: 11987654321 ou Enter para vazio): ")
            valido, resultado = cls.validar_telefone(digitado, obrigatorio)
            if valido:
                return resultado
            print(f"[Aviso] {resultado}")

    @classmethod
    def pedir_email(cls, obrigatorio=False):
        while True:
            digitado = input("E-mail (ou Enter para vazio): ")
            valido, resultado = cls.validar_email(digitado, obrigatorio)
            if valido:
                return resultado
            print(f"[Aviso] {resultado}")

    @classmethod
    def pedir_numero_endereco(cls):
        while True:
            digitado = input("Número (ex: 120 ou S/N): ")
            valido, resultado = cls.validar_numero_endereco(digitado)
            if valido:
                return resultado
            print(f"[Aviso] {resultado}")

    @classmethod
    def pedir_inteiro(cls, mensagem, nome_campo, valor_minimo=0):
        while True:
            digitado = input(mensagem)
            valido, resultado = cls.validar_inteiro(digitado, nome_campo, valor_minimo)
            if valido:
                return resultado
            print(f"[Aviso] {resultado}")

    @classmethod
    def pedir_preco(cls, mensagem="Preço: "):
        while True:
            digitado = input(mensagem)
            valido, resultado = cls.validar_preco(digitado)
            if valido:
                return resultado
            print(f"[Aviso] {resultado}")

    @classmethod
    def pedir_status_pedido(cls):
        status_validos = ["Pendente", "Pago", "Enviado", "Entregue", "Cancelado"]
        while True:
            print(f"Opções de status: {', '.join(status_validos)}")
            digitado = input("Novo Status: ").strip().capitalize()
            for status in status_validos:
                if digitado.lower() == status.lower():
                    return status
            print("[Aviso] Status inválido. Escolha uma das opções listadas.")
