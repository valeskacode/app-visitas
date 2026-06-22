import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Sistema de Auditoría - Caja Arequipa")
st.write("Carga tu archivo Excel para procesar las visitas de auditoría.")

# 1. Botón para subir el archivo Excel
uploaded_file = st.file_uploader("Selecciona el archivo Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Leer el Excel sin cabeceras fijas para guiarnos por la posición de las columnas
        df = pd.read_excel(uploaded_file, header=None)
        st.success("¡Excel cargado con éxito!")
        
        # Mostrar una vista previa de los datos
        st.write("Vista previa de los datos cargados:")
        st.dataframe(df.head())

        # Mapeo de columnas según tu estructura (A=0, B=1, C=2...)
        col_nombres = 4   # Columna E
        col_cargo = 14   # Columna O
        col_cod = 23     # Columna X
        
        # Control de filas para elegir a quién revisar
        fila_a_procesar = st.number_input("Selecciona el número de fila a procesar", min_value=1, max_value=len(df)-1, value=1)
        
        # Extraer los datos reales de la fila seleccionada
        cod_analista = df.iloc[fila_a_procesar, col_cod]
        nombre_analista = df.iloc[fila_a_procesar, col_nombres]
        cargo_analista = df.iloc[fila_a_procesar, col_cargo]

        # Mostrar los datos del analista en pantalla
        st.subheader("Datos del Auditor / Analista Detectado:")
        st.write(f"**Código:** {cod_analista}")
        st.write(f"**Nombre:** {nombre_analista}")
        st.write(f"**Cargo:** {cargo_analista}")

        # Políticas fijas solicitadas al final de tu reporte
        st.info("📌 **Políticas y Procedimientos Aplicados:**\n"
                "- PAGOS INCREMENTADOS EN DIVERSAS AGENCIAS\n"
                "- 8 políticas una procedimientos\n"
                "- performa variable")

        # Botón para generar el reporte definitivo
        if st.button("Generar Informe PDF"):
            st.success(f"¡Procesando reporte para {nombre_analista}!")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
