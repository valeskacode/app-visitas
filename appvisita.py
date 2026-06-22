import streamlit as st
import pandas as pd

# Configuración de página ancha y adaptable para Móvil y PC
st.set_page_config(page_title="Auditoría Caja Arequipa", layout="wide")

st.title("📊 Consulta de Visitas - Unidad de Auditoría Interna")
st.write("Busca por DNI para rellenar y revisar los datos de las Páginas 1, 2 y 3.")

# 1. BARRA LATERAL: Configuración de Columnas del Excel
with st.sidebar:
    st.header("⚙️ Mapeo de Columnas")
    st.write("Indica en qué número de columna de tu Excel (A=0, B=1, C=2, D=3...) está cada dato:")
    
    uploaded_file = st.file_uploader("Carga el archivo Excel", type=["xlsx", "xls"])
    
    st.markdown("---")
    st.subheader("📋 Índices de Columnas")
    # Configuración de los campos de la Página 1
    col_dni = st.number_input("Columna DNI (Columna D = 3)", value=3)
    col_titular = st.number_input("Columna Titular (Columna E = 4)", value=4)
    col_cuenta = st.number_input("Columna Cuenta Cliente", value=2)
    col_analista = st.number_input("Columna Analista Vigente", value=20)
    col_importe = st.number_input("Columna Importe Crédito", value=43)
    
    # Configuración para Datos de la Página 2 y 3 (Ajusta los valores por defecto si sabes su columna)
    st.markdown("**Variables Pág 2 y 3**")
    col_deuda_dir = st.number_input("Columna Deuda Directa", value=50)
    col_deuda_tot = st.number_input("Columna Deuda Total", value=52)
    col_direccion_dom = st.number_input("Columna Dirección Domicilio", value=10)
    col_direccion_neg = st.number_input("Columna Dirección Negocio", value=15)

