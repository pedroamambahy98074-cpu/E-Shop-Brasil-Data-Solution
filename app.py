import streamlit as st
from pymongo import MongoClient
from faker import Faker
import pandas as pd
import os
import random

# --- Configuração do MongoDB ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "eshop_db"
COLLECTION_CLIENTES = "clientes"
COLLECTION_PEDIDOS = "pedidos"

@st.cache_resource
def init_connection():
    """Inicializa a conexão com o MongoDB."""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        return db
    except Exception as e:
        st.error(f"Erro ao conectar ao MongoDB: {e}")
        return None

db = init_connection()
fake = Faker('pt_BR')

# --- Funções de Manipulação de Dados ---

def generate_fake_data(num_clientes=10, num_pedidos=50):
    """Gera dados falsos para clientes e pedidos."""
    if db is None:
        return

    # 1. Clientes
    clientes_data = []
    for i in range(num_clientes):
        clientes_data.append({
            "_id": i + 1,
            "nome": fake.name(),
            "email": fake.email(),
            "cidade": fake.city(),
            "estado": fake.state_abbr(),
            "data_cadastro": fake.date_this_year().isoformat()
        })
    
    # 2. Pedidos
    pedidos_data = []
    for i in range(num_pedidos):
        pedidos_data.append({
            "_id": i + 1,
            "cliente_id": random.randint(1, num_clientes),
            "data_pedido": fake.date_this_year().isoformat(),
            "valor_total": round(random.uniform(50.0, 5000.0), 2),
            "status": random.choice(["Processando", "Enviado", "Entregue", "Cancelado"]),
            "itens": [
                {"produto": fake.word(), "quantidade": random.randint(1, 5), "preco_unitario": round(random.uniform(10.0, 500.0), 2)}
                for _ in range(random.randint(1, 3))
            ]
        })

    # Inserção no DB
    db[COLLECTION_CLIENTES].drop()
    db[COLLECTION_PEDIDOS].drop()
    db[COLLECTION_CLIENTES].insert_many(clientes_data)
    db[COLLECTION_PEDIDOS].insert_many(pedidos_data)
    st.success(f"Dados gerados: {num_clientes} clientes e {num_pedidos} pedidos inseridos.")

def insert_cliente(nome, email, cidade, estado):
    """Insere um novo cliente."""
    if db is None: return
    
    # Encontra o próximo ID
    last_cliente = db[COLLECTION_CLIENTES].find_one(sort=[("_id", -1)])
    new_id = (last_cliente["_id"] + 1) if last_cliente else 1
    
    cliente = {
        "_id": new_id,
        "nome": nome,
        "email": email,
        "cidade": cidade,
        "estado": estado,
        "data_cadastro": pd.Timestamp.now().isoformat()
    }
    db[COLLECTION_CLIENTES].insert_one(cliente)
    st.success(f"Cliente '{nome}' inserido com sucesso! ID: {new_id}")

def update_cliente(cliente_id, nome, email, cidade, estado):
    """Edita um cliente existente."""
    if db is None: return
    result = db[COLLECTION_CLIENTES].update_one(
        {"_id": cliente_id},
        {"$set": {"nome": nome, "email": email, "cidade": cidade, "estado": estado}}
    )
    if result.modified_count:
        st.success(f"Cliente ID {cliente_id} atualizado com sucesso.")
    else:
        st.warning(f"Cliente ID {cliente_id} não encontrado ou nenhum dado modificado.")

def delete_cliente(cliente_id):
    """Exclui um cliente."""
    if db is None: return
    result = db[COLLECTION_CLIENTES].delete_one({"_id": cliente_id})
    if result.deleted_count:
        st.success(f"Cliente ID {cliente_id} excluído com sucesso.")
    else:
        st.warning(f"Cliente ID {cliente_id} não encontrado.")

def get_all_clientes():
    """Retorna todos os clientes como DataFrame."""
    if db is None: return pd.DataFrame()
    clientes = list(db[COLLECTION_CLIENTES].find())
    return pd.DataFrame(clientes)

def get_clientes_por_estado(estado):
    """Consulta clientes por estado."""
    if db is None: return pd.DataFrame()
    clientes = list(db[COLLECTION_CLIENTES].find({"estado": estado}))
    return pd.DataFrame(clientes)

def get_total_gasto_por_cliente():
    """Simula a concatenação/agregação de dados (Big Data Insight)."""
    if db is None: return pd.DataFrame()
    
    # Pipeline de Agregação do MongoDB
    pipeline = [
        # 1. Agrupar pedidos por cliente_id e somar o valor total
        {"$group": {
            "_id": "$cliente_id",
            "total_gasto": {"$sum": "$valor_total"},
            "total_pedidos": {"$sum": 1}
        }},
        # 2. Renomear _id para cliente_id
        {"$project": {
            "cliente_id": "$_id",
            "total_gasto": {"$round": ["$total_gasto", 2]},
            "total_pedidos": 1,
            "_id": 0
        }},
        # 3. Ordenar pelo total gasto
        {"$sort": {"total_gasto": -1}}
    ]
    
    gastos_pedidos = list(db[COLLECTION_PEDIDOS].aggregate(pipeline))
    df_gastos = pd.DataFrame(gastos_pedidos)
    
    if df_gastos.empty:
        return pd.DataFrame()

    # Concatenação (simulando JOIN com dados de clientes)
    df_clientes = get_all_clientes()[["_id", "nome", "email"]]
    df_clientes.rename(columns={"_id": "cliente_id"}, inplace=True)
    
    # Merge dos DataFrames (simulando a junção de dados)
    df_final = pd.merge(df_gastos, df_clientes, on="cliente_id", how="left")
    
    return df_final.sort_values(by="total_gasto", ascending=False)


