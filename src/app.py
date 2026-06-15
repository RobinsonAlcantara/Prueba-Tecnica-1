import streamlit as st
import pandas as pd
import json
from data_processor import load_and_validate_data
from ai_analyzer import generate_ai_analysis

st.set_page_config(page_title="Validador de facturas impulsado por IA", layout="wide")
st.title("Validador de facturas impulsado por IA")
st.subheader("Auditoría inteligente automatizada de contratos y facturación")

#Separacion de la interfaz den pestañas
tab1, tab2 = st.tabs(["Panel de Auditoría", "Documentación"])

with tab1:
# Sidebar para cargar archivos
    st.sidebar.header("1. Carga de Datasets")
    timesheet_file = st.sidebar.file_uploader("Timesheet CSV", type="csv")
    contracts_file = st.sidebar.file_uploader("Contracts CSV", type="csv")
    billing_file = st.sidebar.file_uploader("Billing CSV", type="csv")

    if timesheet_file and contracts_file and billing_file:
        # Envolvemos el procesamiento en un try-except para atrapar errores de columnas
        try:
            # Procesar Datos
            df_result = load_and_validate_data(timesheet_file, contracts_file, billing_file)
            
            # KPIs Rápidos
            total_rows = len(df_result)
            errors_count = len(df_result[df_result['status'] == 'ERROR'])
            
            col1, col2 = st.columns(2)
            col1.metric("Total Registros Auditados", total_rows)
            col2.metric("Errores / Discrepancias Detectadas", errors_count, delta=f"{errors_count} alertas", delta_color="inverse")
        
            
            st.write("### Vista General del Reporte de Auditoría")
            
            # Seleccionamos y ordenamos las columnas clave incluyendo la comparación esperada vs actual
            columns_to_show = [
                'Employee_ID', 
                'Employee_Name',
                'Project', 
                'Expected_Billing',   # Lo que se debió cobrar según contrato
                'Actual_Billing',     # Lo que figura en la factura real
                'Billing_Variance',   # La diferencia o desvío de dinero
                'status', 
                'discrepancy_summary'
            ]
            
            # Mostramos el DataFrame aplicando un formateo estético para los valores monetarios
            st.dataframe(
                df_result[columns_to_show],hide_index=True,
                column_config={
                    "Employee_ID": st.column_config.TextColumn("ID Empleado"),
                    "Employee_Name": st.column_config.TextColumn("Nombre"),
                    "Project": st.column_config.TextColumn("Proyecto"),
                    "Expected_Billing": st.column_config.NumberColumn("Valor Esperado", format="$%.2f"),
                    "Actual_Billing": st.column_config.NumberColumn("Valor Actual", format="$%.2f"),
                    "Billing_Variance": st.column_config.NumberColumn("Diferencia", format="$%.2f"),
                    "status": st.column_config.TextColumn("Estado"),
                    "discrepancy_summary": st.column_config.TextColumn("Resumen de Discrepancias")
                }
            )
                
            # Sección de Análisis de IA
            st.write("---")
            st.write("### 🤖 Análisis con Inteligencia Artificial (Casos de ERROR)")
            
            df_errors = df_result[df_result['status'] == 'ERROR']
            
            if not df_errors.empty:
                selected_index = st.selectbox(
                    "Selecciona una fila con ERROR para que la IA genere el reporte de mitigación:",
                    df_errors.index,
                    format_func=lambda idx: f"Empleado {df_errors.loc[idx, 'Employee_ID']} - Proyecto {df_errors.loc[idx, 'Project']}"
                )
                
                if st.button("Generar Análisis de Mitigación con IA"):
                    with st.spinner("Analizando discrepancia con GPT..."):
                        row_data = df_errors.loc[selected_index].to_dict()
                        ai_response_raw = generate_ai_analysis(row_data)
                        
                        try:
                            ai_response = json.loads(ai_response_raw)
                            st.info(f"**Análisis Ejecutivo:**\n{ai_response.get('analisis_ejecutivo')}")
                            st.success(f"**Acción Correctiva Sugerida:**\n{ai_response.get('accion_correctiva')}")
                        except:
                            st.write(ai_response_raw)
            else:
                st.success("¡Felicidades! No se encontraron discrepancias en este lote de datos.")
        except ValueError as e:
            # Si falta una columna, detenemos la app y mostramos el mensaje de error personalizado
            st.error(f"🚨 **Error de Validación de Datos:** {str(e)}")
            st.warning("⚠️ Por favor, revisa la pestaña **'Documentacion** para confirmar la estructura exacta de columnas que debe tener cada archivo antes de volver a cargarlo.")
    else:
        st.info("Por favor, sube los 3 archivos CSV requeridos en la barra lateral para comenzar la auditoría.")

with tab2:
    st.header("📖 Guía de Usuario: Validador de Facturación")
    st.write(
        "Esta plataforma te permite auditar reportes financieros cruzando datos de contratos, "
        "horas trabajadas y la facturación real, automatizando la detección de errores mediante reglas de negocio e IA."
    )
    
    st.write("---")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("📋 1. Preparación de Archivos")
        st.write("Asegúrate de cargar archivos `.csv` que incluyan las siguientes columnas exactas:")
        st.markdown("""
        * **contracts.csv:** `Project`, `Rate_per_Hour`, `Max_Hours_Per_Week`
        * **timesheet.csv:** `Employee_ID`, `Employee_Name`, `Project`, `Hours_Worked`
        * **billing.csv:** `Employee_ID`, `Project`, `Hours_Billed`, `Rate_Charged`
        """)
        
        st.subheader("📤 2. Flujo de Trabajo")
        st.markdown("""
        1. Sube los tres archivos correspondientes en la barra lateral izquierda.
        2. Revisa las tarjetas de **KPI** en la parte superior para ver el consolidado de alertas.
        3. Analiza la tabla interactiva buscando las filas con estado **ERROR**.
        """)

    with col_g2:
        st.subheader("📊 3. Interpretación de Columnas Financieras")
        st.markdown("""
        * **Valor Esperado ($):** El dinero que se debió cobrar según contrato (respetando topes de horas semanales).
        * **Valor Actual ($):** El dinero que se está cobrando realmente en la factura emitida.
        * **Diferencia ($):** La diferencia monetaria. Una varianza **positiva (+)** indica sobre-facturación. Una varianza **negativa (-)** indica pérdidas para la empresa por cobrar de menos.
        """)
        
        st.subheader("🚨 Reglas Automáticas Detectadas")
        st.markdown("""
        * **Mapeo de Tarifas:** Si el costo por hora cobrado no coincide con el del contrato.
        * **Exceso de Horas:** Si el empleado trabajó más horas del tope legal contratado.
        * **Sobre-facturación:** Si se cobran más horas de las que figuran en el registro de *timesheet*.
        """)
        
    st.write("---")
    st.subheader("🤖 4. ¿Cómo usar el Asistente de IA?")
    st.write(
        "Al final del panel de auditoría, si existen errores, podrás seleccionar la fila "
        "afectada desde un menú desplegable. Al hacer clic en **'Generar Análisis de Mitigación'**, "
        "el LLM analizará el contexto del error humano y redactará un informe explicativo junto con "
        "las acciones correctivas inmediatas para el equipo de cuentas."
    )