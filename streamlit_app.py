import streamlit as st

# --- Configuración de la Página ---
st.set_page_config(page_title="Guía: HTML Content en Power BI", layout="wide")

st.title("💡 Visualizador HTML Content en Power BI")
st.header("Guía Completa para KPI/OKR y Visualizaciones Dinámicas")

st.markdown(
    """
    El visualizador **HTML Content** permite inyectar código HTML/SVG directamente en un informe de Power BI, lo cual es esencial para crear KPI visuales personalizados que superan las limitaciones de formato estándar.
    """
)

st.markdown("---")

# --- Definición de Pestañas ---

tab1, tab2, tab3 = st.tabs(["1. Conceptos y Requisitos", "2. Implementación Paso a Paso en Power BI", "3. Ejemplos Avanzados (KPI, OKR y Código)"])

# ----------------------------------------------------------------------
# PESTAÑA 1: Conceptos (Sin cambios)
# ----------------------------------------------------------------------
with tab1:
    st.subheader("¿Qué es el Visualizador HTML Content?")
    st.markdown(
        """
        Es un visualizador personalizado (no nativo de Microsoft) que interpreta código HTML que se le pasa como una cadena de texto.
        
        * **Propósito:** Superar las limitaciones de formato y visualización de las tarjetas o tablas estándar de Power BI.
        * **Mecanismo:** El resultado de la medida DAX debe ser una cadena de texto que contiene código **HTML, CSS o SVG**.
        """
    )

    st.subheader("Mecanismo Clave: DAX como Generador de Código")
    st.markdown(
        """
        La clave es usar DAX para calcular valores y luego concatenarlos con etiquetas de código.
        
        * **DAX:** Calcula valores, compara (`IF`, `SWITCH`) y define colores o tamaños.
        * **Concatenación:** Usa el operador `&` o la función `CONCATENATEX` para unir el valor DAX con el código SVG/HTML.
        """
    )
    
    st.markdown("---")
    st.subheader("Requisitos Previos")
    st.warning("Necesitas descargar e importar un visualizador personalizado de HTML Content (ej. 'HTML Viewer' o 'Text Filter') desde AppSource de Microsoft.")


# ----------------------------------------------------------------------
# PESTAÑA 2: Implementación Paso a Paso en Power BI (NUEVA)
# ----------------------------------------------------------------------
with tab2:
    st.subheader("Guía Paso a Paso para Aplicar HTML Content")
    
    st.markdown(
        """
        Sigue estos pasos para importar el visualizador y preparar tu medida DAX para la visualización dinámica.
        """
    )
    
    st.markdown("### 1. Importar el Visualizador")
    st.markdown(
        """
        1.  Abre **Power BI Desktop**.
        2.  En la pestaña **Inicio** o **Insertar**, haz clic en el icono **Obtener más objetos visuales** (tres puntos "..." o el icono de AppSource).
        3.  Busca y selecciona un visualizador que soporte HTML, como **"HTML Content"** o **"HTML Viewer"**.
        4.  Haz clic en **Agregar** para importar el visualizador a tu informe.
        """
    )
    
    st.markdown("### 2. Crear la Medida DAX (Generadora de Código)")
    st.markdown(
        """
        1.  Ve a la vista **Datos** o **Modelo** y selecciona la tabla donde quieres guardar la medida.
        2.  Haz clic en **Nueva medida**.
        3.  Escribe el código DAX que genera la cadena HTML/SVG.
        """
    )
    
    st.code(
        """
        // Ejemplo de Medida que genera un Semáforo condicional
        Medida Semáforo = 
        VAR Valor = [Ventas Netas] // Asume que tienes una medida base de ventas
        VAR Color = SWITCH(TRUE(), 
                        Valor >= 50000, "green", 
                        Valor >= 20000, "orange", 
                        "red")
        
        // El resultado es una cadena de texto que HTML Content interpreta.
        RETURN 
            "<span style='font-size: 20px; color: " & Color & ";'>&#9679;</span>" & 
            " " & FORMAT(Valor, "$#,0")
        """,
        language='dax'
    )

    st.markdown("### 3. Configurar la Visualización")
    st.markdown(
        """
        1.  Arrastra el visualizador **HTML Content** al lienzo de tu informe.
        2.  Arrastra la medida que acabas de crear (**Medida Semáforo**) al campo principal del visualizador (a menudo llamado **Value** o **Data**).
        3.  El visualizador ahora mostrará un círculo de color (semáforo) junto al valor, según las reglas que definiste en DAX.
        """
    )


