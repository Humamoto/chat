# chat_app.py
import streamlit as st
import time
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Chat App",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo personalizado
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização do histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inicialização de usuários
if "username" not in st.session_state:
    st.session_state.username = ""

# Interface de login
if not st.session_state.username:
    st.title("💬 Chat App")
    username = st.text_input("Digite seu nome de usuário:")
    if st.button("Entrar") and username:
        st.session_state.username = username
        st.experimental_rerun()

# Interface principal do chat
if st.session_state.username:
    st.title(f"💬 Chat App - {st.session_state.username}")
    
    # Área de mensagens
    chat_container = st.container()
    
    # Exibir mensagens
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(f"{message['time']} - {message['content']}")
    
    # Campo de entrada de mensagem
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adicionar timestamp
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Adicionar mensagem ao histórico
        st.session_state.messages.append({
            "role": "user",
            "content": f"{st.session_state.username}: {prompt}",
            "time": current_time
        })
        
        # Rolar para última mensagem
        st.experimental_rerun()

# Botão para limpar chat
if st.sidebar.button("Limpar Chat"):
    st.session_state.messages = []
    st.experimental_rerun()