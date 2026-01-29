import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Configuração de Página e Tema
st.set_page_config(page_title="Gestão de Instalações", layout="centered")

# 2. CSS "Blindado" (Resolve o problema do fundo branco/texto invisível)
st.markdown("""
    <style>
    /* Força o fundo da página para um cinza muito claro */
    .stApp {
        background-color: #f4f7f9 !important;
    }
    
    /* Card de Agendamento - Cores Fixas */
    .card-container {
        background-color: #ffffff !important;
        border-radius: 15px !important;
        padding: 25px !important;
        margin-bottom: 20px !important;
        border-left: 12px solid #004A99 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        color: #222222 !important; /* Texto sempre escuro */
    }
    
    /* Estilização dos textos internos do card */
    .card-date { color: #004A99 !important; font-size: 1.2em !important; font-weight: bold !important; }
    .card-title { color: #111111 !important; font-size: 1.3em !important; font-weight: 800 !important; margin: 10px 0 !important; }
    .card-info { color: #444444 !important; font-size: 1em !important; line-height: 1.6 !important; }
    .card-label { font-weight: bold; color: #000000; }
    
    /* Botões personalizados */
    .stButton>button {
        background-color: #004A99 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
        width: 100%;
    }
    
    /* Títulos da página */
    h1, h2, h3 { color: #004A99 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Gerenciamento de Dados
def load_data():
    if os.path.exists("agendamentos.csv"):
        return pd.read_csv("agendamentos.csv")
    return pd.DataFrame(columns=["ID", "Data", "Placa", "Local", "Cliente", "Tecnico"])

df = load_data()

# 4. Cabeçalho
col_logo, col_titulo = st.columns([1, 3])
with col_logo:
    # Ajustado para o nome do arquivo que você confirmou
    if os.path.exists("logo_empresa.png"):
        st.image("logo_empresa.png", width=120)
with col_titulo:
    st.title("Painel de Controle")

# 5. Cadastro (Formulário)
with st.expander("➕ Adicionar Novo Agendamento", expanded=False):
    with st.form("form_novo"):
        c1, c2 = st.columns(2)
        data_sel = c1.date_input("Data")
        hora_sel = c2.time_input("Hora")
        veiculo = st.text_input("Veículo/Placa")
        cliente = st.text_input("Cliente/Empresa")
        tecnico = st.text_input("Técnico Responsável")
        local = st.text_area("Endereço Completo")
        
        if st.form_submit_button("SALVAR NO SISTEMA"):
            new_id = datetime.now().strftime("%Y%m%d%H%M%S")
            data_str = f"{data_sel.strftime('%d/%m/%Y')} às {hora_sel.strftime('%H:%M')}"
            nova_linha = pd.DataFrame([[new_id, data_str, veiculo, local, cliente, tecnico]], columns=df.columns)
            df = pd.concat([df, nova_linha], ignore_index=True)
            df.to_csv("agendamentos.csv", index=False)
            st.success
