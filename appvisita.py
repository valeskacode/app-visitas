import streamlit as st
import pandas as pd

# Configuración de la página para que sea ancha en PC y adaptable en celular
st.set_page_config(page_title="Auditoría Caja Arequipa", layout="wide")

st.title("📊 Sistema de Auditoría Interna - Caja Arequipa")
st.write("Consulta y revisión de Visitas a Clientes de Pequeña Empresa.")

# 1. Carga del archivo Excel en la barra lateral (así ahorramos espacio en móvil)
with st.sidebar:
    st.header("⚙️ Configuración")
    uploaded_file = st.file_uploader("1. Carga el Excel de Auditoría", type=["xlsx", "xls"])
    
    st.markdown("---")
    st.subheader("📍 Mapeo de Columnas (Índices)")
    # Aquí defines en qué columna numérica del Excel está cada dato (A=0, B=1, C=2...)
    col_dni = st.number_input("Columna DNI (dnicli)", value=5)  # Ajusta según tu Excel
    col_titular = st.number_input("Columna Titular (tituclie)", value=4) # Columna E
    col_cuenta = st.number_input("Columna Cuenta", value=2)
    col_analista = st.number_input("Columna Analista", value=20)
    col_importe = st.number_input("Columna Importe", value=25)

if uploaded_file is not None:
    try:
        # Leer el Excel
        df = pd.read_excel(uploaded_file, header=None)
        st.sidebar.success("¡Excel cargado con éxito!")
        
        # Asegurar que la columna DNI sea texto para la búsqueda limpia
        df[col_dni] = df[col_dni].astype(str).str.strip().str.replace(".0", "", regex=False)

        # 2. Bloque de Búsqueda por DNI (Se ve gigante y limpio en PC y Celular)
        st.markdown("### 🔍 Consulta de Cliente")
        dni_busqueda = st.text_input("Ingresa el DNI del cliente a revisar:", placeholder="Ej. 45678912").strip()

        if dni_busqueda:
            # Buscar coincidencia exacta del DNI
            resultado = df[df[col_dni] == dni_busqueda]

            if not resultado.empty:
                # Extraemos la fila encontrada (la primera coincidencia)
                fila = resultado.index[0]
                
                # Lectura de datos reales desde el Excel basado en los índices mapeados
                nombre_cliente = df.iloc[fila, col_titular]
                nro_cuenta = df.iloc[fila, col_cuenta]
                analista_vigente = df.iloc[fila, col_analista]
                monto_credito = df.iloc[fila, col_importe]

                st.success(f"✅ Cliente Encontrado: **{nombre_cliente}**")

                # 3. DISEÑO RESPONSIVO POR PESTAÑAS (Ideal para Celular y PC)
                tab1, tab2, tab3 = st.tabs([
                    "📄 PÁGINA 1: Datos Generales", 
                    "⚠️ PÁGINA 2: Riesgos y Criterios", 
                    "🏠 PÁGINA 3: Verificación de Campo"
                ])

                # --- PESTAÑA 1: DATOS GENERALES ---
                with tab1:
                    st.markdown("### 👤 Información del Crédito e Integrantes")
                    # Usamos columnas: en PC van al lado, en Celular se apilan solas
                    c1, c2 = st.columns(2)
                    with c1:
                        st.text_input("Titular de la Cuenta", value=nombre_cliente, disabled=True)
                        st.text_input("DNI / LE", value=dni_busqueda, disabled=True)
                        st.text_input("Cuenta Cliente", value=str(nro_cuenta), disabled=True)
                    with c2:
                        st.text_input("Analista Vigente / Evaluador", value=str(analista_vigente), disabled=True)
                        st.text_input("Importe Operación (S/.)", value=str(monto_credito), disabled=True)
                        st.text_input("Agencia", value="OFICINA ADMINISTRACION", disabled=True)

                # --- PESTAÑA 2: RIESGOS Y CRITERIOS ---
                with tab2:
                    st.markdown("### 📉 Riesgo de Sobreendeudamiento")
                    c3, c4, c5 = st.columns(3)
                    with c3:
                        deuda_directa = st.text_input("a) Deuda Directa", value="0.00")
                    with c4:
                        deuda_potencial = st.text_input("b) Deuda Potencial", value="0.00")
                    with c5:
                        deuda_total = st.text_input("c) Deuda Total", value="0.00")
                    
                    st.markdown("---")
                    st.markdown("### 📋 Criterios para Visita a Clientes (Selección del Auditor)")
                    st.write("Marque los hallazgos encontrados durante la auditoría:")
                    
                    # Checkboxes interactivos para la evaluación de la pág 2
                    dolo = st.checkbox("Indicio de dolo o fraude en la evaluación de créditos")
                    deficiente = st.checkbox("Evaluaciones deficientes o con sustento insuficiente")
                    enmendadura = st.checkbox("Documentos con enmendaduras / datos inconsistentes")
                    sin_sustento = st.checkbox("No se evidenció sustento de actividad económica o ingresos")
                    reprogramado = st.checkbox("Créditos reprogramados y refinanciados")

                # --- PESTAÑA 3: VERIFICACIÓN DE CAMPO ---
                with tab3:
                    st.markdown("### 📍 Direcciones y Entrevistas Registradas")
                    
                    # Contenedor visual para el Domicilio
                    with st.container(border=True):
                        st.markdown("🏡 **Dirección del Domicilio (Visita)**")
                        dir_dom = st.text_input("Dirección Completa", value="Asociación Las Flores Mz. B Lote 5")
                        c6, c7, c8 = st.columns(3)
                        with c6: st.text_input("Distrito", value="Cerro Colorado")
                        with c7: st.text_input("Provincia", value="Arequipa")
                        with c8: st.text_input("Departamento", value="Arequipa")
                        st.text_area("Comentarios de la visita al Domicilio", value="Se corroboró vivienda propia mediante título.")

                    # Contenedor visual para el Negocio
                    with st.container(border=True):
                        st.markdown("🏢 **Dirección del Negocio (Visita)**")
                        dir_neg = st.text_input("Dirección del Negocio", value="Calle Mercaderes 312")
                        st.text_input("Tipo de Negocio", value="Familiar / Comercial")
                        st.text_area("Comentarios de la visita al Negocio", value="Cliente manifiesta ventas estables en el local.")

                # --- BOTÓN DE CIERRE: GENERACIÓN ---
                st.markdown("---")
                if st.button("💾 Guardar Cambios y Preparar PDF definitivo", type="primary", use_container_width=True):
                    st.success("¡Datos consolidados correctamente para el reporte final!")
            else:
                st.error(f"❌ No se encontró ningún cliente con el DNI: {dni_busqueda}")

    except Exception as e:
        st.error(f"Error al procesar el archivo Excel: {e}")
else:
    # Mensaje de bienvenida amigable si aún no sube el archivo
    st.info("👋 ¡Bienvenido! Por favor, ve a la barra lateral izquierda y carga tu archivo Excel para iniciar la auditoría.")
