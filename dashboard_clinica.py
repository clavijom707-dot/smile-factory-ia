import streamlit as st
import json
import urllib.request

# --- CONFIGURACIÓN DE PÁGINA (Forzamos barra lateral abierta) ---
st.set_page_config(
    page_title="Smile Factory - Clínica Dental", 
    page_icon="🦷", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CÓDIGO CSS (Quita menús feos y deja la flechita del panel) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Estilos visuales */
    .stApp {background-color: #f8f9fa;}
    .big-title {color: #0e4d64; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; font-size: 3.5rem; margin-bottom: 0px;}
    .sub-title {color: #6c757d; font-size: 1.2rem; margin-bottom: 20px;}
    .st-emotion-cache-1v0mbdj img {border-radius: 15px;}
    
    /* Iconos sociales */
    .social-links a {
        text-decoration: none;
        font-size: 1.1rem;
        margin-right: 20px;
        font-weight: bold;
        color: #0e4d64;
    }
    .social-links a:hover { color: #007bff; }
    </style>
""", unsafe_allow_html=True)

# --- SEGURIDAD ---
ia_token = st.secrets["DEEPSEEK_TOKEN"]

# --- INICIALIZAR CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Bienvenido a Smile Factory. Soy Nataly, ¿en qué puedo ayudarle hoy? 🦷"}]

# --- PANEL DE ADMINISTRADOR ---
with st.sidebar:
    st.header("⚙️ Acceso Doctores")
    password = st.text_input("Contraseña:", type="password")
    
    if password == "smile2026":
        st.success("Modo Administrador Activado")
        
        opcion = st.radio(
            "Seleccione el horario de atención de hoy:",
            ("Solo Mañanas (8am - 12pm)", "Solo Tardes (2pm - 6pm)", "Mañana y Tarde", "Personalizado...")
        )
        
        if opcion == "Solo Mañanas (8am - 12pm)":
            horario_personalizado = "La agenda está llena en las tardes. SOLO ofrece citas en la MAÑANA (8:00 a 12:00)."
        elif opcion == "Solo Tardes (2pm - 6pm)":
            horario_personalizado = "La agenda está llena en las mañanas. SOLO ofrece citas en la TARDE (14:00 a 18:00)."
        elif opcion == "Mañana y Tarde":
            horario_personalizado = "El doctor atiende en la MAÑANA (8:00 a 12:00) y en la TARDE (14:00 a 18:00). Ofrece ambos horarios al paciente."
        else:
            horario_personalizado = st.text_area(
                "Escriba la instrucción exacta:", 
                value="Hoy el doctor solo atiende en la tarde de 3 a 5 PM."
            )
            
        st.divider()
        
        if st.button("🗑️ Limpiar Historial de Chat"):
            st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Bienvenido a Smile Factory. Soy Nataly, ¿en qué puedo ayudarle hoy? 🦷"}]
            st.rerun() 
            
    else:
        horario_personalizado = "La agenda está llena en las tardes. SOLO ofrece citas en la MAÑANA (8:00 a 12:00)."

# --- ENCABEZADO ---
st.markdown('<p class="big-title">🦷 Smile Factory</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Tecnología y salud dental en un solo lugar. Agenda tu cita con Nataly, nuestra IA 24/7.</p>', unsafe_allow_html=True)

# --- REDES SOCIALES ---
st.markdown("""
    <div class="social-links">
        <a href="https://facebook.com" target="_blank">📘 Facebook</a>
        <a href="https://instagram.com" target="_blank">📸 Instagram</a>
        <a href="https://tiktok.com" target="_blank">🎵 TikTok</a>
    </div>
    <br>
""", unsafe_allow_html=True)

# --- COLUMNAS ---
col_info, col_chat = st.columns([1, 1], gap="large")

with col_info:
    # AQUÍ ESTÁ EL TRUCO: Usamos un enlace web directo a una foto de clínica hermosa.
    # Así nunca fallará por "archivo no encontrado".
    st.image("foto_smile.jpg", use_container_width=True)
    
    st.write("### Bienvenido a la excelencia dental")
    st.write("En **Smile Factory** combinamos la calidez humana con la inteligencia artificial más avanzada. Nuestra recepcionista virtual está disponible las 24 horas.")
    st.markdown("#### Nuestros Servicios")
    st.markdown("- 🦷 **Limpieza Dental**\n- 🪥 **Ortodoncia**\n- 🩺 **Consulta General**\n- ✨ **Blanqueamiento**")

with col_chat:
    system_prompt = f"""
    Eres Nataly, la recepcionista virtual de la clínica dental 'Smile Factory'.
    Tus reglas:
    1. Eres amable, empática, profesional y usas un tono cálido.
    2. Tu objetivo principal es agendar una cita.
    3. Pregunta el nombre y el motivo.
    4. REGLA DE HORARIO DEL DOCTOR (OBLIGATORIO): {horario_personalizado}
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

    st.subheader("💬 Agenda tu cita aquí")
    
    with st.container(border=True):
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
