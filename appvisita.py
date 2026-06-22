import streamlit as st
import pandas as pd

# Configuración de pantalla ancha y adaptable (Móvil y PC)
st.set_page_config(page_title="Auditoría Caja Arequipa", layout="wide")

st.title("📊 Sistema de Auditoría Interna - Caja Arequipa")
st.write("Consulta automatizada de carpetas de evaluación por DNI.")

# 1. Carga del archivo Excel
uploaded_file = st.sidebar.file_uploader("1. Carga el Excel de Auditoría", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Leer el Excel completo sin cabecera fija
        df = pd.read_excel(uploaded_file, header=None)
        st.sidebar.success("¡Excel cargado con éxito!")

        # Mapeo de índices de columnas según tu estructura (A=0, B=1, C=2...)
        col_dni = 3       # Columna D (DNI Cliente)
        col_nombres = 4   # Columna E (Nombres Analista)
        col_cargo = 14    # Columna O (Cargo Analista)
        col_cod = 23      # Columna X (Código Analista)

        # Mapeo de las 12 Preguntas (Páginas 2 y 3)
        preguntas_indices = {
            "Pregunta 1 (AA)": 26, "Pregunta 2 (AD)": 29, "Pregunta 3 (AG)": 32,
            "Pregunta 4 (AJ)": 35, "Pregunta 5 (AM)": 38, "Pregunta 6 (AP)": 41,
            "Pregunta 7 (AS)": 44, "Pregunta 8 (AV)": 47, "Pregunta 9 (AY)": 50,
            "Pregunta 10 (BB)": 53, "Pregunta 11 (BE)": 56, "Pregunta 12 (BH)": 59
        }

        # --- FUNCIÓN DE LIMPIEZA TOTAL DE DNI ---
        def limpiar_dni(val):
            if pd.isna(val):
                return ""
            if isinstance(val, float):
                if val.is_integer():
                    val = int(val)
            s = str(val).strip()
            if s.endswith('.0'):
                s = s[:-2]
            # Autocompletar con ceros a la izquierda si el DNI empieza con 0
            if s.isdigit() and len(s) <= 8 and len(s) > 0:
                return s.zfill(8)
            return s

        # Aplicar limpieza a la columna D
        df[col_dni] = df[col_dni].apply(limpiar_dni)

        # Filtrar la lista de DNIs válidos eliminando el texto del encabezado (ej. "DNI", "DOCUMENTO")
        lista_dnis = [
            x for x in df[col_dni].unique() 
            if x != "" and not x.lower().startswith("dni") and not x.lower().startswith("doc") and x.isdigit()
        ]

        # 2. BUSCADOR DESPLEGABLE (Perfecto para Celular y evita errores de digitación)
        st.markdown("### 🔍 Selección de Expediente")
        dni_seleccionado = st.selectbox(
            "Busca o selecciona el DNI del cliente:", 
            options=["-- Selecciona un DNI --"] + sorted(lista_dnis)
        )

        if dni_seleccionado != "-- Selecciona un DNI --":
            # Buscar la fila correspondiente al DNI seleccionado
            fila_idx = df[df[col_dni] == dni_seleccionado].index[0]

            # Función auxiliar para extraer datos de forma segura sin romper el código
            def obtener_valor(fila, columna):
                if columna < len(df.columns):
                    val = df.iloc[fila, columna]
                    return "" if pd.isna(val) else str(val).strip()
                return "No disponible"

            # Extraer Datos Generales
            cod_analista = obtener_valor(fila_idx, col_cod)
            nombre_analista = obtener_valor(fila_idx, col_nombres)
            cargo_analista = obtener_valor(fila_idx, col_cargo)

            st.success(f"✅ Expediente cargado correctamente para el DNI: {dni_seleccionado}")

            # 3. DISEÑO DE PESTAÑAS RESPONSIVO (Páginas 1, 2 y 3 del PDF)
            tab1, tab2, tab3 = st.tabs([
                "📄 PÁGINA 1: Datos Generales", 
                "⚠️ PÁGINA 2: Evaluación (Preguntas 1-8)", 
                "🏠 PÁGINA 3: Revisión de Campo (Preguntas 9-12)"
            ])

            # ================= PESTAÑA 1 =================
            with tab1:
                st.subheader("Información General del Analista Evaluado")
                c1, c2 = st.columns(2)
                with c1:
                    st.text_input("Código del Analista (Columna X)", value=cod_analista, disabled=True)
                    st.text_input("Nombres y Apellidos (Columna E)", value=nombre_analista, disabled=True)
                with c2:
                    st.text_input("Cargo (Columna O)", value=cargo_analista, disabled=True)
                    st.text_input("DNI del Cliente Consultado (Columna D)", value=dni_seleccionado, disabled=True)

            # ================= PESTAÑA 2 =================
            with tab2:
                st.subheader("Criterios de Riesgo y Evaluación de Políticas")
                st.info("Valores recuperados desde el Excel para las preguntas del formulario:")
                
                # Mostrar preguntas de la 1 a la 8 en un diseño limpio adaptado a móvil
                c3, c4 = st.columns(2)
                with c3:
                    st.text_area("Pregunta 1 (Columna AA)", value=obtener_valor(fila_idx, 26), height=70)
                    st.text_area("Pregunta 2 (Columna AD)", value=obtener_valor(fila_idx, 29), height=70)
                    st.text_area("Pregunta 3 (Columna AG)", value=obtener_valor(fila_idx, 32), height=70)
                    st.text_area("Pregunta 4 (Columna AJ)", value=obtener_valor(fila_idx, 35), height=70)
                with c4:
                    st.text_area("Pregunta 5 (Columna AM)", value=obtener_valor(fila_idx, 38), height=70)
                    st.text_area("Pregunta 6 (Columna AP)", value=obtener_valor(fila_idx, 41), height=70)
                    st.text_area("Pregunta 7 (Columna AS)", value=obtener_valor(fila_idx, 44), height=70)
                    st.text_area("Pregunta 8 (Columna AV)", value=obtener_valor(fila_idx, 47), height=70)

            # ================= PESTAÑA 3 =================
            with tab3:
                st.subheader("Revisiones Pendientes y Verificación de Campo")
                
                with st.container(border=True):
                    st.markdown("🔍 **Resultados Financieros y Visita al Aval**")
                    st.text_area("Pregunta 9: Revisión Pendiente (Columna AY)", value=obtener_valor(fila_idx, 50))
                    st.text_area("Pregunta 10: Revisión Pendiente (Columna BB)", value=obtener_valor(fila_idx, 53))
                    st.text_area("Pregunta 11: Revisión Pendiente (Columna BE)", value=obtener_valor(fila_idx, 56))
                    st.text_area("Pregunta 12: Revisión Pendiente (Columna BH)", value=obtener_valor(fila_idx, 59))

            # ================= POLÍTICAS FIJAS SOLICITADAS =================
            st.markdown("---")
            with st.container(border=True):
                st.markdown("📌 **Políticas Generales del Informe:**")
                st.caption("- PAGOS INCREMENTADOS EN DIVERSAS AGENCIAS")
                st.caption("- 8 políticas una procedimientos")
                st.caption("- performa variable")

            # Botón de Guardado adaptado a todo ancho de pantalla
            if st.button("💾 Generar Informe PDF definitivo", type="primary", use_container_width=True):
                st.success(f"¡Datos consolidados listos para exportar al formato de Auditoría!")

    except Exception as e:
        st.error(f"Error al procesar el archivo Excel: {e}")
else:
    st.info("👋 Por favor, abre la barra lateral izquierda y sube tu archivo Excel de auditoría para comenzar.")
