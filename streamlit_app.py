import streamlit as st
import sqlite3
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="Chat em Tempo Real",
    page_icon="💭",
    layout="wide"
)

# Criar/conectar ao banco de dados SQLite
def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (username TEXT, message TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

# Função para salvar mensagem
def save_message(username, message):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%H:%M:%S")
    c.execute("INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)",
              (username, message, timestamp))
    conn.commit()
    conn.close()

# Função para carregar mensagens
def load_messages():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("SELECT username, message, timestamp FROM messages")
    messages = c.fetchall()
    conn.close()
    return messages

# Inicializar banco de dados
init_db()

# Interface do usuário
if 'username' not in st.session_state:
    st.session_state.username = ''

# Tela de login
if not st.session_state.username:
    st.title("💭 Chat em Tempo Real")
    col1, col2 = st.columns([2,1])
    with col1:
        input_username = st.text_input("Digite seu nome:")
    with col2:
        if st.button("Entrar") and input_username:
            st.session_state.username = input_username
            st.rerun()

# Interface principal do chat
if st.session_state.username:
    st.title(f"Chat - Usuário: {st.session_state.username}")
    
    # Área de mensagens
    chat_container = st.container()
    
    # Área de input
    with st.container():
        message = st.text_input("Mensagem:", key="message_input")
        if st.button("Enviar") and message:
            save_message(st.session_state.username, message)
            st.rerun()
    
    # Exibir mensagens
    with chat_container:
        messages = load_messages()
        for username, msg, timestamp in messages:
            st.write(f"[{timestamp}] {username}: {msg}")
    
    # Atualização automática
    time.sleep(1)
    st.rerun()

# Sidebar
with st.sidebar:
    st.title("Opções")
    if st.button("Limpar Chat"):
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        c.execute("DELETE FROM messages")
        conn.commit()
        conn.close()
        st.rerun()
