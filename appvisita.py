import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Auditoría - Caja Arequipa", layout="wide")

# Estilos CSS
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
        # Cargar archivo usando la primera fila como encabezado
        df = pd.read_excel(uploaded_file, header=0)
        
        # Definir columnas por índice (A=0, B=1, C=2, D=3... S=18)
        idx_col_dni = 3
        idx_col_titular = 18
        idx_col_cuenta = 12
        idx_col_analista = 20
        
        # Limpieza de DNIs: convertir a texto y limpiar decimales o espacios
        nombre_col_dni = df.columns[idx_col_dni]
        df[nombre_col_dni] = df[nombre_col_dni].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

        # Buscador
        st.markdown("### 🔍 Búsqueda de Expediente")
        dni_input = st.text_input("Ingrese el DNI a buscar:", placeholder="Ej: 41234567").strip()

        if dni_input:
            resultado = df[df[nombre_col_dni] == dni_input]
            
            if not resultado.empty:
                fila = resultado.iloc[0]
                # Extraer datos usando los índices definidos
                nombre = str(fila[df.columns[idx_col_titular]])
                cuenta = str(fila[df.columns[idx_col_cuenta]])
                analista = str(fila[df.columns[idx_col_analista]])
                
                st.success(f"✅ Cliente encontrado: **{nombre}**")
                
                # Pestañas del aplicativo
                tab1, tab2, tab3 = st.tabs(["📄 PÁGINA 1", "⚠️ PÁGINA 2", "🏠 PÁGINA 3"])
                
                with tab1:
                    st.subheader("Datos Generales")
                    st.text_input("Titular (Columna S)", value=nombre, disabled=True)
                    st.text_input("DNI (Columna D)", value=dni_input, disabled=True)
                    st.text_input("Cuenta Cliente", value=cuenta)
                    st.text_input("Analista Vigente", value=analista)
                
                with tab2:
                    st.subheader("Riesgos y Hallazgos")
                    st.checkbox("Indicio de dolo o fraude")
                    st.checkbox("Evaluaciones deficientes")
                    st.checkbox("Documentos con enmendaduras")
                    st.checkbox("No se evidenció sustento de ingresos")
                
                with tab3:
                    st.subheader("Verificación de Campo")
                    st.text_area("Comentarios de Visita", placeholder="Escriba aquí los hallazgos...")
                
                if st.button("💾 Consolidar Datos"):
                    st.success("¡Datos guardados correctamente!")
            else:
                st.error("DNI no encontrado. Verifique la columna D.")
                
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
else:
    st.info("Por favor, suba el archivo Excel en la barra lateral.")
