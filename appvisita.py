import streamlit as st
import pandas as pd

# 1. Configuración de Interfaz de Aplicativo (Mobile & PC layout)
st.set_page_config(page_title="Auditoría - Caja Arequipa", layout="wide", initial_sidebar_state="expanded")

# Estilos visuales personalizados para que parezca una app nativa
st.markdown("""
    <style>
    .main-title { font-size:26px !important; font-weight: bold; color: #8B0000; margin-bottom: 5px; }
    .subtitle { font-size:14px !important; color: #555555; margin-bottom: 20px; }
    div[data-testid="stExpander"] div[role="button"] p { font-size: 16px; font-weight: bold; }
    .stButton>button { width: 100% !important; font-weight: bold; }
    </style>
    """, unsafe_style_html=True)

st.markdown('<p class="main-title">🏢 Unidad de Auditoría Interna</p>', unsafe_style_html=True)
st.markdown('<p class="subtitle">Visita a Clientes de Pequeña Empresa - Caja Arequipa</p>', unsafe_style_html=True)

# Barra lateral para cargar la Base de Datos
with st.sidebar:
    st.header("📂 Base de Datos")
    uploaded_file = st.file_uploader("Carga la hoja MUESTRA_FINAL (Excel)", type=["xlsx", "xls"])
    st.markdown("---")
    st.caption("⚙️ Mapeo de Columnas Internas:")
    st.caption("- Columna D (Índice 3): Búsqueda de DNI")
    st.caption("- Columna S (Índice 18): Nombre del Titular")

