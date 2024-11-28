import streamlit as st
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="Chat em Tempo Real",
    page_icon="💭",
    layout="wide"
)

# Inicialização do estado global
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

# Função para adicionar mensagem
def add_message(user, message):
    st.session_state.messages.append({
        "user": user,
        "message": message,
        "time": datetime.now().strftime("%H:%M:%S")
    })

# Interface principal
st.title("💭 Chat em Tempo Real")

# Login do usuário
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# Tela de login
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
        for msg in st.session_state.messages:
            st.write(f"[{msg['time']}] {msg['user']}: {msg['message']}")
    
    # Campo de mensagem
    message = st.text_input("Digite sua mensagem:", key="message_input")
    if st.button("Enviar") or message:
        if message:  # Verifica se a mensagem não está vazia
            add_message(st.session_state.user_name, message)
            st.session_state.messages = st.session_state.messages  # Força atualização
            st.rerun()

    # Atualização automática a cada 2 segundos
    if time.time() - st.session_state.last_refresh > 2:
        st.session_state.last_refresh = time.time()
        st.rerun()

# Sidebar com opções
with st.sidebar:
    st.title("Opções")
    if st.button("Limpar Chat"):
        st.session_state.messages = []
        st.rerun()
    
    # Exibir número de mensagens
    st.write(f"Total de mensagens: {len(st.session_state.messages)}")
    
    # Exibir usuários online
    users = set(msg['user'] for msg in st.session_state.messages)
    st.write(f"Usuários que participaram: {', '.join(users)}")

# Rodapé
st.markdown("---")
st.markdown("Chat desenvolvido com Streamlit")
