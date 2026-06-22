import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Formato de Visita - Auditoría", layout="wide")

# Estilos CSS para el look & feel del formato
st.markdown("""
    <style>
    .header-box { background-color: #8B0000; padding: 15px; border-radius: 10px; color: white; text-align: center; }
    .stTab { font-weight: bold; }
    </style>
    <div class="header-box"><h1>📋 FORMATO DE VISITA A CLIENTES - AUDITORÍA INTERNA</h1></div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📂 Base de Datos")
    uploaded_file = st.file_uploader("Cargar Excel (MUESTRA_FINAL)", type=["xlsx", "xls"])

# --- LÓGICA DE DATOS ---
df = None
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, header=None)
        df[3] = df[3].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    except Exception as e:
        st.error(f"Error cargando Excel: {e}")

# --- ENTRADA DE DNI ---
dni_input = st.text_input("🔍 Ingrese DNI (para intentar recuperar datos) o deje vacío para llenar manualmente:")

# --- INTERFAZ COMPLETA (SIEMPRE VISIBLE) ---
# Intentamos recuperar datos si el DNI existe
datos_encontrados = None
if dni_input and df is not None:
    resultado = df[df[3] == dni_input]
    if not resultado.empty:
        datos_encontrados = resultado.iloc[0]
        st.success("✅ Datos recuperados de la Base de Datos.")
    else:
        st.warning("⚠️ DNI no encontrado. Llenado manual habilitado.")

# --- VENTANAS DE RECOLECCIÓN (SECCIONES PSD) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 1. DATOS GENERALES", 
    "⚠️ 2. RIESGOS", 
    "🏠 3. CAMPO", 
    "📊 4. INGRESOS", 
    "👤 5. AVAL/CIERRE"
])

with tab1:
    st.subheader("Datos Generales y Crédito")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Titular", value=str(datos_encontrados[18]) if datos_encontrados is not None else "")
        st.text_input("Cuenta Cliente", value=str(datos_encontrados[12]) if datos_encontrados is not None else "")
    with c2:
        st.text_input("Analista Vigente", value=str(datos_encontrados[20]) if datos_encontrados is not None else "")
        st.text_input("Importe Operación")

with tab2:
    st.subheader("Sobreendeudamiento")
    col_r1, col_r2, col_r3 = st.columns(3)
    col_r1.number_input("Deuda Directa", step=0.01)
    col_r2.number_input("Deuda Potencial", step=0.01)
    col_r3.number_input("Deuda Total", step=0.01)
    st.multiselect("Criterios de Auditoría:", ["Dolo o fraude", "Evaluación deficiente", "Enmendaduras", "Falta sustento ingresos"])

with tab3:
    st.subheader("Verificación Domicilio y Negocio")
    st.text_input("Dirección del Domicilio")
    st.text_area("Comentarios de Visita Domiciliaria")
    st.text_input("Dirección del Negocio")
    st.text_area("Comentarios de Visita de Negocio")

with tab4:
    st.subheader("Estados Financieros")
    col_a1, col_a2 = st.columns(2)
    col_a1.number_input("Ventas Mensuales (S/.)")
    col_a2.number_input("Utilidad Neta (S/.)")

with tab5:
    st.subheader("Aval y Cierre")
    st.text_input("Nombre del Aval")
    st.text_area("Observaciones Finales")
    if st.button("💾 GUARDAR FORMATO COMPLETO"):
        st.success("Formato guardado satisfactoriamente.")
