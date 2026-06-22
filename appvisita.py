import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditoría Caja Arequipa", layout="wide")

st.markdown('<p style="font-size:26px; font-weight: bold; color: #8B0000;">🏢 Unidad de Auditoría Interna</p>', unsafe_allow_html=True)

with st.sidebar:
    uploaded_file = st.file_uploader("Carga el Excel (MUESTRA_FINAL)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # 1. Cargar con encabezado
        df = pd.read_excel(uploaded_file, header=0)
        
        # 2. LIMPIEZA AUTOMÁTICA: 
        # Convertimos todos los nombres de columnas a mayúsculas para que no haya error de tipeo
        df.columns = df.columns.str.upper().str.strip()
        
        # 3. BUSCAR NOMBRES DE COLUMNAS
        # Aquí escribes los nombres exactos que tienen tus cabeceras en el Excel
        # Si tu columna se llama "PENDOC" o "DNI", cámbialo abajo:
        col_dni = "PENDOC" 
        col_titular = "TITULAR" # Cambia esto por el nombre exacto de la columna del nombre
        
        if col_dni not in df.columns:
            st.error(f"❌ No encuentro la columna '{col_dni}'. Columnas disponibles: {list(df.columns)}")
        else:
            # Limpieza del DNI
            df[col_dni] = df[col_dni].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
            
            dni_input = st.text_input("Ingrese el DNI a buscar:").strip()
            
            if dni_input:
                resultado = df[df[col_dni] == dni_input]
                
                if not resultado.empty:
                    fila = resultado.iloc[0]
                    # Extraer titular si la columna existe
                    nombre = fila[col_titular] if col_titular in df.columns else "No encontrada"
                    
                    st.success(f"✅ Cliente: {nombre}")
                    
                    # Pestañas
                    tab1, tab2, tab3 = st.tabs(["📄 PÁGINA 1", "⚠️ PÁGINA 2", "🏠 PÁGINA 3"])
                    with tab1:
                        st.text_input("Titular:", value=str(nombre), disabled=True)
                        st.text_input("DNI:", value=dni_input, disabled=True)
                else:
                    st.warning("DNI no encontrado.")
            
    except Exception as e:
        st.error(f"Error: {e}")
