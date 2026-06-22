import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditoría - Caja Arequipa", layout="wide")

st.markdown('<p style="font-size:26px; font-weight: bold; color: #8B0000;">🏢 Unidad de Auditoría Interna</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📂 Configuración")
    uploaded_file = st.file_uploader("Carga el Excel (MUESTRA_FINAL)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Cargamos el archivo respetando la fila de encabezados
        df = pd.read_excel(uploaded_file, header=0)
        
        # MOSTRAR INFORMACIÓN DE DEPURACIÓN (Útil para saber qué está pasando)
        st.sidebar.write(f"Columnas detectadas: {len(df.columns)}")
        
        # Columna D (Índice 3) y S (Índice 18)
        # Verificamos si las columnas existen antes de intentar usarlas
        if len(df.columns) > 3:
            col_dni = df.columns[3]
            
            # Limpieza segura del DNI
            df[col_dni] = df[col_dni].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
            
            st.markdown(f"### 🔍 Buscando en columna: {col_dni}")
            dni_input = st.text_input("Ingrese el DNI a buscar:").strip()

            if dni_input:
                resultado = df[df[col_dni] == dni_input]
                
                if not resultado.empty:
                    fila = resultado.iloc[0]
                    # Si el archivo tiene la columna S (índice 18), la usamos
                    nombre = fila[df.columns[18]] if len(df.columns) > 18 else "Columna S no existe"
                    
                    st.success(f"✅ Cliente encontrado: **{nombre}**")
                else:
                    st.error("DNI no encontrado.")
        else:
            st.error("El archivo cargado es demasiado pequeño. ¿Es la hoja 'MUESTRA_FINAL' correcta?")
            
    except Exception as e:
        st.error(f"Error técnico: {e}")