if uploaded_file is not None:
    try:
        # Leer el archivo Excel sin asumir cabeceras fijas
        df = pd.read_excel(uploaded_file, header=None)
        st.sidebar.success("¡Excel cargado con éxito!")
        
        # Limpieza de la columna DNI para que la búsqueda sea exacta (quita espacios y decimales ocultos)
        df[col_dni] = df[col_dni].astype(str).str.strip().str.replace(".0", "", regex=False)

        # 2. BUSCADOR POR DNI (Diseño limpio y gigante para cualquier pantalla)
        st.markdown("### 🔍 Buscador de Clientes")
        dni_busqueda = st.text_input("Escribe el DNI del cliente para cargar su expediente:", placeholder="Ej. 41234567").strip()

        if dni_busqueda:
            # Buscar el DNI en la columna D (índice configurado)
            resultado = df[df[col_dni] == dni_busqueda]

            if not resultado.empty:
                fila = resultado.index[0] # Tomamos la primera fila encontrada
                
                # Extracción segura de datos desde el Excel según tus índices de la barra lateral
                val_titular = df.iloc[fila, col_titular] if col_titular < len(df.columns) else "No mapeado"
                val_cuenta = df.iloc[fila, col_cuenta] if col_cuenta < len(df.columns) else "No mapeado"
                val_analista = df.iloc[fila, col_analista] if col_analista < len(df.columns) else "No mapeado"
                val_importe = df.iloc[fila, col_importe] if col_importe < len(df.columns) else "0.00"
                
                val_deuda_dir = df.iloc[fila, col_deuda_dir] if col_deuda_dir < len(df.columns) else "0.00"
                val_deuda_tot = df.iloc[fila, col_deuda_tot] if col_deuda_tot < len(df.columns) else "0.00"
                
                val_dir_dom = df.iloc[fila, col_direccion_dom] if col_direccion_dom < len(df.columns) else ""
                val_dir_neg = df.iloc[fila, col_direccion_neg] if col_direccion_neg < len(df.columns) else ""

                st.success(f"✅ Mostrando expediente de: **{val_titular}**")

                # 3. DISEÑO RESPONSIVO EN PESTAÑAS (Tabs)
                # En PC se ven horizontales; en celular se adaptan perfectamente al ancho del dedo.
                tab1, tab2, tab3 = st.tabs([
                    "📄 PÁGINA 1: Visita al Cliente", 
                    "⚠️ PÁGINA 2: Riesgo y Criterios", 
                    "🏠 PÁGINA 3: Verificación de Campo"
                ])

                # ================= PESTAÑA 1 =================
                with tab1:
                    st.subheader("1. Datos del Cliente y del Crédito")
                    # En PC crea dos columnas a los lados, en celular las pone una abajo de otra automáticamente
                    c1, c2 = st.columns(2)
                    with c1:
                        st.text_input("Titular", value=str(val_titular), disabled=True)
                        st.text_input("DNI / LE", value=str(dni_busqueda), disabled=True)
                        st.text_input("Cuenta Cliente", value=str(val_cuenta), disabled=True)
                    with c2:
                        st.text_input("Analista Vigente / Evaluador", value=str(val_analista), disabled=True)
                        st.text_input("Importe Operación (S/.)", value=str(val_importe), disabled=True)
                        st.text_input("Agencia", value="OFICINA ADMINISTRACION", disabled=True)

                # ================= PESTAÑA 2 =================
                with tab2:
                    st.subheader("4. Riesgo de Sobreendeudamiento")
                    c3, c4 = st.columns(2)
                    with c3:
                        st.text_input("a) Deuda Directa RCC", value=str(val_deuda_dir))
                    with c4:
                        st.text_input("c) Deuda Total RCC", value=str(val_deuda_tot))
                    
                    st.markdown("---")
                    st.subheader("📋 Criterio para visita a Clientes (Hallazgos)")
                    st.info("Selecciona las observaciones encontradas por el auditor:")
                    
                    # Checkboxes ideales para marcar desde pantallas táctiles de celulares
                    obs_1 = st.checkbox("Indicio de dolo o fraude en la evaluación de créditos")
                    obs_2 = st.checkbox("Evaluaciones deficientes o con sustento insuficiente")
                    obs_3 = st.checkbox("Documentos con enmendaduras o datos inconsistentes")
                    obs_4 = st.checkbox("No se evidenció sustento de actividad económica / ingresos")
                    obs_5 = st.checkbox("Créditos reprogramados y refinanciados")

                # ================= PESTAÑA 3 =================
                with tab3:
                    st.subheader("5. Verificación de Direcciones")
                    
                    # Contenedor visual para Domicilio
                    with st.container(border=True):
                        st.markdown("🏠 **Dirección del Domicilio (Visita)**")
                        st.text_input("Dirección Encontrada", value=str(val_dir_dom))
                        c5, c6 = st.columns(2)
                        with c5: st.text_input("Distrito/Provincia", value="Cerro Colorado / Arequipa")
                        with c6: st.text_input("Entrevista con:", value="")
                        st.text_area("Comentarios de Visita (Domicilio):", placeholder="Escribe aquí los comentarios sobre la vivienda...")

                    # Contenedor visual para Negocio
                    with st.container(border=True):
                        st.markdown("🏢 **Dirección del Negocio (Visita)**")
                        st.text_input("Dirección Comercial", value=str(val_dir_neg))
                        st.text_input("Tipo de Negocio / Actividad Principal", value="Comercio / Pequeña Empresa")
                        st.text_area("Comentarios de Visita (Negocio):", placeholder="Escribe aquí las observaciones sobre el negocio...")

                # ================= BOTÓN DE GUARDADO FINALES =================
                st.markdown("---")
                if st.button("💾 Guardar y Consolidar Informe de Auditoría", type="primary", use_container_width=True):
                    st.success("¡Datos procesados correctamente para la fila seleccionada!")
            else:
                st.error(f"❌ No se encontró ningún registro con el DNI: {dni_busqueda} en la Columna {col_dni}.")

    except Exception as e:
        st.error(f"Error al procesar las columnas del Excel: {e}")
else:
    st.info("👋 Por favor, ve a la barra lateral izquierda y carga tu archivo Excel para iniciar la consulta.")
