import streamlit as st
import json
import urllib.request

# --- SEGURIDAD: Lee el token desde la bóveda ---
ia_token = st.secrets["DEEPSEEK_TOKEN"]

st.set_page_config(page_title="Smile Factory - IA", page_icon="🦷", layout="wide")

st.title("🦷 Panel de Control - Smile Factory")
st.subheader("Bienvenido al centro de operaciones de tu Recepcionista IA.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Citas Agendadas (IA)", "12", "+3 hoy")
col2.metric("Mensajes Contestados", "48", "100% automático")
col3.metric("Tiempo Ahorrado", "4.5 horas", "vs ayer")
col4.metric("Ingresos Estimados", "$600", "+$150")

st.divider()

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
st.subheader("📱 Chat en Vivo con Nataly (Modo Prueba)")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Bienvenido a Smile Factory. Soy Nataly, ¿en qué puedo ayudarle hoy? 🦷"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escriba aquí como si fuera un paciente..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Nataly está escribiendo..."):
        respuesta = chatear(st.session_state.messages)
        st.chat_message("assistant").markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
