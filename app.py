import streamlit as st
import pandas as pd
import os
from datetime import datetime

# CONFIGURAÇÃO DE TEMA (Forçando modo claro no conteúdo)
st.set_page_config(page_title="Controle de Instalações", layout="centered")

# CSS INJETADO - FOCO NO CONTRASTE
st.markdown("""
    <style>
    /* Fundo da página */
    .stApp { background-color: #E8F0F7; }
    
    /* Estilo do Card de Agendamento */
    .agendamento-card {
        background-color: #FFFFFF !important;
        border-left: 10px solid #004A99 !important;
        padding: 20px !important;
        border-radius: 12px !important;
        margin-bottom: 20px !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    /* Forçar cores de texto dentro do card */
    .card-title { color: #004A99 !important; font-size: 20px !important; font-weight: bold !important; margin-bottom: 5px; }
    .card-text { color: #333333 !important; font-size: 16px !important; margin: 5px 0; }
    .card-label { color: #666666 !important; font-weight: bold; }
    
    /* Botões */
    .stButton>button {
        background-color: #004A99;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# LÓGICA DE DADOS
def carregar_dados():
    if os.path.exists("agendamentos.csv"):
        return pd.read_csv("agendamentos.csv")
    return pd.DataFrame(columns=["ID", "Data", "Placa", "Local", "Cliente", "Tecnico"])

df = carregar_dados()

# CABEÇALHO
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("logo_empresa.png"):
        st.image("logo_empresa.png", width=120)
with col2:
    st.title("Painel de Agendamentos")

# FORMULÁRIO (Simplificado para evitar erros)
with st.expander("➕ Adicionar Novo", expanded=False):
    with st.form("add_form"):
        d = st.date_input("Data")
        h = st.time_input("Hora")
        v = st.text_input("Veículo/Placa")
        c = st.text_input("Cliente")
        l = st.text_area("Local/Endereço")
        t = st.text_input("Técnico")
        if st.form_submit_button("AGENDAR"):
            new_id = datetime.now().strftime("%H%M%S")
            data_f = f"{d.strftime('%d/%m/%Y')} às {h.strftime('%H:%M')}"
            nova_linha = pd.DataFrame([[new_id, data_f, v, l, c, t]], columns=df.columns)
            df = pd.concat([df, nova_linha], ignore_index=True)
            df.to_csv("agendamentos.csv", index=False)
            st.rerun()

st.write("---")

# LISTAGEM MELHORADA
if not df.empty:
    for i, linha in df.iterrows():
        # HTML PURO PARA O CARD (Para não herdar cores erradas do Streamlit)
        st.markdown(f"""
            <div class="agendamento-card">
                <div class="card-title">📅 {linha['Data']}</div>
                <div class="card-text"><b>VEÍCULO:</b> {linha['Placa']}</div>
                <div class="card-text"><b>CLIENTE:</b> {linha['Cliente']}</div>
                <div class="card-text"><b>TÉCNICO:</b> {linha['Tecnico']}</div>
                <div style="color: #555; font-size: 14px; margin-top: 10px;">📍 {linha['Local']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botão de conclusão
        if st.button(f"CONCLUIR {linha['Placa']}", key=str(linha['ID'])):
            df = df.drop(i)
            df.to_csv("agendamentos.csv", index=False)
            st.rerun()
else:
    st.info("Nenhum serviço pendente.")