# --- Interface Streamlit ---

st.set_page_config(layout="wide", page_title="E-Shop Brasil - Gestão de Dados e Big Data")

st.title("🇧🇷 E-Shop Brasil: Solução de Gestão de Dados e Big Data")
st.subheader("Aplicação Prática com MongoDB e Streamlit")

if db is None:
    st.warning("A conexão com o MongoDB não foi estabelecida. Verifique o `docker-compose.yml` e o `MONGO_URI`.")
else:
    # Sidebar para navegação
    menu = ["Visão Geral", "Inserção de Dados", "Manipulação (CRUD)", "Consultas e Insights (Big Data)"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Visão Geral":
        st.header("Visão Geral dos Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("Clientes Atuais")
            df_clientes = get_all_clientes()
            st.dataframe(df_clientes, height=300)
            st.metric("Total de Clientes", len(df_clientes))
            
        with col2:
            st.info("Pedidos Atuais")
            df_pedidos = pd.DataFrame(list(db[COLLECTION_PEDIDOS].find()))
            st.dataframe(df_pedidos, height=300)
            st.metric("Total de Pedidos", len(df_pedidos))
            
        st.markdown("---")
        st.header("Geração de Dados Falsos (Mock Data)")
        st.write("Use esta opção para popular o banco de dados com dados de teste.")
        if st.button("Gerar e Inserir Dados Falsos"):
            generate_fake_data()
            st.rerun() # Recarrega a página para mostrar os novos dados

    elif choice == "Inserção de Dados":
        st.header("Inserir Novo Cliente")
        with st.form("form_inserir_cliente"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail")
            cidade = st.text_input("Cidade")
            estado = st.selectbox("Estado", ["SP", "RJ", "MG", "BA", "RS", "Outro"])
            submitted = st.form_submit_button("Inserir Cliente")
            if submitted and nome and email:
                insert_cliente(nome, email, cidade, estado)
                st.rerun()

    elif choice == "Manipulação (CRUD)":
        st.header("Editar ou Excluir Cliente")
        
        df_clientes = get_all_clientes()
        if df_clientes.empty:
            st.warning("Nenhum cliente encontrado. Gere dados na Visão Geral.")
        else:
            cliente_ids = df_clientes["_id"].tolist()
            
            # Seleção do Cliente
            cliente_id_selecionado = st.selectbox("Selecione o ID do Cliente para Manipulação", cliente_ids)
            cliente_selecionado = df_clientes[df_clientes["_id"] == cliente_id_selecionado].iloc[0]
            
            st.markdown("---")
            
            # Formulário de Edição
            st.subheader("Editar Dados do Cliente")
            with st.form("form_editar_cliente"):
                nome_edit = st.text_input("Nome", value=cliente_selecionado["nome"])
                email_edit = st.text_input("E-mail", value=cliente_selecionado["email"])
                cidade_edit = st.text_input("Cidade", value=cliente_selecionado["cidade"])
                estado_edit = st.selectbox("Estado", ["SP", "RJ", "MG", "BA", "RS", "Outro"], index=["SP", "RJ", "MG", "BA", "RS", "Outro"].index(cliente_selecionado["estado"]) if cliente_selecionado["estado"] in ["SP", "RJ", "MG", "BA", "RS", "Outro"] else 5)
                
                submitted_edit = st.form_submit_button("Salvar Edição")
                if submitted_edit:
                    update_cliente(cliente_id_selecionado, nome_edit, email_edit, cidade_edit, estado_edit)
                    st.rerun()
            
            st.markdown("---")
            
            # Exclusão
            st.subheader("Excluir Cliente")
            if st.button(f"Excluir Cliente ID {cliente_id_selecionado}", help="Esta ação é irreversível.", type="primary"):
                delete_cliente(cliente_id_selecionado)
                st.rerun()

    elif choice == "Consultas e Insights (Big Data)":
        st.header("Análise de Dados e Insights (Simulação Big Data)")
        
        tab1, tab2 = st.tabs(["Clientes por Estado", "Top Clientes por Gasto"])
        
        with tab1:
            st.subheader("Consulta: Distribuição Geográfica de Clientes")
            estado_consulta = st.selectbox("Selecione o Estado para Filtrar", ["Todos", "SP", "RJ", "MG", "BA", "RS"])
            
            if estado_consulta == "Todos":
                df_consulta = get_all_clientes()
            else:
                df_consulta = get_clientes_por_estado(estado_consulta)
                
            st.write(f"Clientes encontrados em {estado_consulta}: {len(df_consulta)}")
            st.dataframe(df_consulta)
            
            if not df_consulta.empty:
                st.bar_chart(df_consulta["cidade"].value_counts().head(10))

        with tab2:
            st.subheader("Insight de Big Data: Top Clientes por Gasto Total")
            st.write("Esta consulta simula a concatenação de dados de clientes e pedidos, um processo comum em análise de Big Data para identificar clientes de alto valor.")
            
            df_top_clientes = get_total_gasto_por_cliente()
            
            if df_top_clientes.empty:
                st.warning("Não há dados de pedidos para realizar a agregação.")
            else:
                st.dataframe(df_top_clientes)
                st.bar_chart(df_top_clientes.set_index("nome")["total_gasto"].head(10))
