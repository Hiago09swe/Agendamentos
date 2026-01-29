import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Configuração inicial
st.set_page_config(page_title="Sistema de Agendamentos", layout="centered")

# 2. Estilo Azul
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #0056b3; color: white; border-radius: 5px; width: 100%; }
    h1 { color: #0056b3; }
    </style>
    """, unsafe_allow_html=True)

# 3. Função de carregar dados com tratamento de erro
def carregar_dados():
    if os.path.exists("agendamentos.csv"):
        try:
            return pd.read_csv("agendamentos.csv")
        except:
            return pd.DataFrame(columns=["ID", "Data", "Placa", "Local", "Cliente", "Tecnico"])
    return pd.DataFrame(columns=["ID", "Data", "Placa", "Local", "Cliente", "Tecnico"])

df = carregar_dados()

# 4. Cabeçalho com o seu Logo
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("logo_empresa.png"):
        st.image("logo_empresa.png", width=100)
    else:
        st.info("Logo?")

with col2:
    st.title("Meus Agendamentos")

# 5. Formulário
with st.expander("📝 Novo Registro", expanded=False):
    with st.form("meu_form"):
        d = st.date_input("Data")
        h = st.time_input("Hora")
        veiculo = st.text_input("Veículo/Placa")
        cli = st.text_input("Cliente")
        end = st.text_area("Endereço")
        tec = st.text_input("Técnico")
        
        if st.form_submit_button("Salvar"):
            data_hora = f"{d.strftime('%d/%m/%Y')} {h.strftime('%H:%M')}"
            novo_id = datetime.now().strftime("%Y%m%d%H%M%S")
            nova_linha = pd.DataFrame([[novo_id, data_hora, veiculo, end, cli, tec]], columns=df.columns)
            df = pd.concat([df, nova_linha], ignore_index=True)
            df.to_csv("agendamentos.csv", index=False)
            st.success("Salvo!")
            st.rerun()

st.divider()

# 6. Lista de Agendamentos (Interface Corrigida)
st.subheader("🗓️ Próximos Serviços")

if not df.empty:
    for i, linha in df.iterrows():
        with st.container():
            # Card com fundo branco sólido e texto escuro para visibilidade total
            st.markdown(f"""
            <div style="
                border-left: 8px solid #0056b3; 
                padding: 20px; 
                background-color: #ffffff; 
                margin-bottom: 5px; 
                border-radius: 10px; 
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                color: #1a1a1a !important;
            ">
                <div style="font-size: 1.1em; font-weight: bold; color: #0056b3; margin-bottom: 5px;">
                    🕒 {linha['Data']}
                </div>
                <div style="font-size: 1.2em; font-weight: bold; margin-bottom: 8px;">
                    🚗 {linha['Placa']}
                </div>
                <div style="margin-bottom: 5px;">
                    <b>👤 Cliente:</b> {linha['Cliente']}
                </div>
                <div style="margin-bottom: 5px;">
                    <b>🔧 Técnico:</b> {linha['Tecnico']}
                </div>
                <div style="font-size: 0.9em; line-height: 1.4; color: #444;">
                    📍 {linha['Local']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botão centralizado logo abaixo do card
            if st.button(f"✅ Concluir {linha['Placa']}", key=str(linha['ID'])):
                df = df.drop(i)
                df.to_csv("agendamentos.csv", index=False)
                st.rerun()
            st.markdown("---") # Linha de separação entre agendamentos
else:
    st.info("Tudo limpo! Nenhum agendamento pendente.")

