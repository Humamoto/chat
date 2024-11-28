import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Configuração da página
st.set_page_config(
    page_title="Chat em Tempo Real",
    page_icon="💭",
    layout="wide"
)

# Inicialização do histórico
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Função para salvar mensagens no log
def save_to_log(message_data):
    log_file = "chat_log.json"
    try:
        if os.path.exists(log_file):
            with open(log_file, "r", encoding='utf-8') as f:
                log = json.load(f)
        else:
            log = []
        
        log.append(message_data)
        
        with open(log_file, "w", encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Erro ao salvar log: {e}")

# Interface principal
st.title("💭 Chat em Tempo Real")

# Login do usuário
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.user_name:
    with st.form("login_form"):
        user_name = st.text_input("Digite seu nome para entrar no chat:")
        submit = st.form_submit_button("Entrar")
        if submit and user_name:
            st.session_state.user_name = user_name
            st.rerun()

# Interface do chat
if st.session_state.user_name:
    st.write(f"Bem-vindo(a), {st.session_state.user_name}! 👋")
    
    # Área de mensagens
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(f"{message['time']} - {message['user']}: {message['content']}")
    
    # Campo de mensagem
    if message := st.chat_input("Digite sua mensagem..."):
        # Criar dados da mensagem
        message_data = {
            "role": "user",
            "user": st.session_state.user_name,
            "content": message,
            "time": datetime.now().strftime("%H:%M:%S")
        }
        
        # Adicionar à lista de mensagens
        st.session_state.messages.append(message_data)
        
        # Salvar no log
        save_to_log(message_data)
        
        # Atualizar chat
        st.rerun()

# Sidebar com opções
with st.sidebar:
    st.title("Opções")
    if st.button("Limpar Chat"):
        st.session_state.messages = []
        st.rerun()
    
    # Exibir histórico de mensagens
    st.title("Histórico")
    if os.path.exists("chat_log.json"):
        with open("chat_log.json", "r", encoding='utf-8') as f:
            log = json.load(f)
            df = pd.DataFrame(log)
            st.dataframe(df[["time", "user", "content"]])
