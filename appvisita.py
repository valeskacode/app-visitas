import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditoría Caja Arequipa", layout="wide")

st.markdown('<p style="font-size:26px; font-weight: bold; color: #8B0000;">🏢 Unidad de Auditoría Interna</p>', unsafe_allow_html=True)

with st.sidebar:
    uploaded_file = st.file_uploader("Carga el Excel (MUESTRA_FINAL)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # header=None: Esto le dice a Pandas que NO busque encabezados
        # Así, la Columna A es la 0, B la 1, C la 2, D la 3, S la 18.
        df = pd.read_excel(uploaded_file, header=None)
        
        # LIMPIEZA: Convertimos la columna D (índice 3) a texto limpio
        df[3] = df[3].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        
        st.markdown("### 🔍 Búsqueda de Expediente")
        dni_input = st.text_input("Ingrese el DNI (Columna D):").strip()
        
        if dni_input:
            # Filtramos por el índice 3 (Columna D)
            resultado = df[df[3] == dni_input]
            
            if not resultado.empty:
                fila = resultado.iloc[0]
                # Columna S es el índice 18
                nombre = str(fila[18]) 
                
                st.success(f"✅ Cliente encontrado: **{nombre}**")
                
                # Visualización de pestañas
                tab1, tab2, tab3 = st.tabs(["📄 PÁGINA 1", "⚠️ PÁGINA 2", "🏠 PÁGINA 3"])
                with tab1:
                    st.text_input("Titular (Columna S):", value=nombre, disabled=True)
                    st.text_input("DNI (Columna D):", value=dni_input, disabled=True)
            else:
                st.error("DNI no encontrado en la Columna D.")
                st.info(f"DNI buscado: {dni_input}. Asegúrese de que el DNI esté en la columna D.")
                    
    except Exception as e:
        st.error(f"Error al procesar: {e}")