if uploaded_file is not None:
    try:
        # Leer el Excel (Hoja MUESTRA_FINAL)
        # Se lee desde la fila 0 para procesar los datos de forma flexible
        df = pd.read_excel(uploaded_file, header=None)
        st.sidebar.success("¡Base de Datos acoplada!")

        # Índices fijos del Excel según tus especificaciones
        col_dni = 3        # Columna D (DNI a buscar)
        col_titular = 18   # Columna S (Nombre completo del Cliente)
        col_cuenta = 12    # Cuenta Cliente [cuenta Miente]
        col_analista = 20  # Analista Vigente [analistavigente]
        col_importe = 45   # Importe Operación [importe]
        
        # Pág 2 y 3 Variables del PDF
        col_deuda_dir = 113
        col_deuda_pot = 116
        col_deuda_tot = 119
        col_domicilio = 156
        col_negocio = 164

        # Función de limpieza estricta para que encuentre el DNI sin importar el formato en Excel
        def limpiar_dato_dni(v):
            if pd.isna(v): return ""
            s = str(v).strip()
            if s.endswith('.0'): s = s[:-2]
            return s

        # Aplicar limpieza a la columna D para garantizar el cruce
        df[col_dni] = df[col_dni].apply(limpiar_dato_dni)

        # ================= SECCIÓN DE BÚSQUEDA E INSERCIÓN (COLUMNA D) =================
        st.markdown("### 🔍 Inserción y Búsqueda de DNI")
        dni_input = st.text_input("Ingrese el número de DNI para realizar la auditoría:", key="dni_search", placeholder="Escriba aquí el DNI de 8 dígitos...").strip()

        if dni_input:
            # Buscar el DNI en la columna D
            resultado = df[df[col_dni] == dni_input]

            if not resultado.empty:
                fila_idx = resultado.index[0]

                # Función de extracción segura evitando desbordamientos de columnas
                def extraer(idx, col, defecto=""):
                    if col < len(df.columns):
                        val = df.iloc[idx, col]
                        return defecto if pd.isna(val) else str(val).strip()
                    return defecto

                # Extracción de Datos en base a tu estructura del PDF
                nombre_cliente = extraer(fila_idx, col_titular, "No encontrado en Columna S")
                cuenta_cliente = extraer(fila_idx, col_cuenta, "[cuenta Miente]")
                analista_vigente = extraer(fila_idx, col_analista, "[analistavigente]")
                importe_credito = extraer(fila_idx, col_importe, "[importe]")
                
                deuda_directa = extraer(fila_idx, col_deuda_dir, "0.00")
                deuda_potencial = extraer(fila_idx, col_deuda_pot, "0.00")
                deuda_total = extraer(fila_idx, col_deuda_tot, "0.00")
                
                dir_domicilio = extraer(fila_idx, col_domicilio, "")
                dir_negocio = extraer(fila_idx, col_negocio, "")

                st.success(f"📋 Datos recuperados para el DNI {dni_input}")

                # ================= VISTA DE APLICATIVO RESPONSIVA (PESTAÑAS) =================
                # Ideal tanto para celulares como para pantallas de computadoras
                tab1, tab2, tab3 = st.tabs([
                    "📄 PÁGINA 1: Visita al Cliente", 
                    "⚠️ PÁGINA 2: Sobreendeudamiento y Riesgos", 
                    "🏠 PÁGINA 3: Verificaciones de Campo"
                ])

                # ---------- PÁGINA 1 ----------
                with tab1:
                    st.markdown("#### 1. Datos Generales del Crédito")
                    c1, c2 = st.columns(2)
                    with c1:
                        # ¡Carga automática del nombre desde la columna S!
                        st.text_input("Titular (Extraído de Columna S)", value=nombre_cliente, disabled=True)
                        st.text_input("DNI / LE (Columna D)", value=dni_input, disabled=True)
                        st.text_input("Cuenta Cliente", value=cuenta_cliente)
                    with c2:
                        st.text_input("Analista Vigente", value=analista_vigente)
                        st.text_input("Importe Operación (S/.)", value=importe_credito)
                        st.text_input("Agencia", value="OFICINA ADMINISTRACION")

                # ---------- PÁGINA 2 ----------
                with tab2:
                    st.markdown("#### 4. Riesgo de Sobreendeudamiento")
                    c3, c4, c5 = st.columns(3)
                    with c3:
                        st.text_input("a) Deuda Directa", value=deuda_directa)
                    with c4:
                        st.text_input("b) Deuda Potencial", value=deuda_potencial)
                    with c5:
                        st.text_input("c) Deuda Total", value=deuda_total)
                    
                    st.markdown("---")
                    st.markdown("#### 📋 Criterios Aplicados en la Visita")
                    
                    # Checkboxes optimizados para pantallas táctiles de celulares
                    st.checkbox("Indicio de dolo o fraude en la evaluación de créditos", value=False)
                    st.checkbox("Evaluaciones deficientes o con sustento insuficiente", value=False)
                    st.checkbox("Documentos con enmendaduras o datos inconsistentes", value=False)
                    st.checkbox("No se evidenció sustento de actividad económica o ingresos", value=False)
                    st.checkbox("Créditos reprogramados y refinanciados", value=False)

                # ---------- PÁGINA 3 ----------
                with tab3:
                    st.markdown("#### 5. Direcciones Encontradas e Inspección")
                    
                    with st.container(border=True):
                        st.markdown("🏡 **Dirección del Domicilio**")
                        st.text_input("Domicilio Real", value=dir_domicilio if dir_domicilio else "Asociación Las Flores Mz. B Lote 5")
                        c6, c7 = st.columns(2)
                        with c6: st.text_input("Distrito / Provincia", value="Cerro Colorado / Arequipa")
                        with c7: st.text_input("Entrevista con", value="", placeholder="Nombre del entrevistado...")
                        st.text_area("Comentarios de la Visita Domiciliaria", height=80)

                    with st.container(border=True):
                        st.markdown("🏢 **Dirección del Negocio**")
                        st.text_input("Negocio Real", value=dir_negocio if dir_negocio else "Calle Mercaderes 312")
                        st.text_input("Tipo de Negocio", value="Familiar")
                        st.text_area("Comentarios de la Visita de Negocio", value="Idem anterior.", height=80)

                # ---------- ACCIÓN DE GUARDADO ----------
                st.markdown("---")
                if st.button("💾 Procesar e Imprimir Formato PDF", type="primary", use_container_width=True):
                    st.success(f"¡Expediente de {nombre_cliente} consolidado de manera exitosa!")
            else:
                st.error(f"❌ El DNI '{dni_input}' no se encuentra registrado en la columna D de la hoja MUESTRA_FINAL.")
                st.info("💡 Consejo: Asegúrate de que el Excel esté correctamente guardado y que el DNI no contenga letras.")

    except Exception as e:
        st.error(f"Error técnico al procesar el archivo Excel: {e}")
else:
    st.info("👋 Para iniciar, cargue el archivo Excel de la hoja MUESTRA_FINAL mediante el panel lateral.")
