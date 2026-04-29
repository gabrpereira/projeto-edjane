import streamlit as st
import sqlite3
import pandas as pd

# --- Configuração de Armazenamento Local ---
conn = sqlite3.connect('produtos.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS produtos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              nome TEXT NOT NULL, categoria TEXT, preco REAL,
              quantidade INTEGER, descricao TEXT,
              imagem_url TEXT, status TEXT)''')
conn.commit()

# --- Configuração da Interface ---
st.set_page_config(page_title="App de Produtos", layout="wide")
st.title("📦 Cadastro de Produtos")

# --- Menu de Navegação ---
menu = ["Cadastrar Produto", "Estoque (Listar, Editar e Excluir)"]
escolha = st.sidebar.radio("Navegação", menu)

# --- TELA 1: CADASTRO ---
if escolha == "Cadastrar Produto":
    st.subheader("Novo Produto")

    with st.form("form_cadastro"):
        nome = st.text_input("Nome do Produto *")
        categoria = st.selectbox("Categoria", ["Eletrônicos", "Vestuário", "Alimentos", "Casa", "Outros"])

        col1, col2 = st.columns(2)
        preco = col1.number_input("Preço (R$) *", min_value=0.0, format="%.2f")
        quantidade = col2.number_input("Quantidade *", min_value=0, step=1)

        descricao = st.text_area("Descrição")
        imagem_url = st.text_input("URL da Imagem do Produto * (Ex: https://link.com/img.jpg)")
        status = st.selectbox("Status", ["Ativo", "Inativo"])

        submit = st.form_submit_button("Salvar Produto")

        if submit:
            if nome == "" or imagem_url == "":
                st.error("Por favor, preencha os campos obrigatórios (*).")
            else:
                c.execute(
                    "INSERT INTO produtos (nome, categoria, preco, quantidade, descricao, imagem_url, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (nome, categoria, preco, quantidade, descricao, imagem_url, status)
                )
                conn.commit()
                st.success(f"Produto '{nome}' cadastrado com sucesso!")

# --- TELA 2: LISTAGEM, EDIÇÃO E EXCLUSÃO ---
elif escolha == "Estoque (Listar, Editar e Excluir)":
    st.subheader("Gerenciamento de Estoque")

    # Filtro e Ordenação
    col_f, col_o = st.columns(2)
    categorias_db = [row[0] for row in c.execute("SELECT DISTINCT categoria FROM produtos")]
    filtro_cat = col_f.selectbox("Filtro por Categoria", ["Todas"] + categorias_db)
    ordenacao = col_o.selectbox("Ordenação", ["ID", "Nome (A-Z)", "Preço (Menor-Maior)", "Preço (Maior-Menor)"])

    # Construção da query com filtros
    query = "SELECT * FROM produtos"
    params = []

    if filtro_cat != "Todas":
        query += " WHERE categoria = ?"
        params.append(filtro_cat)

    if ordenacao == "Nome (A-Z)":
        query += " ORDER BY nome ASC"
    elif ordenacao == "Preço (Menor-Maior)":
        query += " ORDER BY preco ASC"
    elif ordenacao == "Preço (Maior-Menor)":
        query += " ORDER BY preco DESC"

    df = pd.read_sql_query(query, conn, params=params)

    if not df.empty:
        for index, row in df.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([1, 3, 1])

                with c1:
                    try:
                        st.image(row['imagem_url'], width=120)
                    except:
                        st.warning("Imagem inválida")

                with c2:
                    st.markdown(f"### {row['nome']}")
                    st.write(f"**Categoria:** {row['categoria']} | **Status:** {row['status']}")
                    st.write(f"**Descrição:** {row['descricao']}")
                    st.markdown(f"**Preço:** R$ {row['preco']:.2f} | **Estoque:** {row['quantidade']} unidades")

                with c3:
                    st.write("Ações:")
                    if st.button("❌ Excluir", key=f"del_{row['id']}"):
                        c.execute("DELETE FROM produtos WHERE id=?", (row['id'],))
                        conn.commit()
                        st.rerun()

            st.divider()

        # Área de Edição
        st.subheader("✏️ Editar um Produto")
        id_editar = st.selectbox("Selecione o ID do produto que deseja editar", df['id'])
        produto_edit = df[df['id'] == id_editar].iloc[0]

        with st.form("form_editar"):
            novo_nome = st.text_input("Nome", produto_edit['nome'])
            novo_preco = st.number_input("Preço", value=float(produto_edit['preco']), format="%.2f")
            nova_qtd = st.number_input("Quantidade", value=int(produto_edit['quantidade']), step=1)
            novo_status = st.selectbox("Status", ["Ativo", "Inativo"], index=0 if produto_edit['status'] == "Ativo" else 1)

            if st.form_submit_button("Atualizar Produto"):
                c.execute(
                    "UPDATE produtos SET nome=?, preco=?, quantidade=?, status=? WHERE id=?",
                    (novo_nome, novo_preco, nova_qtd, novo_status, int(id_editar))
                )
                conn.commit()
                st.success("Produto atualizado com sucesso!")
                st.rerun()
    else:
        st.info("Nenhum produto cadastrado ou encontrado no filtro atual.")
