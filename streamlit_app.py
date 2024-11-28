import streamlit as st
import sqlite3
from datetime import datetime
import time
import re
import json

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Configuração da página
st.set_page_config(
    page_title="Chat em Tempo Real",
    page_icon="💭",
    layout="wide"
)

# Configurações de estilo
st.markdown("""
    <style>
    .user-message {
        text-align: right;
        color: #0066ff;
        padding: 5px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .other-message {
        text-align: left;
        color: #00cc00;
        padding: 5px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .timestamp {
        font-size: 0.8em;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Lista de emojis
EMOJI_LIST = ["😊", "😂", "❤️", "👍", "🎉", "🤔", "😎", "🎮", "🌟", "🔥"]

# Palavras proibidas
BANNED_WORDS = ["palavrão1", "palavrão2", "palavrão3"]

# Funções do banco de dados
def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (username TEXT, message TEXT, timestamp TEXT, 
                  is_private INTEGER DEFAULT 0, 
                  recipient TEXT DEFAULT NULL)''')
    conn.commit()
    conn.close()



def save_message(username, message, is_private=False, recipient=None):
    if not is_appropriate(message):
        return False
        
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%H:%M:%S")
    c.execute("""INSERT INTO messages (username, message, timestamp, is_private, recipient) 
                 VALUES (?, ?, ?, ?, ?)""",
              (username, message, timestamp, is_private, recipient))
    conn.commit()
    conn.close()
    return True

def load_messages():
    try:
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        c.execute("""SELECT username, message, timestamp, is_private, recipient 
                    FROM messages ORDER BY timestamp""")
        messages = c.fetchall()
        conn.close()
        return messages
    except sqlite3.OperationalError:
        st.error("Erro ao acessar o banco de dados")
        return []



def update_user_status(username):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%H:%M:%S")
    c.execute("REPLACE INTO user_status VALUES (?, ?)", (username, timestamp))
    conn.commit()
    conn.close()

def get_active_users():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("SELECT username, last_seen FROM user_status")
    users = c.fetchall()
    conn.close()
    return users

# Funções auxiliares
def is_appropriate(message):
    return not any(word in message.lower() for word in BANNED_WORDS)

def format_message(message):
    # Formatar links
    url_pattern = r'(https?://\S+)'
    message = re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', message)
    return message

def get_chat_stats():
    messages = load_messages()
    total_messages = len(messages)
    users = len(set([m[0] for m in messages]))
    return total_messages, users

# Inicializar banco de dados
init_db()

# Interface do usuário
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'
if 'last_message_count' not in st.session_state:
    st.session_state.last_message_count = 0

# Configuração de tema
if st.session_state.theme == 'Dark':
    st.markdown("""
        <style>
        .stApp {
            background-color: #1a1a1a;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

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
    
    # Atualizar status do usuário
    update_user_status(st.session_state.username)
    
    # Área de mensagens
    chat_container = st.container()
    
    # Área de input
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            message = st.text_input("Mensagem:", key="message_input")
        
        with col2:
            selected_emoji = st.selectbox("Emojis:", EMOJI_LIST)
            if st.button("Add Emoji"):
                message += selected_emoji
        
        with col3:
            users = [u[0] for u in get_active_users()]
            recipient = st.selectbox("Enviar para:", ["Todos"] + users)
            is_private = recipient != "Todos"
        
        if st.button("Enviar") and message:
            if save_message(st.session_state.username, message, is_private, recipient):
                st.rerun()
            else:
                st.error("Mensagem contém conteúdo inadequado!")

                    # Exibir mensagens
    with chat_container:
        messages = load_messages()
        for username, msg, timestamp, is_private, recipient in messages:
            # Verificar se a mensagem deve ser exibida para este usuário
            should_display = (
                not is_private or 
                username == st.session_state.username or 
                recipient == st.session_state.username
            )
            
            if should_display:
                formatted_msg = format_message(msg)
                if username == st.session_state.username:
                    st.markdown(
                        f"""<div class="user-message">
                            <span class="timestamp">[{timestamp}]</span>
                            <strong>Você:</strong> {formatted_msg}
                            </div>""", 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""<div class="other-message">
                            <span class="timestamp">[{timestamp}]</span>
                            <strong>{username}:</strong> {formatted_msg}
                            </div>""", 
                        unsafe_allow_html=True
                    )
    
    # Atualização automática
    time.sleep(1)
    st.rerun()

# Sidebar com opções e estatísticas
with st.sidebar:
    st.title("Opções")
    
    # Tema
    theme = st.selectbox(
        "Tema:",
        ["Light", "Dark"],
        key="theme_selector"
    )
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()
    
    # Pesquisa
    search_term = st.text_input("Pesquisar mensagens:")
    if search_term:
        messages = [m for m in load_messages() if search_term.lower() in m[1].lower()]
        st.write(f"Resultados encontrados: {len(messages)}")
    
    # Estatísticas
    st.title("Estatísticas")
    total_msgs, total_users = get_chat_stats()
    st.metric("Total de Mensagens", total_msgs)
    st.metric("Usuários Ativos", total_users)
    
    # Usuários online
    st.title("Usuários Online")
    active_users = get_active_users()
    for user, last_seen in active_users:
        st.write(f"👤 {user} - Último acesso: {last_seen}")
    
    # Limpar chat
    if st.button("Limpar Chat"):
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        c.execute("DELETE FROM messages")
        conn.commit()
        conn.close()
        st.rerun()

# Notificações de novas mensagens
current_count = len(load_messages())
if current_count > st.session_state.last_message_count:
    st.balloons()
    st.session_state.last_message_count = current_count

# Rodapé
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Chat desenvolvido com Streamlit</p>
        <p>© 2024 - Todos os direitos reservados</p>
    </div>
""", unsafe_allow_html=True)
