import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração Básica
st.set_page_config(page_title="Gestão de Instalações", layout="centered")

# Lógica de Dados
def load_data():
    if os.path.exists("agendamentos.csv"):
        try:
            return pd.read_csv("agendamentos.csv")
        except:
            return pd.DataFrame(columns=["ID", "Data", "Placa", "Local", "Cliente", "Tecnico"])
    return pd.DataFrame(columns=["ID", "Data", "Placa", "Local", "Cliente", "Tecnico"])

df = load_data()

# Cabeçalho
col_logo, col_tit = st.columns([1, 3])
with col_logo:
    if os.path.exists("logo_empresa.png"):
        st.image("logo_empresa.png", width=100)
    else:
        st.write("🔵 **SISTEMA**")
with col_tit:
    st.title("Painel de Agendamentos")

# Formulário de Cadastro
with st.expander("➕ NOVO AGENDAMENTO", expanded=False):
    with st.form("cadastro"):
        data = st.date_input("Data do Serviço")
        hora = st.time_input("Horário")
        veiculo = st.text_input("Veículo/Placa", placeholder="Ex: TER3H09")
        cliente = st.text_input("Cliente", placeholder="Ex: Syngenta")
        tecnico = st.text_input("Técnico", placeholder="Ex: Alberto")
        local = st.text_area("Endereço")
        
        if st.form_submit_button("SALVAR"):
            data_str = f"{data.strftime('%d/%m/%Y')} {hora.strftime('%H:%M')}"
            novo_id = datetime.now().strftime("%Y%m%d%H%M%S")
            nova_linha = pd.DataFrame([[novo_id, data_str, veiculo, local, cliente, tecnico]], columns=df.columns)
            df = pd.concat([df, nova_linha], ignore_index=True)
            df.to_csv("agendamentos.csv", index=False)
            st.rerun()

st.write("---")

# Visualização dos Agendamentos (Usando componentes oficiais)
st.subheader("📋 Serviços Pendentes")

if not df.empty:
    for i, linha in df.iterrows():
        # Usamos uma "Border" nativa do Streamlit para criar o card sem bugs de cor
        with st.container(border=True):
            st.write(f"### 🕒 {linha['Data']}")
            st.write(f"**🚗 VEÍCULO:** {linha['Placa']}")
            st.write(f"**👤 CLIENTE:** {linha['Cliente']} | **🔧 TÉCNICO:** {linha['Tecnico']}")
            st.write(f"📍 {linha['Local']}")
            
            # Botão de Concluir
            if st.button(f"CONCLUIR SERVIÇO #{i}", key=str(linha['ID']), use_container_width=True):
                df = df.drop(i)
                df.to_csv("agendamentos.csv", index=False)
                st.rerun()
else:
    st.info("Nenhum agendamento encontrado.")
