import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Auditoría - Caja Arequipa", layout="wide")

st.markdown('<p style="font-size:26px; font-weight: bold; color: #8B0000;">🏢 Unidad de Auditoría Interna</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📂 Base de Datos")
    uploaded_file = st.file_uploader("Carga el Excel (MUESTRA_FINAL)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Cargar con encabezado en la primera fila
        df = pd.read_excel(uploaded_file, header=0)
        
        # DEFINICIÓN DE COLUMNAS (Índices base 0)
        # Columna D = Índice 3
        # Columna S = Índice 18
        idx_dni = 3
        idx_titular = 18
        idx_cuenta = 12
        idx_analista = 20
        
        # NOMBRE DE LAS COLUMNAS
        col_name_dni = df.columns[idx_dni]
        col_name_titular = df.columns[idx_titular]
        col_name_cuenta = df.columns[idx_cuenta]
        col_name_analista = df.columns[idx_analista]

        # --- LÓGICA DE LIMPIEZA ROBUSTA ---
        # Convertimos toda la columna a texto, quitamos decimales .0 y espacios
        df[col_name_dni] = df[col_name_dni].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

        st.markdown("### 🔍 Inserción de DNI")
        dni_input = st.text_input("Ingrese el DNI a buscar:", placeholder="Ej: 41234567").strip()

        if dni_input:
            # Buscamos comparando cadenas de texto limpias
            resultado = df[df[col_name_dni] == dni_input]
            
            if not resultado.empty:
                fila = resultado.iloc[0]
                nombre = str(fila[col_name_titular])
                cuenta = str(fila[col_name_cuenta])
                analista = str(fila[col_name_analista])
                
                st.success(f"✅ Cliente encontrado: **{nombre}**")
                
                tab1, tab2, tab3 = st.tabs(["📄 PÁGINA 1", "⚠️ PÁGINA 2", "🏠 PÁGINA 3"])
                
                with tab1:
                    st.text_input("Titular:", value=nombre, disabled=True)
                    st.text_input("DNI:", value=dni_input, disabled=True)
                    st.text_input("Cuenta:", value=cuenta)
                    st.text_input("Analista:", value=analista)
                
                with tab2:
                    st.checkbox("Indicio de dolo o fraude")
                    st.checkbox("Evaluaciones deficientes")
                
                with tab3:
                    st.text_area("Comentarios de Visita", placeholder="Escriba los hallazgos...")
                
                if st.button("💾 Consolidar Datos"):
                    st.success("¡Datos guardados!")
            else:
                # Debugging visual para ayudar a encontrar el error si no lo halla
                st.error("No se encontró el DNI. Asegúrese de que el DNI esté en la columna D.")
                with st.expander("Ver lista de DNIs cargados (primeros 5)"):
                    st.write(df[col_name_dni].head(5).tolist())
                    
    except Exception as e:
        st.error(f"Error técnico: {e}")
else:
    st.info("Suba el archivo Excel en la barra lateral.")
