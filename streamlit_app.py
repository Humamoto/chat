import streamlit as st
import json
from datetime import datetime
import time
import os

MESSAGES_FILE = ".streamlit/messages.json"


# Configuração da página
st.set_page_config(
    page_title="Chat em Tempo Real",
    page_icon="💭",
    layout="wide"
)

# Função para carregar mensagens do arquivo
def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        os.makedirs(os.path.dirname(MESSAGES_FILE), exist_ok=True)
        with open(MESSAGES_FILE, 'w') as f:
            json.dump([], f)
    with open(MESSAGES_FILE, 'r') as f:
        return json.load(f)

# Função para salvar mensagens no arquivo
def save_message(username, message):
    messages = load_messages()
    messages.append({
        'username': username,
        'message': message,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f)


# Inicialização
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'last_message_count' not in st.session_state:
    st.session_state.last_message_count = 0

# Login
if not st.session_state.username:
    st.title('💭 Chat em Tempo Real')
    username = st.text_input('Digite seu nome:')
    if st.button('Entrar') and username:
        st.session_state.username = username
        st.rerun()

# Chat principal
if st.session_state.username:
    st.title(f'💭 Chat - {st.session_state.username}')
    
    # Área de mensagens
    chat_placeholder = st.empty()
    
    # Input de mensagem
    with st.container():
        message = st.text_input('Mensagem:', key='message_input')
        if st.button('Enviar'):
            if message:
                save_message(st.session_state.username, message)
                st.session_state.last_message_count += 1
                st.rerun()

    # Atualização automática das mensagens
    while True:
        messages = load_messages()
        if len(messages) > st.session_state.last_message_count:
            with chat_placeholder.container():
                for msg in messages:
                    st.text(f"[{msg['timestamp']}] {msg['username']}: {msg['message']}")
            st.session_state.last_message_count = len(messages)
        time.sleep(1)

# Sidebar
with st.sidebar:
    st.title('Opções')
    if st.button('Limpar Chat'):
        with open('messages.json', 'w') as f:
            json.dump([], f)
        st.rerun()
