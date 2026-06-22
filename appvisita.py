import streamlit as st
import pandas as pd
from fpdf import FPDF

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Auditoría Caja Arequipa", layout="centered")

# --- AUTENTICACIÓN ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

def login():
    st.title("🔐 Acceso de Auditor")
    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if user == "auditor" and pwd == "caja2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Credenciales inválidas")

if not st.session_state.logged_in:
    login()
else:
    # --- INTERFAZ PRINCIPAL ---
    st.markdown("<h2 style='color:#8B0000;'>📋 Formato de Visita</h2>", unsafe_allow_html=True)
    
    # Navegación con slider
    paso = st.select_slider("Sección de Auditoría", options=["1. Datos", "2. Riesgos", "3. Campo", "4. Negocio", "5. Cierre"])
    
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}

    # Formulario
    with st.form("main_form"):
        if paso == "1. Datos":
            st.session_state.form_data['titular'] = st.text_input("Titular", value=st.session_state.form_data.get('titular', ''))
            st.session_state.form_data['cuenta'] = st.text_input("Cuenta", value=st.session_state.form_data.get('cuenta', ''))
        elif paso == "2. Riesgos":
            st.session_state.form_data['deuda'] = st.number_input("Deuda Total (S/.)", value=st.session_state.form_data.get('deuda', 0.0))
        elif paso == "3. Campo":
            st.session_state.form_data['direccion'] = st.text_input("Dirección", value=st.session_state.form_data.get('direccion', ''))
        elif paso == "4. Negocio":
            st.session_state.form_data['ventas'] = st.number_input("Ventas (S/.)", value=st.session_state.form_data.get('ventas', 0.0))
        elif paso == "5. Cierre":
            st.session_state.form_data['obs'] = st.text_area("Observaciones", value=st.session_state.form_data.get('obs', ''))
            
        submitted = st.form_submit_button("Guardar sección en memoria")

    # --- GENERACIÓN DE INFORME PDF ---
    if st.button("📥 Generar y Descargar PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="INFORME DE VISITA - AUDITORÍA", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        for k, v in st.session_state.form_data.items():
            pdf.cell(200, 10, txt=f"{k.upper()}: {v}", ln=True)
        
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("Descargar PDF", data=pdf_bytes, file_name="Reporte_Auditoria.pdf", mime="application/pdf")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