# ----------------------------------------------------------------------
# PESTAÑA 3: Ejemplos Avanzados (KPI, OKR y Código) (MODIFICADA)
# ----------------------------------------------------------------------
with tab3:
    st.header("3. Ejemplos Avanzados: KPI, OKR y Código SVG")
    
    st.markdown(
        """
        Estos ejemplos muestran cómo usar la capacidad de HTML Content para la monitorización de objetivos de negocio (KPI/OKR), utilizando SVG para el impacto visual.
        """
    )

    # --- 1. KPI: Barra de Progreso Dinámica (SVG) ---
    st.subheader("1. KPI: Barra de Progreso Dinámica (Métrica hacia Meta)")
    
    col_code_1, col_business_1 = st.columns(2)
    
    with col_business_1:
        st.markdown("#### 🎯 Aplicación KPI/OKR")
        st.markdown(
            """
            * **KPI:** Porcentaje de Cumplimiento de Ventas del Trimestre.
            * **OKR:** Resultado Clave (KR): Aumentar la tasa de cumplimiento del objetivo de ingresos de la Región Norte del 65% al 90%.
            * **Uso:** Ideal en una Matriz para ver el progreso de cada región o categoría.
            """
        )
    
    with col_code_1:
        st.code(
            """
            // DAX: Asumimos que [Progreso %] existe (ej: DIVIDE([Ventas], [Meta]))
            VAR Progreso = ROUND([Progreso %] * 100, 0) 
            VAR ColorBarra = IF(Progreso >= 100, "teal", "dodgerblue")

            VAR SVGCode =
                "<svg width='100%' height='15'>" & 
                // ... (Código SVG para dibujar barra y porcentaje) ...
                "<rect width='" & Progreso & "%' height='100%' fill='" & ColorBarra & "' rx='3' ry='3' />" &
                // ...
                "</svg>"

            RETURN SVGCode
            """,
            language='dax',
        )

    st.markdown("---")

    # --- 2. OKR: Flecha de Tendencia (HTML Condicional) ---
    st.subheader("2. OKR: Flecha de Tendencia (Evaluación de Progreso)")
    
    col_code_2, col_business_2 = st.columns(2)
    
    with col_business_2:
        st.markdown("#### 🎯 Aplicación KPI/OKR")
        st.markdown(
            """
            * **KPI:** Variación de Ingresos Mes-sobre-Mes (MoM).
            * **OKR:** Objetivo: Reducir la rotación de clientes. Resultado Clave (KR): Disminuir la tasa de cancelación MoM en un 5%.
            * **Uso:** Muestra instantáneamente si la tendencia es positiva (verde) o negativa (rojo) para evaluar el KR.
            """
        )
    
    with col_code_2:
        st.code(
            """
            // DAX: [Variación vs Mes Anterior] = DIVIDE([Actual] - [Anterior], [Anterior])
            VAR Variacion = [Variacion vs Mes Anterior]

            VAR IconoHTML = 
                SWITCH(
                    TRUE(),
                    Variacion > 0, "<span style='color: green; font-size: 16px;'>▲</span>", 
                    Variacion < 0, "<span style='color: red; font-size: 16px;'>▼</span>",  
                    "<span style='color: gray; font-size: 16px;'>—</span>"              
                )
                
            RETURN IconoHTML & " " & FORMAT(Variacion, "0.0%")
            """,
            language='dax'
        )

    st.markdown("---")
    
    # --- 3. KPI/OKR: Medidor Circular (Donut SVG) ---
    st.subheader("3. KPI: Medidor Circular (Visión 360 de un Objetivo)")
    
    col_code_3, col_business_3 = st.columns(2)

    with col_business_3:
        st.markdown("#### 🎯 Aplicación KPI/OKR")
        st.markdown(
            """
            * **KPI:** Porcentaje de Tareas Completadas (En proyectos/IT).
            * **Uso:** Excelente para tarjetas de resumen que necesitan mostrar el progreso visual hacia un hito fijo (Ej: 85% del proyecto completado).
            """
        )
    
    with col_code_3:
        st.code(
            """
            // DAX: [Progreso %] es el valor (0 a 1)
            VAR Valor = ROUND([Progreso %], 2)
            VAR Radio = 30 
            VAR Circunferencia = 2 * PI() * Radio
            VAR DashOffset = Circunferencia * (1 - Valor)
            
            VAR SVGCode =
                "<svg width='100' height='70'>" &
                // ... (Círculo de fondo y círculo de progreso dinámico) ...
                "<circle r='" & Radio & "' cx='50' cy='35' fill='transparent' stroke='lightgray' stroke-width='8' />" &
                "<circle r='" & Radio & "' cx='50' cy='35' fill='transparent' stroke='dodgerblue' stroke-width='8' stroke-dashoffset='" & DashOffset & "' transform='rotate(-90 50 35)' />" &
                // ... (Texto) ...
                "</svg>"

            RETURN SVGCode
            """,
            language='dax'
        )

st.markdown("---")
st.success("¡La guía completa con pasos de implementación y ejemplos KPI/OKR está lista!")
