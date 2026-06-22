import streamlit as st

# Configuración de página optimizada para móviles
st.set_page_config(page_title="Auditoría Móvil", layout="centered", initial_sidebar_state="collapsed")

# Estilo para que los campos sean fáciles de tocar en móvil
st.markdown("""
    <style>
    .stTextInput>div>div>input { font-size: 16px !important; }
    .stButton>button { width: 100%; height: 50px; font-weight: bold; }
    div[data-testid="stExpander"] { border: 1px solid #8B0000; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("📱 Auditoría Caja Arequipa")

# Navegación compacta usando Acordeones
with st.expander("📄 1. Datos Generales", expanded=True):
    st.text_input("Titular", placeholder="[tituclie]")
    st.text_input("Cuenta Cliente", placeholder="[cuentacliente]")
    col1, col2 = st.columns(2)
    col1.text_input("Analista Vigente", placeholder="[analistavigente]")
    col2.text_input("Analista Evaluador", placeholder="[analistaevaluador]")
    st.text_input("Importe (S/.)", placeholder="[importe]")

with st.expander("⚠️ 2. Riesgos y Sobreendeudamiento"):
    st.number_input("Deuda Total (S/.)", value=0.0)
    st.text_input("Resultado Neto", placeholder="[resultadoneto]")

with st.expander("🏠 3. Verificación de Campo"):
    st.text_input("Dirección Domicilio", placeholder="[direccion]")
    st.text_area("Comentarios de Visita", placeholder="[comentarios]")

with st.expander("📊 4. Negocio e Ingresos"):
    st.text_input("Actividad Principal", placeholder="[actividadprincipal]")
    col1, col2 = st.columns(2)
    col1.number_input("Ventas (S/.)", value=0.0)
    col2.number_input("Utilidad Neta (S/.)", value=0.0)

with st.expander("👤 5. Aval y Cierre"):
    st.text_input("Nombre del Aval")
    st.text_input("Hecho por", placeholder="[iniau]")
    st.date_input("Fecha de Visita")

# Botón de acción grande para dedos
if st.button("💾 GUARDAR FORMATO DE VISITA"):
    st.success("Información guardada correctamente.")
    st.balloons()
