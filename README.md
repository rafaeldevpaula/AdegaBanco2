#  Sistema de Gestão - Adega Passarela (BDD2)

Sistema completo de gerenciamento para a **Adega Passarela**, desenvolvido em **Python 3** orientado a objetos e integrado ao banco de dados relacional **MySQL**. Controla o catálogo de bebidas em geral (cervejas, destilados, vinhos, refrigerantes, sucos, gelo e carvão) e itens de conveniência/mercearia (petiscos, salgadinhos, frios e doces).

---

##  Funcionalidades

- **Clientes**: Cadastro, validação de CPF/telefone/e-mail, listagem em tabelas, atualização seletiva e remoção com integridade.
- **Endereços**: Vínculo 1:1 com cliente, validação de CEP e formatação.
- **Fornecedores**: Cadastro com CNPJ, listagem, atualização pontual e exclusão.
- **Produtos & Estoque**: Controle de categorias, marcas, preços e baixa automática no estoque.
- **Pedidos de Venda**: Criação de pedidos com múltiplos itens, cálculo automático de totais, consultas simples e consultas detalhadas com junções em 4 tabelas.
- **Interface Terminal**: Menu em painel, tabelas alinhadas com bordas e cores.

---

##  Como Executar

### 1. Clonar o repositório
```bash
git clone https://github.com/rafaeldevpaula/AdegaBanco2.git
cd AdegaBanco2
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente (`.env`)
Copie o modelo de `.env.example` para `.env`:
```env
ADEGA_DB_HOST=localhost
ADEGA_DB_PORT=3306
ADEGA_DB_USER=root
ADEGA_DB_PASSWORD=sua_senha
ADEGA_DB_NAME=adega
```

### 4. Executar
```bash
python main.py
```
