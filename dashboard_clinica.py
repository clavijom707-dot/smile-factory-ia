import streamlit as st
import json
import urllib.request

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Smile Factory - Tu Clínica Dental", page_icon="🦷", layout="wide")

# --- CÓDIGO CSS PARA DARLE ESTILO DE WEB REAL ---
st.markdown("""
    <style>
    /* Ocultar el menú de Streamlit para que parezca una web real */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo general y tipografía */
    .stApp {
        background-color: #f4f9f9;
    }
    
    /* Estilo para el título principal */
    .big-title {
        color: #0e4d64;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    
    /* Estilo para el subtítulo */
    .sub-title {
        color: #5c5c5c;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SEGURIDAD: Lee el token desde la bóveda ---
ia_token = st.secrets["DEEPSEEK_TOKEN"]

# --- ENCABEZADO DE LA WEB ---
st.markdown('<p class="big-title">🦷 Smile Factory</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Tu sonrisa perfecta, atendida por nuestra recepcionista virtual inteligente 24/7.</p>', unsafe_allow_html=True)

# --- CREAMOS DOS COLUMNAS: Izquierda (Info) y Derecha (Chat) ---
col_info, col_chat = st.columns([1, 1], gap="large")

with col_info:
    st.subheader("Bienvenido a la clínica")
    st.write("""
    En **Smile Factory** nos especializamos en brindarte la mejor atención dental. 
    Nuestra inteligencia artificial está disponible para agendar tu cita al instante, sin esperas.
    """)
    
    # Aquí puedes poner un link a una imagen generada por IA o una foto de stock
    # Por ahora usaremos una imagen de ejemplo de internet
    st.image("https://images.unsplash.com/photo-1606811841689-23dfddce3e95?q=80&w=1000&auto=format&fit=crop", caption="Instalaciones modernas de Smile Factory")
    
    st.markdown("### Nuestros Servicios")
    st.markdown("- 🦷 Limpieza Dental\n- 🪥 Ortodoncia (Brackets)\n- 🩺 Consulta General\n- ✨ Blanqueamiento")

with col_chat:
    # --- EL CEREBRO DE NATALY ---
    system_prompt = """
    Eres Nataly, la recepcionista virtual de la clínica dental 'Smile Factory'.
    Tus reglas:
    1. Eres amable, empática, profesional y usas un tono cálido.
    2. Tu objetivo principal es agendar una cita.
    3. Pregunta el nombre, el motivo y si prefiere en la mañana o en la tarde.
    4. IMPORTANTE: La agenda del doctor está llena en las tardes. SOLO ofrece citas en la MAÑANA (de 8:00 a 12:00). Si piden tarde, ofrece amablemente la mañana.
    5. NO des diagnósticos médicos. Si hay dolor agudo, da el número de emergencias (cero nueve nueve, nueve nueve nueve).
    6. Si el paciente acepta la cita, confírmala y despídete.
    """

    def chatear(mensajes):
        url = "https://api.deepseek.com/chat/completions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {ia_token}"}
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "system", "content": system_prompt}] + mensajes,
            "temperature": 0.7
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req) as res:
                return json.loads(res.read().decode())['choices'][0]['message']['content']
        except Exception as e:
            return f"Error de conexión: {e}"

    # --- INTERFAZ DEL CHAT ---
    st.subheader("💬 Agenda tu cita ahora")
    
    # Caja con borde para el chat
    with st.container(border=True):
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Bienvenido a Smile Factory. Soy Nataly, ¿en qué puedo ayudarle hoy? 🦷"}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Escribe aquí..."):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.spinner("Nataly está escribiendo..."):
                respuesta = chatear(st.session_state.messages)
                st.chat_message("assistant").markdown(respuesta)
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
