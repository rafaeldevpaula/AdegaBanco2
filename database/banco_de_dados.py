import mysql.connector
import config


class BancoDeDados:
    def __init__(self):
        self.host = config.HOST_BANCO
        self.porta = config.PORTA_BANCO
        self.usuario = config.USUARIO_BANCO
        self.senha = config.SENHA_BANCO
        self.nome_banco = config.NOME_BANCO

    def conectar(self):
        return mysql.connector.connect(
            host=self.host,
            port=self.porta,
            user=self.usuario,
            password=self.senha,
            database=self.nome_banco,
            ssl_disabled=True,
        )

    def executar(self, comando_sql, parametros=()):
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute(comando_sql, parametros)
        conexao.commit()
        linhas_afetadas = cursor.rowcount
        cursor.close()
        conexao.close()
        return linhas_afetadas

    def consultar(self, comando_sql, parametros=()):
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute(comando_sql, parametros)
        resultado = cursor.fetchall()
        cursor.close()
        conexao.close()
        return resultado
