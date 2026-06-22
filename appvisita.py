import streamlit as st
import pandas as pd

# Configuración visual
st.set_page_config(page_title="Formato de Visita - Auditoría", layout="wide")

st.markdown("""
    <style>
    .header-box { background-color: #8B0000; padding: 15px; border-radius: 10px; color: white; text-align: center; }
    </style>
    <div class="header-box"><h1>📋 FORMATO DE VISITA A CLIENTES - AUDITORÍA INTERNA</h1></div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📂 Carga de Base de Datos")
    uploaded_file = st.file_uploader("Subir MUESTRA_FINAL", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Carga sin encabezado fijo para evitar errores de nombres
    df = pd.read_excel(uploaded_file, header=None)
    
    # Limpieza: Columna D (Índice 3)
    df[3] = df[3].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    
    dni_input = st.text_input("🔍 Ingrese DNI del Cliente (Columna D):").strip()
    
    if dni_input:
        resultado = df[df[3] == dni_input]
        if not resultado.empty:
            fila = resultado.iloc[0]
            st.success("✅ Cliente ubicado en la base de datos.")
            
            # --- ESTRUCTURA DE VENTANAS (REPLICANDO EL FORMATO) ---
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
                    st.text_input("Titular", value=str(fila[18]))
                    st.text_input("Cuenta Cliente", value=str(fila[12]))
                with c2:
                    st.text_input("Analista Vigente", value=str(fila[20]))
                    st.text_input("Importe Operación")
            
            with tab2:
                st.subheader("Sobreendeudamiento (Sección 2)")
                col_r1, col_r2, col_r3 = st.columns(3)
                col_r1.number_input("Deuda Directa", step=0.01)
                col_r2.number_input("Deuda Potencial", step=0.01)
                col_r3.number_input("Deuda Total", step=0.01)
                st.multiselect("Hallazgos de Auditoría:", 
                               ["Dolo o fraude", "Evaluación deficiente", "Enmendaduras", "Falta sustento ingresos"])
                
            with tab3:
                st.subheader("Verificación Domicilio y Negocio")
                st.text_input("Dirección del Domicilio")
                st.text_area("Comentarios de Visita Domiciliaria")
                st.text_input("Dirección del Negocio")
                st.text_area("Comentarios de Visita de Negocio")
                
            with tab4:
                st.subheader("Estados Financieros (Sección 4)")
                col_a1, col_a2 = st.columns(2)
                col_a1.number_input("Ventas Mensuales (S/.)")
                col_a2.number_input("Utilidad Neta (S/.)")
                
            with tab5:
                st.subheader("Aval y Cierre (Sección 5)")
                st.text_input("Nombre del Aval")
                st.text_area("Observaciones Finales")
                if st.button("💾 GUARDAR FORMATO Y CERRAR"):
                    st.success("Formato consolidado exitosamente.")
        else:
            st.error("DNI no encontrado.")
else:
    st.info("👈 Por favor, cargue el archivo Excel en la barra lateral para iniciar.")
