# Validador de facturas impulsado por IA

Este sistema automatiza el proceso de auditoría y conciliación financiera cruzando datos de contratos, horas reales reportadas y reportes de facturación final. Utiliza analítica de datos en Python para el filtrado de reglas corporativas e Inteligencia Artificial (OpenAI) para la resolución semántica de problemas y sugerencias correctivas.

## 🚀 Características del Proyecto

1. **Validación Automática de Datos:** Une e identifica de forma instantánea desajustes en tarifas, sobre-facturación de horas, horas faltantes y violaciones a los límites de horas contratadas.
2. **Razonamiento con IA:** Traduce errores crudos de bases de datos a explicaciones ejecutivas claras y accionables.
3. **Interfaz Interactiva:** Construida con Streamlit para permitir a usuarios no técnicos cargar archivos y realizar auditorías en tiempo real.

## 📁 Estructura del Repositorio

* `data/`: Archivos muestra (`timesheet.csv`, `contracts.csv`, `billing.csv`).
* `src/data_processor.py`: Lógica matemática y cruce relacional de datasets (Generación de Flags OK/ERROR).
* `src/ai_analyzer.py`: Integración con OpenAI API empleando JSON estructurado.
* `src/app.py`: Frontend interactivo en Streamlit.

## Instalacion

1. Descargue los archivos desde el repositorio de github (https://github.com/RobinsonAlcantara/Prueba-Tecnica-1)
2. Instale los requerimientos que se encuentran en el archivo requirements.txt utilizando la instruccion "pip install -r requirements.txt" desde su terminal en la carpeta raiz del proyecto.
3. Ejecute la instruccion "python -m streamlit run src/app.py" para iniciar el proyecto o solucion desde la raiz del proyecto. 

**Si quiere usar la aplicacion directamente puede dirigirse a la URL https://robinsonalcantara-prueba-tecnica-1-srcapp-zdvidl.streamlit.app/**

## 📖Guía de Usuario: Validador de facturas impulsado por IA

Bienvenido al Validador de facturas impulsado por IA. Esta plataforma te permite auditar reportes financieros y de horas de forma automática, detectando errores humanos de cobro y utilizando Inteligencia Artificial para entender los problemas y proponer soluciones.

Sigue estos sencillos pasos para auditar tus datos en menos de dos minutos.

### 🛠️ Paso 1: Preparación de tus Archivos (Formatos Admitidos)
Para que el sistema procese la información correctamente, asegúrate de tener listos tus tres archivos en formato CSV con los siguientes nombres de columna exactos:

**contracts.csv:** `Project`, `Rate_per_Hour`, `Max_Hours_Per_Week`
**timesheet.csv:** `Employee_ID`, `Employee_Name`, `Project`, `Hours_Worked`
**billing.csv:** `Employee_ID`, `Project`, `Hours_Billed`, `Rate_Charged`

### 📤 Paso 2: Carga de Datos en la Plataforma

1. Abre la aplicación en tu navegador web.
2. Dirígete a la Barra Lateral Izquierda (Sidebar).
3. Encontrarás tres botones de carga de archivos (Browse files).
4. Arrastra o selecciona cada archivo CSV en su casilla correspondiente:
    * Sube el archivo de horas en Timesheet CSV.
    * Sube el archivo de tarifas en Contracts CSV.
    * Sube el reporte de cobros en Billing CSV.

### 📊 Paso 3: Interpretación del Reporte de Auditoría

Una vez subidos los tres archivos, el sistema calculará todo automáticamente y desplegará el panel principal:

1. Tarjetas de KPI: En la parte superior verás el total de registros auditados y el número exacto de alertas o discrepancias encontradas.
2. Tabla de Resultados: Aquí verás la comparación financiera directa requerida por el negocio:
    * Valor esperado ($): El dinero exacto que debió cobrarse según el contrato y las horas del timesheet (respetando los topes semanales).
    * Valor actual ($): El dinero que se está cobrando realmente en la factura.
    * Diferencia ($): La diferencia económica. Si es positiva (+) significa que se está cobrando de más (sobre-facturación); si es negativa (-) la empresa está perdiendo   dinero por cobrar de menos.
    * Status: Si la fila está en OK, todo coincide. Si está en ERROR, el sistema ha detectado una anomalía.

### 🤖 Paso 4: Análisis Automatizado con Inteligencia Artificial

Si el sistema detecta filas con el estado ERROR, puedes solicitar una auditoría semántica detallada usando IA:

1. Desplázate hacia abajo hasta la sección Análisis con Inteligencia Artificial.
2. Abre el menú desplegable y selecciona el empleado y proyecto que deseas investigar.
3. Haz clic en el botón "Generar Análisis de Mitigación con IA".
4. El sistema llamará al modelo de lenguaje, el cual te devolverá un informe dividido en dos partes:
    * Análisis Ejecutivo: Una explicación detallada y corporativa del motivo del error.
    * Acción Correctiva Sugerida: Los pasos administrativos exactos que debe tomar el equipo de finanzas para corregir la situación antes de enviar la factura al cliente final.

### 🚨 Tipos de Alertas que el Sistema Detecta de forma Automática

**Tarifas Incorrectas:** Cuando la tarifa por hora en la factura no coincide con la tarifa firmada en el contrato.
**Exceso de Contrato:** Cuando un empleado trabajó más horas de las permitidas semanalmente por el contrato del proyecto.
**Sobre-facturación de Horas:** Cuando se intentan cobrar más horas de las que el empleado realmente registró en su plantilla de marcas (timesheet).
**Horas faltantes (Missing Hours):** Cuando se esta intentado cobrar menos de las horas trabajadas.