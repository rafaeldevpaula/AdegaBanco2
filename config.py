import os
from dotenv import load_dotenv

load_dotenv()

HOST_BANCO = os.getenv("ADEGA_DB_HOST", "localhost")
PORTA_BANCO = int(os.getenv("ADEGA_DB_PORT", "3306"))
USUARIO_BANCO = os.getenv("ADEGA_DB_USER", "root")
SENHA_BANCO = os.getenv("ADEGA_DB_PASSWORD", "")
NOME_BANCO = os.getenv("ADEGA_DB_NAME", "adega")
