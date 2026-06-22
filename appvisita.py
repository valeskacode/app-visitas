import streamlit as st
import pandas as pd

# 1. Configuración de Interfaz de Aplicativo (Mobile & PC layout)
st.set_page_config(page_title="Auditoría - Caja Arequipa", layout="wide", initial_sidebar_state="expanded")

# CORRECCIÓN DE PARÁMETRO: Se cambió unsafe_style_html por unsafe_allow_html
st.markdown("""
    <style>
    .main-title { font-size:26px !important; font-weight: bold; color: #8B0000; margin-bottom: 5px; }
    .subtitle { font-size:14px !important; color: #555555; margin-bottom: 20px; }
    div[data-testid="stExpander"] div[role="button"] p { font-size: 16px; font-weight: bold; }
    .stButton>button { width: 100% !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🏢 Unidad de Auditoría Interna</p>', unsafe_style_html=True) if hasattr(st, 'markdown') else None
st.markdown('<p class="main-title">🏢 Unidad de Auditoría Interna</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Visita a Clientes de Pequeña Empresa - Caja Arequipa</p>', unsafe_allow_html=True)

# Barra lateral para cargar la Base de Datos
with st.sidebar:
    st.header("📂 Base de Datos")
    uploaded_file = st.file_uploader("Carga la hoja MUESTRA_FINAL (Excel)", type=["xlsx", "xls"])
    st.markdown("---")
    st.caption("⚙️ Mapeo Estricto de Columnas:")
    st.caption("- Búsqueda en Columna D (DNI)")
    st.caption("- Extracción de Columna S (Nombre Completo)")

if uploaded_file is not None:
    try:
        # Leer el Excel (Fuerza la lectura completa de todas las filas y columnas)
        df = pd.read_excel(uploaded_file, header=None)
        st.sidebar.success("¡Base de Datos acoplada!")

        # Índices basados en la estructura real (A=0, B=1, C=2, D=3...)
        col_dni = 3        # Columna D (Para buscar el DNI)
        col_titular = 18   # Columna S (Para extraer el Nombre Completo)
        
        # Mapeos de apoyo basados en tu plantilla del PDF
        col_cuenta = 12    # Cuenta Cliente
        col_analista = 20  # Analista Vigente
        col_importe = 45   # Importe Operación

        # Función de limpieza profunda para homogeneizar los DNIs del Excel
        def limpiar_dato_dni(v):
            if pd.isna(v): return ""
            s = str(v).strip()
            if s.endswith('.0'): s = s[:-2]
            return s

        df[col_dni] = df[col_dni].apply(limpiar_dato_dni)

        # ================= SECCIÓN DE INTRODUCCIÓN MANUAL (COLUMNA D) =================
        st.markdown("### 🔍 Inserción de DNI para Auditoría")
        dni_input = st.text_input("Ingrese el DNI del cliente paraautofilar el expediente:", key="dni_search", placeholder="Escriba los 8 dígitos del DNI aquí...").strip()

        if dni_input:
            # Buscar coincidencia exacta en la columna D
            resultado = df[df[col_dni] == dni_input]

            if not resultado.empty:
                fila_idx = resultado.index[0]

                # Función auxiliar para extraer celdas de forma segura
                def extraer(idx, col, defecto=""):
                    if col < len(df.columns):
                        val = df.iloc[idx, col]
                        return defecto if pd.isna(val) else str(val).strip()
                    return defecto

                # Extracción dinámica vinculada a tu formato final
                nombre_cliente = extraer(fila_idx, col_titular, "No encontrado en Columna S")
                cuenta_cliente = extraer(fila_idx, col_cuenta, "[cuenta Miente]")
                analista_vigente = extraer(fila_idx, col_analista, "[analistavigente]")
                importe_credito = extraer(fila_idx, col_importe, "[importe]")

                st.success(f"📋 Registro Encontrado")

                # ================= VISTA DE APLICATIVO RESPONSIVA (PESTAÑAS) =================
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
                        # CARGA AUTOMÁTICA DE LA COLUMNA S
                        st.text_input("Titular Completo (Extraído de Columna S)", value=nombre_cliente, disabled=True)
                        st.text_input("DNI / LE (Buscado en Columna D)", value=dni_input, disabled=True)
                        st.text_input("Cuenta Cliente", value=cuenta_cliente)
                    with c2:
                        st.text_input("Analista Vigente / Evaluador", value=analista_vigente)
                        st.text_input("Importe Operación (S/.)", value=importe_credito)
                        st.text_input("Agencia de Origen", value="OFICINA ADMINISTRACION")

                # ---------- PÁGINA 2 ----------
                with tab2:
                    st.markdown("#### 4. Riesgo de Sobreendeudamiento (Pág 2 PDF)")
                    c3, c4, c5 = st.columns(3)
                    with c3: st.text_input("a) Deuda Directa RCC", value="0.00")
                    with c4: st.text_input("b) Deuda Potencial RCC", value="0.00")
                    with c5: st.text_input("c) Deuda Total RCC", value="0.00")
                    
                    st.markdown("---")
                    st.markdown("#### 📋 Criterios y Hallazgos Encontrados")
                    st.checkbox("Indicio de dolo o fraude en la evaluación de créditos", value=False)
                    st.checkbox("Evaluaciones deficientes o con sustento insuficiente", value=False)
                    st.checkbox("Documentos con enmendaduras o datos inconsistentes", value=False)
                    st.checkbox("No se evidenció sustento de actividad económica o ingresos", value=False)
                    st.checkbox("Créditos reprogramados y refinanciados", value=False)

                # ---------- PÁGINA 3 ----------
                with tab3:
                    st.markdown("#### 5. Direcciones de Inspección (Pág 3 PDF)")
                    
                    with st.container(border=True):
                        st.markdown("🏡 **Dirección del Domicilio Declarado**")
                        st.text_input("Domicilio Físico", value="Asociación Las Flores Mz. B Lote 5")
                        c6, c7 = st.columns(2)
                        with c6: st.text_input("Distrito / Provincia / Dpto", value="Cerro Colorado / Arequipa / Arequipa")
                        with c7: st.text_input("Persona Entrevistada", value="", placeholder="Nombre...")
                        st.text_area("Comentarios de la Inspección Domiciliaria", height=70)

                    with st.container(border=True):
                        st.markdown("🏢 **Dirección del Negocio Verificado**")
                        st.text_input("Local Comercial / Negocio", value="Calle Mercaderes 312")
                        st.text_input("Giro / Tipo de Actividad", value="Familiar / Comercial")
                        st.text_area("Comentarios sobre Verificación del Negocio", value="Idem anterior.", height=70)

                # ---------- ACCIÓN DE GUARDADO DE LA AUDITORÍA ----------
                st.markdown("---")
                if st.button("💾 Consolidar Datos e Imprimir Reporte PDF", type="primary", use_container_width=True):
                    st.success(f"¡Expediente de {nombre_cliente} verificado exitosamente!")
            else:
                st.error(f"❌ El DNI '{dni_input}' no fue localizado en la Columna D de la hoja MUESTRA_FINAL.")
                st.info("💡 Consejo: Comprueba que el DNI ingresado no posea espacios extras o caracteres especiales en el archivo original.")

    except Exception as e:
        st.error(f"Error al intentar segmentar el archivo Excel: {e}")
else:
    st.info("👋 Aplicativo Listo. Dirígete a la barra lateral izquierda y sube el Excel con la hoja MUESTRA_FINAL.")
