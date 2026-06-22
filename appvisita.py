import streamlit as st
import pandas as pd
from io import BytesIO

# Configuración
st.set_page_config(page_title="Auditoría - Caja Arequipa", layout="wide")
st.markdown('<div style="background-color: #8B0000; padding: 15px; border-radius: 10px; color: white; text-align: center;"><h1>📋 FORMATO DE VISITA - UNIDAD DE AUDITORÍA INTERNA</h1></div>', unsafe_allow_html=True)

# Lógica de carga
with st.sidebar:
    uploaded_file = st.file_uploader("Cargar Base (MUESTRA_FINAL)", type=["xlsx", "xls"])

df = None
if uploaded_file:
    df = pd.read_excel(uploaded_file, header=None)
    df[3] = df[3].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

# Entrada de datos
dni_input = st.text_input("🔍 Ingrese DNI (opcional para autocompletar):").strip()
datos = None
if dni_input and df is not None:
    res = df[df[3] == dni_input]
    if not res.empty:
        datos = res.iloc[0]
        st.success("✅ Datos recuperados.")

# Pestañas del Formato
t1, t2, t3, t4, t5 = st.tabs(["📄 Datos Grales", "⚠️ Riesgos", "🏠 Campo", "📊 Ingresos", "💾 Guardar"])

with t1:
    col1, col2 = st.columns(2)
    titular = col1.text_input("Titular", value=str(datos[18]) if datos is not None else "")
    cuenta = col2.text_input("Cuenta", value=str(datos[12]) if datos is not None else "")
    analista = col1.text_input("Analista", value=str(datos[20]) if datos is not None else "")

with t2:
    deuda = st.number_input("Deuda Total", step=0.01)
    hallazgos = st.multiselect("Criterios:", ["Dolo", "Deficiente", "Enmendaduras"])

with t3:
    dir_dom = st.text_input("Dirección Domicilio")
    com_dom = st.text_area("Comentarios Visita")

with t4:
    ventas = st.number_input("Ventas Mensuales")
    utilidad = st.number_input("Utilidad Neta")

with t5:
    st.subheader("Finalizar Auditoría")
    if st.button("Generar Reporte Excel"):
        # Crear estructura de reporte
        reporte = pd.DataFrame({
            "Campo": ["Titular", "Cuenta", "Deuda", "Ventas"],
            "Valor": [titular, cuenta, deuda, ventas]
        })
        
        # Guardar en memoria
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            reporte.to_excel(writer, index=False)
        
        st.download_button(
            label="⬇️ Descargar Reporte en Excel",
            data=buffer.getvalue(),
            file_name="reporte_auditoria.xlsx",
            mime="application/vnd.ms-excel"
        )
        st.success("¡Listo para descargar!")
