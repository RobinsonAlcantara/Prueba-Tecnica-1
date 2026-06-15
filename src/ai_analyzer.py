import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_analysis(row_data):    
    """Genera una explicación ejecutiva adaptada a las nuevas columnas del dataset"""
    prompt = f"""
    Actúa como un Auditor Financiero Senior. Analiza la siguiente discrepancia detectada en nuestro proceso de facturación:
    
    - ID Empleado: {row_data.get('Employee_ID')}
    - Nombre: {row_data.get('Employee_Name')}
    - Proyecto: {row_data.get('Project')}
    - Tarifa del Contrato: ${row_data.get('Rate_per_Hour')}/h
    - Máximo de Horas Permitidas (Contrato): {row_data.get('Max_Hours_Per_Week')}h
    - Horas Reales Trabajadas (Timesheet): {row_data.get('Hours_Worked')}h
    - Horas Facturadas (Billing): {row_data.get('Hours_Billed')}h
    - Tarifa Facturada (Billing): ${row_data.get('Rate_Charged')}/h
    
    - Resumen de las violaciones de datos encontradas: {row_data.get('discrepancy_summary')}
    
    Por favor provee un JSON estrictamente con la siguiente estructura:
    {{
        "analisis_ejecutivo": "Explicación clara, detallada y corporativa del problema.",
        "accion_correctiva": "Pasos exactos a seguir para enmendar el error con el cliente o el equipo interno."
    }}
    """
    
    try:
        response = client.responses.create(
            model="gpt-5.4-mini",
            input=[{"role": "user", "content": prompt}],
            store=True,
        )        
        return response.output_text
    except Exception as e:
        return f'{{"error": "No se pudo conectar con la IA: {str(e)}"}}'