import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditoría Caja Arequipa", layout="wide")

st.markdown('<h2 style="color: #8B0000;">🏢 Unidad de Auditoría Interna</h2>', unsafe_allow_html=True)

with st.sidebar:
    uploaded_file = st.file_uploader("Carga el archivo Excel:", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Cargamos sin encabezado para evitar errores de lectura de nombres
        df = pd.read_excel(uploaded_file, header=None)
        
        # 1. Limpiamos la columna D (índice 3) para que sean solo texto puro
        # Usamos .astype(str) y eliminamos cualquier punto decimal o espacio
        df[3] = df[3].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        
        st.write(f"Columnas detectadas: {df.shape[1]}")
        
        dni_input = st.text_input("Ingrese DNI a buscar:").strip()
        
        if dni_input:
            # 2. Convertimos el input también a string crudo
            dni_input = str(dni_input).strip()
            
            # 3. Buscamos la coincidencia exacta en la columna 3
            resultado = df[df[3] == dni_input]
            
            if not resultado.empty:
                st.success("✅ ¡DNI encontrado!")
                fila = resultado.iloc[0]
                
                # Intentamos obtener la columna 18 (S) si existe
                nombre = fila[18] if 18 < df.shape[1] else "Columna S no disponible"
                st.info(f"Nombre en Columna S: **{nombre}**")
                
                st.tabs(["📄 PÁGINA 1", "⚠️ PÁGINA 2", "🏠 PÁGINA 3"])
            else:
                st.error("DNI no encontrado.")
                # MUESTRA LO QUE ESTÁ LEYENDO REALMENTE PARA DEPURAR
                st.write("Primeros 5 registros de la Columna D:")
                st.write(df[3].head(5).tolist())
                
    except Exception as e:
        st.error(f"Error técnico: {e}")
