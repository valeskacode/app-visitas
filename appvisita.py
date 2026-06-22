import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditoría Caja Arequipa", layout="wide")

st.markdown('<h2 style="color: #8B0000;">🔍 Herramienta de Auditoría: Búsqueda de Clientes</h2>', unsafe_allow_html=True)

with st.sidebar:
    uploaded_file = st.file_uploader("Carga el archivo Excel:", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Cargamos el archivo sin encabezado fijo para ver qué hay realmente
        df = pd.read_excel(uploaded_file, header=None)
        
        st.write(f"📊 **Archivo cargado con éxito.**")
        st.write(f"Total de columnas detectadas: {df.shape[1]}")
        
        # --- PASO 1: LOCALIZAR EL DNI ---
        # Si el DNI está en la Columna D, es el índice 3
        # Si tienes error de 'index out of bounds', el número aquí debe ser menor a df.shape[1]
        idx_dni = 3 
        
        if idx_dni < df.shape[1]:
            # Convertimos a string y limpiamos
            df[idx_dni] = df[idx_dni].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
            
            dni_input = st.text_input("Ingrese el DNI a buscar (debe estar en la columna D):").strip()
            
            if dni_input:
                resultado = df[df[idx_dni] == dni_input]
                
                if not resultado.empty:
                    st.success("✅ ¡DNI encontrado!")
                    fila = resultado.iloc[0]
                    
                    # --- PASO 2: LOCALIZAR EL NOMBRE ---
                    # Vamos a intentar buscar el nombre en la columna S (índice 18)
                    # Si no llega a 18, buscaremos la columna más lejana disponible
                    idx_nombre = 18 if 18 < df.shape[1] else df.shape[1] - 1
                    nombre = fila[idx_nombre]
                    
                    st.info(f"Nombre encontrado en columna índice {idx_nombre}: **{nombre}**")
                    
                    # Pestañas de auditoría
                    tab1, tab2, tab3 = st.tabs(["📄 PÁGINA 1", "⚠️ PÁGINA 2", "🏠 PÁGINA 3"])
                    with tab1:
                        st.write(f"Titular: {nombre}")
                        st.write(f"DNI: {dni_input}")
                else:
                    st.error("DNI no encontrado. Intenta verificar si el DNI tiene espacios.")
        else:
            st.error(f"El archivo solo tiene {df.shape[1]} columnas. La columna D (índice 3) no existe.")
            
    except Exception as e:
        st.error(f"Error técnico: {e}")
