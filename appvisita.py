import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Auditoría - Caja Arequipa", layout="wide")

st.markdown('<p style="font-size:26px; font-weight: bold; color: #8B0000;">🏢 Unidad de Auditoría Interna</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📂 Base de Datos")
    uploaded_file = st.file_uploader("Carga el Excel (MUESTRA_FINAL)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Cargamos el archivo usando la primera fila como encabezado (header=0)
        df = pd.read_excel(uploaded_file, header=0)
        
        # Identificar columnas
        # Columna D es el índice 3. Buscamos el nombre de esa columna.
        col_dni_name = df.columns[3]  # Nombre en la cabecera de la Columna D
        col_titular_name = df.columns[18] # Columna S
        
        # Limpieza: Asegurar que el DNI sea texto y quitar decimales
        df[col_dni_name] = df[col_dni_name].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

        st.markdown(f"### 🔍 Búsqueda por DNI (Columna: {col_dni_name})")
        dni_input = st.text_input("Ingrese el DNI a buscar:", placeholder="Ej: 41234567").strip()

        if dni_input:
            # Filtramos buscando el valor en la columna identificada como DNI
            resultado = df[df[col_dni_name] == dni_input]
            
            if not resultado.empty:
                fila = resultado.iloc[0]
                nombre = str(fila[col_titular_name])
                
                st.success(f"✅ Cliente encontrado: **{nombre}**")
                
                # Aquí despliegas tus pestañas de auditoría...
                tab1, tab2, tab3 = st.tabs(["📄 PÁGINA 1", "⚠️ PÁGINA 2", "🏠 PÁGINA 3"])
                with tab1:
                    st.text_input("Titular:", value=nombre, disabled=True)
                    st.text_input("DNI:", value=dni_input, disabled=True)
                
            else:
                st.error(f"No se encontró el DNI '{dni_input}' en la columna '{col_dni_name}'.")
                st.info("Verifique que el archivo subido sea la hoja 'MUESTRA_FINAL' correcta.")
                    
    except Exception as e:
        st.error(f"Error al procesar: {e}")
else:
    st.info("Por favor, suba el archivo Excel en la barra lateral.")
