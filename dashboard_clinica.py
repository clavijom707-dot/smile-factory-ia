import streamlit as st
import json
import urllib.request

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Smile Factory - Clínica Dental", 
    page_icon="🦷", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CÓDIGO CSS (Oculta Share/GitHub y deja la flechita) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stToolbar"] {display: none;}
    .stApp {background-color: #f8f9fa;}
    .big-title {color: #0e4d64; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; font-size: 3.5rem; margin-bottom: 0px;}
    .sub-title {color: #6c757d; font-size: 1.2rem; margin-bottom: 20px;}
    .st-emotion-cache-1v0mbdj img {border-radius: 15px;}
    </style>
""", unsafe_allow_html=True)

# --- SEGURIDAD ---
ia_token = st.secrets["DEEPSEEK_TOKEN"]

# --- MEMORIA DE LA APP ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Bienvenido a Smile Factory. Soy Nataly, ¿en qué puedo ayudarle hoy? 🦷"}]

if "horario_actual" not in st.session_state:
    st.session_state.horario_actual = "La agenda está llena en las tardes. SOLO ofrece citas en la MAÑANA (8:00 a 12:00)."

# --- PANEL DE ADMINISTRADOR ---
with st.sidebar:
    st.header("⚙️ Acceso Doctores")
    password = st.text_input("Contraseña:", type="password")
    
    if password == "smile2026":
        st.success("Modo Administrador Activado")
        
        st.write("### 🔗 Compartir Clínica")
        enlace_app = "https://smile-factory-ia-fkq5qvkpcytjtlfnats7yp.streamlit.app"
        st.code(enlace_app, language="text")
        
        st.divider()
        
        opcion = st.radio(
            "Seleccione el horario de atención de hoy:",
            ("Solo Mañanas (8am - 12pm)", "Solo Tardes (2pm - 6pm)", "Mañana y Tarde", "Personalizado...")
        )
        
        if opcion == "Solo Mañanas (8am - 12pm)":
            st.session_state.horario_actual = "La agenda está llena en las tardes. SOLO ofrece citas en la MAÑANA (8:00 a 12:00)."
        elif opcion == "Solo Tardes (2pm - 6pm)":
            st.session_state.horario_actual = "La agenda está llena en las mañanas. SOLO ofrece citas en la TARDE (14:00 a 18:00)."
        elif opcion == "Mañana y Tarde":
            st.session_state.horario_actual = "El doctor atiende en la MAÑANA (8:00 a 12:00) y en la TARDE (14:00 a 18:00). Ofrece ambos horarios al paciente."
        else:
            st.session_state.horario_actual = st.text_area(
                "Escriba la instrucción exacta:", 
                value="Hoy el doctor solo atiende en la tarde de 3 a 5 PM."
            )
            
        st.divider()
        
        if st.button("🗑️ Limpiar Historial de Chat"):
            st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Bienvenido a Smile Factory. Soy Nataly, ¿en qué puedo ayudarle hoy? 🦷"}]
            st.rerun() 

# --- ENCABEZADO ---
st.markdown('<p class="big-title">🦷 Smile Factory</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Tecnología y salud dental en un solo lugar. Agenda tu cita con Nataly, nuestra IA 24/7.</p>', unsafe_allow_html=True)

# --- COLUMNAS ---
col_info, col_chat = st.columns([1, 1], gap="large")

with col_info:
    # Usamos una foto profesional de internet para que no falle. 
    st.image("https://images.unsplash.com/photo-1606811841689-23dfddce3e95?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
    
    st.write("### Bienvenido a la excelencia dental")
    st.write("En **Smile Factory** combinamos la calidez humana con la inteligencia artificial más avanzada. Nuestra recepcionista virtual está disponible las 24 horas.")
    st.markdown("#### Nuestros Servicios")
    st.markdown("- 🦷 **Limpieza Dental**\n- 🪥 **Ortodoncia**\n- 🩺 **Consulta General**\n- ✨ **Blanqueamiento**")

with col_chat:
    # Botón de "Nueva Consulta"
    col_titulo, col_boton = st.columns([2, 1])
    with col_titulo:
        st.subheader("💬 Agenda tu cita aquí")
    with col_boton:
        if st.button("🔄 Nueva Consulta", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Bienvenido a Smile Factory. Soy Nataly, ¿en qué puedo ayudarle hoy? 🦷"}]
            st.rerun()

    system_prompt = f"""
    Eres Nataly, la recepcionista virtual de la clínica dental 'Smile Factory'.
    Tus reglas:
    1. Eres amable, empática, profesional y usas un tono cálido.
    2. Tu objetivo principal es agendar una cita.
    3. Pregunta el nombre y el motivo.
    4. REGLA DE HORARIO DEL DOCTOR (OBLIGATORIO): {st.session_state.horario_actual}
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

    # Caja de chat con altura fija
    with st.container(height=400, border=True):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Escribe aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Nataly está escribiendo..."):
            respuesta = chatear(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
            
        st.rerun()
