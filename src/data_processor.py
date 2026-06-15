import pandas as pd

def load_and_validate_data(timesheet_path, contracts_path, billing_path):

    # 1. Definir los campos requeridos por cada archivo
    required_columns = {
        "Timesheet": ['Employee_ID', 'Employee_Name', 'Project', 'Hours_Worked'],
        "Contracts": ['Project', 'Rate_per_Hour', 'Max_Hours_Per_Week'],
        "Billing": ['Employee_ID', 'Project', 'Hours_Billed', 'Rate_Charged']
    }
    
    # 2. Cargar Datasets
    df_time = pd.read_csv(timesheet_path)
    df_contract = pd.read_csv(contracts_path)
    df_billing = pd.read_csv(billing_path)
    
    # 3. Validar de forma estricta las columnas de cada archivo
    # Verificamos Timesheet
    missing_time = [col for col in required_columns["Timesheet"] if col not in df_time.columns]
    if missing_time:
        raise ValueError(f"El archivo de **Timesheet** no cumple con los requerimientos. Faltan las siguientes columnas obligatorias: {', '.join(missing_time)}")
        
    # Verificamos Contracts
    missing_contract = [col for col in required_columns["Contracts"] if col not in df_contract.columns]
    if missing_contract:
        raise ValueError(f"El archivo de **Contratos (Contracts)** no cumple con los requerimientos. Faltan las siguientes columnas obligatorias: {', '.join(missing_contract)}")
        
    # Verificamos Billing
    missing_billing = [col for col in required_columns["Billing"] if col not in df_billing.columns]
    if missing_billing:
        raise ValueError(f"El archivo de **Facturación (Billing)** no cumple con los requerimientos. Faltan las siguientes columnas obligatorias: {', '.join(missing_billing)}")
    
    # Limpieza básica de strings
    for df in [df_time, df_contract, df_billing]:
        if 'Project' in df.columns:
            df['Project'] = df['Project'].astype(str).str.strip()

    # 2. Cruzar Timesheet con Contratos usando 'Project'
    df_time_contract = pd.merge(df_time, df_contract, on='Project', how='left')
    
    # 3. Cruzar con Billing usando 'Employee_ID' y 'Project'
    final_df = pd.merge(df_billing, df_time_contract, on=['Employee_ID', 'Project'], how='outer')
    
    # Rellenar nulos
    final_df['Hours_Billed'] = final_df['Hours_Billed'].fillna(0)
    final_df['Hours_Worked'] = final_df['Hours_Worked'].fillna(0)
    
    # --- NUEVOS CÁLCULOS FINANCIEROS (EXPECTED VS ACTUAL) ---
    # Horas válidas para cobrar: el mínimo entre lo trabajado y el tope del contrato
    final_df['Valid_Hours_To_Bill'] = final_df.apply(
        lambda row: min(row['Hours_Worked'], row['Max_Hours_Per_Week']) if pd.notna(row['Max_Hours_Per_Week']) else row['Hours_Worked'],
        axis=1
    )
    # Valor Esperado (Contrato)
    final_df['Expected_Billing'] = final_df['Valid_Hours_To_Bill'] * final_df['Rate_per_Hour']
    # Valor Real Cobrado (Factura)
    final_df['Actual_Billing'] = final_df['Hours_Billed'] * final_df['Rate_Charged']
    # Diferencia Financiera
    final_df['Billing_Variance'] = final_df['Actual_Billing'] - final_df['Expected_Billing']
    # ---------------------------------------------------------
    
   # 4. Motor de Reglas de Negocio (Flags de Auditoría)
    flags = []
    reasons = []
    
    for idx, row in final_df.iterrows():
        error_detected = False
        reason_list = []
        
        # Alerta 1: Discrepancia de Tarifas (Cobrar de más o de menos)
        if row['Rate_Charged'] != row['Rate_per_Hour']:
            error_detected = True
            reason_list.append(f"Tarifa incorrecta: Facturado ${row['Rate_Charged']}/h vs Contrato ${row['Rate_per_Hour']}/h.")
            
        # Alerta 2: Violación de horas máximas del contrato por semana
        if row['Hours_Worked'] > row['Max_Hours_Per_Week']:
            error_detected = True
            reason_list.append(f"Exceso de Contrato: Trabajó {row['Hours_Worked']}h superando el límite semanal de {row['Max_Hours_Per_Week']}h.")
            
        # Alerta 3: Sobre-facturación de horas (Se cobra más de lo que se trabajó)
        if row['Hours_Billed'] > row['Hours_Worked']:
            error_detected = True
            reason_list.append(f"Sobre-facturación: Se facturaron {row['Hours_Billed']}h pero el Timesheet registra {row['Hours_Worked']}h.")
            
        # Alerta 4: HORAS FALTANTES / MISSING HOURS (Se cobra menos de lo trabajado) ---
        if row['Hours_Billed'] < row['Hours_Worked']:
            error_detected = True
            missing_hours = row['Hours_Worked'] - row['Hours_Billed']
            reason_list.append(f"Horas faltantes (Missing Hours): Se registraron {row['Hours_Worked']}h en Timesheet pero solo se facturaron {row['Hours_Billed']}h (Faltan {missing_hours}h por cobrar).")
        # --------------------------------------------------------------------------------------
            
        # Asignación de Estado final
        if error_detected:
            flags.append("ERROR")
            reasons.append(" | ".join(reason_list))
        else:
            flags.append("OK")
            reasons.append("Cálculos correctos. Validado contra contrato y timesheet.")
            
    final_df['status'] = flags
    final_df['discrepancy_summary'] = reasons
    
    return final_df