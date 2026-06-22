import streamlit as st
import pandas as pd

# 1. Configuración de pantalla
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

# 2. Barra lateral
with st.sidebar:
    st.header("📂 Configuración")
    uploaded_file = st.file_uploader("Carga la hoja MUESTRA_FINAL (Excel)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Cargar datos
        df = pd.read_excel(uploaded_file, header=None)
        
        # Índices de columnas (A=0, B=1, C=2, D=3... S=18)
        col_dni = 3
        col_titular = 18
        
        # Limpieza de DNI
        def limpiar_dni(v):
            s = str(v).strip()
            return s[:-2] if s.endswith('.0') else s
        
        df[col_dni] = df[col_dni].apply(limpiar_dni)

        # 3. Buscador
        st.markdown("### 🔍 Inserción de DNI")
        dni_input = st.text_input("Ingrese DNI para buscar:", placeholder="Ej: 41234567").strip()

        if dni_input:
            resultado = df[df[col_dni] == dni_input]
            
            if not resultado.empty:
                fila_idx = resultado.index[0]
                # Extraer nombre de la Columna S (18)
                nombre = str(df.iloc[fila_idx, col_titular])
                
                st.success(f"✅ Cliente encontrado: **{nombre}**")
                
                # Pestañas del PDF
                tab1, tab2, tab3 = st.tabs(["📄 PÁGINA 1", "⚠️ PÁGINA 2", "🏠 PÁGINA 3"])
                
                with tab1:
                    st.subheader("Datos Generales")
                    st.text_input("Titular (Columna S)", value=nombre, disabled=True)
                    st.text_input("DNI (Columna D)", value=dni_input, disabled=True)
                    st.text_input("Cuenta Cliente", value=str(df.iloc[fila_idx, 12]))
                    st.text_input("Analista Vigente", value=str(df.iloc[fila_idx, 20]))
                
                with tab2:
                    st.subheader("Riesgos y Criterios")
                    st.write("Seleccione observaciones:")
                    st.checkbox("Indicio de dolo o fraude")
                    st.checkbox("Evaluaciones deficientes")
                    st.checkbox("Documentos con enmendaduras")
                    st.checkbox("No se evidenció sustento de ingresos")
                
                with tab3:
                    st.subheader("Verificación de Campo")
                    st.text_area("Dirección del Domicilio", value="Asociación Las Flores Mz. B Lote 5")
                    st.text_area("Comentarios de Visita", placeholder="Escriba aquí los hallazgos...")
                
                if st.button("💾 Consolidar Datos"):
                    st.success("Informe procesado correctamente.")
            else:
                st.error("DNI no encontrado en la base de datos.")
                
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("Suba el archivo MUESTRA_FINAL en la barra lateral para empezar.")
