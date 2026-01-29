import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da página
st.set_page_config(page_title="Gestão de Agendamentos", page_icon="📅", layout="centered")

# Estilização em tons de azul (Fundo azul escuro para botões e títulos)
st.markdown("""
    <style>
    .main { background-color: #f0f5ff; }
    .stButton>button { 
        background-color: #0056b3; 
        color: white; 
        border-radius: 8px; 
        height: 3em;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #003d80; border: 1px solid white; }
    h1, h2, h3 { color: #003366; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    div[data-testid="stExpander"] { background-color: white; border-radius: 10px; border: 1px solid #d1e3ff; }
    </style>
    """, unsafe_allow_html=True)

# Lógica de Dados
def load_data():
    if os.path.exists("agendamentos.csv"):
        return pd.read_csv("agendamentos.csv")
    return pd.DataFrame(columns=["ID", "Data", "Placa", "Local", "Maps", "Cliente", "Tecnico"])

def save_data(df):
    df.to_csv("agendamentos.csv", index=False)

df = load_data()

# Cabeçalho com Logo
col_l, col_t = st.columns([1, 3])
with col_l:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.write("🟦 **LOGO**")
with col_t:
    st.title("Painel de Instalações")

# Formulário de Cadastro
with st.expander("➕ Agendar Novo Serviço", expanded=False):
    with st.form("novo_agendamento"):
        c1, c2 = st.columns(2)
        d = c1.date_input("Data")
        h = c2.time_input("Hora")
        placa = st.text_input("Veículo/Placa", value="TER3H09 | FIAT/STRADA VOLCANO 13AT")
        cliente = st.text_input("Cliente/Contato", value="Syngenta (Andressa +55 63 9120-9383)")
        tecnico = st.text_input("Técnico", value="Alberto - Palmas TO")
        local = st.text_area("Endereço", value="QUADRA 812 SUL, AVENIDA LO-19, QI-08, LOTE 15")
        link = st.text_input("Link Google Maps", value="https://maps.app.goo.gl/aRaPrFjjNDiCKrGM7")
        
        if st.form_submit_button("SALVAR AGENDAMENTO"):
            novo_id = datetime.now().strftime("%Y%m%d%H%M%S")
            data_str = f"{d.strftime('%d/%m/%Y')} às {h.strftime('%H:%M')}"
            novo_df = pd.DataFrame([[novo_id, data_str, placa, local, link, cliente, tecnico]], columns=df.columns)
            df = pd.concat([df, novo_df], ignore_index=True)
            save_data(df)
            st.success("Agendado!")
            st.rerun()

st.markdown("---")

# Exibição dos Agendamentos Ativos
st.subheader("🗓️ Serviços Pendentes")

if not df.empty:
    for index, row in df.iterrows():
        # Layout do Card
        with st.container():
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 15px; border-left: 10px solid #0056b3; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <span style="color: #0056b3; font-weight: bold; font-size: 1.2em;">🕒 {row['Data']}</span><br>
                <b style="font-size: 1.1em;">🚗 {row['Placa']}</b><br>
                <hr style="margin: 10px 0; border: 0; border-top: 1px solid #eee;">
                <b>👤 Cliente:</b> {row['Cliente']}<br>
                <b>🔧 Técnico:</b> {row['Tecnico']}<br>
                <b>📍 Local:</b> {row['Local']}<br>
                <a href="{row['Maps']}" target="_blank" style="color: #0056b3; text-decoration: none; font-weight: bold;">➡️ Ver no Mapa</a>
            </div>
            """, unsafe_allow_html=True)
            
            # Botão de Concluir (fora do markdown para ter funcionalidade)
            if st.button(f"✅ Concluir Serviço: {row['Placa']}", key=row['ID']):
                df = df.drop(index)
                save_data(df)
                st.toast(f"Serviço {row['Placa']} concluído!")
                st.rerun()
else:
    st.info("Tudo em dia! Nenhum agendamento pendente.")