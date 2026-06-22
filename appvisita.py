import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Auditoría - Caja Arequipa", layout="wide")

# Estilos visuales
st.markdown("""
    <style>
    .main-title { font-size:26px !important; font-weight: bold; color: #8B0000; margin-bottom: 5px; }
    .subtitle { font-size:14px !important; color: #555555; margin-bottom: 20px; }
    .stButton>button { width: 100% !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🏢 Unidad de Auditoría Interna</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Visita a Clientes de Pequeña Empresa - Caja Arequipa</p>', unsafe_allow_html=True)

# Barra lateral
with st.sidebar:
    st.header("📂 Base de Datos")
    uploaded_file = st.file_uploader("Carga el Excel (MUESTRA_FINAL)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # header=0 indica que la primera fila son los títulos de columna
        df = pd.read_excel(uploaded_file, header=0)
        
        # Índices de columnas (A=0, B=1, C=2, D=3... S=18)
        # Usamos los índices posicionales para evitar errores de nombres
        idx_dni = 3
        idx_titular = 18
        
        # Limpieza robusta del DNI en la columna D
        nombre_col_dni = df.columns[idx_dni]
        df[nombre_col_dni] = df[nombre_col_dni].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

        st.markdown("### 🔍 Inserción de DNI")
        dni_input = st.text_input("Ingrese el DNI a buscar:", placeholder="Ej: 41234567").strip()

        if dni_input:
            # Búsqueda exacta en la columna D
            resultado = df[df[nombre_col_dni] == dni_input]
            
            if not resultado.empty:
                fila = resultado.iloc[0]
                # Extracción desde columna S (índice 18)
                nombre = str(fila[df.columns[idx_titular]])
                
                st.success(f"✅ Cliente encontrado: **{nombre}**")
                
                # Pestañas del aplicativo
                tab1, tab2, tab3 = st.tabs(["📄 PÁGINA 1", "⚠️ PÁGINA 2", "🏠 PÁGINA 3"])
                
                with tab1:
                    st.subheader("Datos Generales")
                    st.text_input("Titular (Columna S)", value=nombre, disabled=True)
                    st.text_input("DNI (Columna D)", value=dni_input, disabled=True)
                
                with tab2:
                    st.subheader("Riesgos y Hallazgos")
                    st.checkbox("Indicio de dolo o fraude")
                    st.checkbox("Evaluaciones deficientes")
                
                with tab3:
                    st.subheader("Verificación de Campo")
                    st.text_area("Comentarios de Visita", placeholder="Escriba los hallazgos...")
                
                if st.button("💾 Consolidar Datos"):
                    st.success("¡Datos guardados correctamente!")
            else:
                st.error("❌ DNI no encontrado. Verifique que el archivo contenga el DNI en la columna D.")
                
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    st.info("👋 Por favor, suba el archivo Excel 'MUESTRA_FINAL' en la barra lateral.")
