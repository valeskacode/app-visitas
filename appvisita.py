import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Auditoría - Caja Arequipa", layout="wide")

st.markdown('<h2 style="color: #8B0000;">🏢 Unidad de Auditoría: Recolección de Datos</h2>', unsafe_allow_html=True)

with st.sidebar:
    uploaded_file = st.file_uploader("Carga el Excel (MUESTRA_FINAL)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Cargamos el archivo sin encabezado fijo
        df = pd.read_excel(uploaded_file, header=None)
        
        # Limpieza de la columna D (índice 3)
        df[3] = df[3].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        
        dni_input = st.text_input("Ingrese DNI para habilitar ventanas:").strip()
        
        if dni_input:
            resultado = df[df[3] == dni_input]
            
            if not resultado.empty:
                fila = resultado.iloc[0]
                
                # Datos básicos para las ventanas
                nombre_cliente = fila[18] if 18 < df.shape[1] else "No disponible"
                
                st.success(f"✅ Cliente: {nombre_cliente}")
                
                # --- VISUALIZACIÓN DE LAS VENTANAS DE RECOLECCIÓN ---
                tab1, tab2, tab3 = st.tabs(["📄 PÁGINA 1: Datos", "⚠️ PÁGINA 2: Riesgos", "🏠 PÁGINA 3: Campo"])
                
                with tab1:
                    st.subheader("Datos Generales del Crédito")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_input("Titular", value=str(nombre_cliente), disabled=True)
                        st.text_input("Cuenta")
                    with col2:
                        st.text_input("Analista Vigente")
                        st.text_input("Importe")
                
                with tab2:
                    st.subheader("Sobreendeudamiento y Riesgos")
                    st.number_input("Deuda Directa (S/.)", min_value=0.0)
                    st.number_input("Deuda Total (S/.)", min_value=0.0)
                    st.multiselect("Criterios de Auditoría", 
                                   ["Indicio de dolo", "Evaluación deficiente", "Documentos con enmendaduras", "Sin sustento de ingresos"])
                
                with tab3:
                    st.subheader("Dirección y Verificación")
                    st.text_input("Domicilio Real")
                    st.text_area("Comentarios de Auditoría")
                    if st.button("Guardar Datos de Visita"):
                        st.toast("Datos almacenados en el sistema")
            else:
                st.error("DNI no encontrado en la columna D.")
                
    except Exception as e:
        st.error(f"Error técnico: {e}")
