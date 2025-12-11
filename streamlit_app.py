import streamlit as st

# --- Configuración de la Página ---
st.set_page_config(page_title="Guía: HTML Content en Power BI", layout="wide")

st.title("💡 Visualizador HTML Content en Power BI")
st.header("Convierte Medidas DAX en Visualizaciones Dinámicas (HTML/SVG)")

st.markdown(
    """
    El visualizador **HTML Content** (generalmente un visualizador personalizado como 'HTML Viewer' o el visualizador 'Text Filter' con la capacidad HTML activada) permite inyectar código HTML, CSS y SVG directamente en un informe de Power BI. 
    Esto es crucial para crear visualizaciones personalizadas que DAX, por sí solo, no puede generar (ej. iconos, medidores, semáforos, barras de progreso dentro de una tabla).
    """
)

st.markdown("---")

# --- Definición de Pestañas ---

tab1, tab2, tab3 = st.tabs(["1. ¿Qué es y Cómo Funciona?", "2. Aplicación y Código DAX", "3. Ejemplos Prácticos (SVG/HTML)"])

# ----------------------------------------------------------------------
# PESTAÑA 1: Conceptos
# ----------------------------------------------------------------------
with tab1:
    st.subheader("¿Qué es el Visualizador HTML Content?")
    st.markdown(
        """
        Es un visualizador personalizado (no nativo de Microsoft) que interpreta código HTML que se le pasa como una cadena de texto.
        
        * **Propósito:** Superar las limitaciones de formato y visualización de las tarjetas o tablas estándar de Power BI.
        * **Contenido Aceptado:** HTML, CSS y, fundamentalmente, código **SVG (Scalable Vector Graphics)** para dibujar gráficos dinámicos.
        """
    )

    st.subheader("Mecanismo Clave: DAX como Generador de Código")
    st.markdown(
        """
        El funcionamiento se basa en generar una *única medida DAX* cuyo resultado no es un número o texto simple, sino una **cadena de código HTML o SVG completa**.
        
        1.  **Cálculo DAX:** Se utiliza DAX para calcular valores, realizar comparaciones (`IF`, `SWITCH`), y determinar colores o tamaños.
        2.  **Concatenación:** El resultado del cálculo se concatena con etiquetas HTML/SVG como `<div>`, `<svg>`, `<rect>`, usando `CONCATENATEX` o `&`.
        3.  **Visualización:** El visualizador HTML Content toma esa cadena de código DAX (ej., `'<div style="color: red;">' & [Mi Medida] & '</div>'`) y lo renderiza como un elemento visual en la página.
        """
    )
    
    st.markdown("---")
    st.subheader("Requisitos Previos")
    st.warning("Necesitas descargar e importar un visualizador personalizado de HTML Content desde AppSource de Microsoft (por ejemplo, 'HTML Viewer').")


# ----------------------------------------------------------------------
# PESTAÑA 2: Aplicación y Código DAX
# ----------------------------------------------------------------------
with tab2:
    st.subheader("Pasos para la Aplicación en Power BI")
    
    st.markdown(
        """
        1.  **Importar Visualizador:** Importa el visualizador **HTML Content** (o similar) desde el mercado de AppSource.
        2.  **Crear Medida DAX:** Escribe una medida DAX que incluya el código HTML/SVG necesario. El código debe ser una **cadena de texto**.
        3.  **Colocar la Medida:** Arrastra esa medida DAX al campo principal del visualizador HTML Content.
        4.  **Configuración:** Asegúrate de que la configuración del visualizador esté activa para interpretar el HTML.
        """
    )
    
    st.subheader("Ejemplo Base de Medida DAX (Semáforo Condicional)")
    st.markdown("Este ejemplo utiliza DAX para decidir si el resultado es bueno, regular o malo y lo envuelve en un emoji/ícono.")
    
    st.code(
        """
        // 1. Definir la métrica base (asumimos que existe)
        VAR VentasActuales = [Total Ventas] 

        // 2. Definir los colores/símbolos basados en la métrica
        VAR ColorSemaforo = 
            SWITCH(
                TRUE(),
                VentasActuales >= 100000, "green",
                VentasActuales >= 50000, "orange",
                "red"
            )
        
        // 3. Generar el código HTML/SVG completo
        VAR IconoHTML = 
            "<span style='font-size: 20px; color: " & ColorSemaforo & ";'>&#9679;</span>" // Emoji círculo

        // 4. Concatenar el icono con el valor
        RETURN
            IconoHTML & " " & FORMAT(VentasActuales, "$#,0")
        """,
        language='dax'
    )
    st.info("El resultado de esta medida es una única cadena de texto que el visualizador renderiza como un ícono de color seguido del valor.")

# ----------------------------------------------------------------------
# PESTAÑA 3: Ejemplos Prácticos (SVG/HTML)
# ----------------------------------------------------------------------
with tab3:
    st.header("Ejemplos Avanzados de Código para Power BI")
    st.markdown("Estos ejemplos son ideales para visualizaciones en Tablas o Matrices.")

    st.subheader("1. Barra de Progreso Dinámica (SVG)")
    st.markdown("Útil para mostrar el progreso de una métrica hacia un objetivo dentro de una tabla. El ancho de la barra es dinámico.")
    
    st.code(
        """
        // DAX: Asumimos que [Progreso %] existe (ej: DIVIDE([Actual], [Meta]))
        VAR Progreso = ROUND([Progreso %] * 100, 0) // Valor entre 0 y 100
        VAR ColorBarra = IF(Progreso >= 100, "teal", "dodgerblue")

        VAR SVGCode =
            "<svg width='100%' height='15'>" & 
            // Barra de fondo gris
            "<rect width='100%' height='100%' fill='#cccccc' rx='3' ry='3' />" &
            // Barra de progreso dinámica
            "<rect width='" & Progreso & "%' height='100%' fill='" & ColorBarra & "' rx='3' ry='3' />" &
            // Texto (opcional)
            "<text x='50%' y='60%' dominant-baseline='middle' text-anchor='middle' font-size='10' fill='white'>" & 
            Progreso & "%" & 
            "</text>" &
            "</svg>"

        RETURN SVGCode
        """,
        language='dax',
        
    )
    st.warning("Debes colocar la medida `SVGCode` en el campo de un visualizador HTML Content, y luego usar ese visualizador en tu matriz.")

    st.subheader("2. Medidor Circular Simple (Donut SVG)")
    st.markdown("Una visualización de KPI simple que utiliza SVG para dibujar un círculo parcial, ideal para una tarjeta o una matriz con pocos elementos.")
    
    st.code(
        """
        // DAX: Medida para el valor a mostrar (0 a 100%)
        VAR Valor = ROUND([Progreso %], 2)
        VAR Radio = 30
        VAR Circunferencia = 2 * PI() * Radio
        VAR DashOffset = Circunferencia * (1 - Valor)
        VAR ColorStroke = IF(Valor >= 0.8, "green", "red")

        VAR SVGCode =
            "<svg width='100' height='70'>" &
            // Círculo de fondo (gris)
            "<circle r='" & Radio & "' cx='50' cy='35' fill='transparent' stroke='lightgray' stroke-width='8' />" &
            // Círculo de progreso (dinámico)
            "<circle r='" & Radio & "' cx='50' cy='35' fill='transparent' stroke='" & ColorStroke & 
            "' stroke-width='8' stroke-dasharray='" & Circunferencia & 
            "' stroke-dashoffset='" & DashOffset & "' transform='rotate(-90 50 35)' />" &
            // Texto del porcentaje
            "<text x='50' y='35' text-anchor='middle' font-size='12' fill='#333333'>" & 
            FORMAT(Valor, "0%") & 
            "</text>" &
            "</svg>"

        RETURN SVGCode
        """,
        language='dax'
    )
    
    st.subheader("3. HTML Condicional (Icono de Tendencia)")
    st.markdown("Usando HTML puro y etiquetas `<span>` para mostrar iconos de flechas basados en una variación.")
    
    st.code(
        """
        // DAX: Medida de variación, ej. [Variación vs Mes Anterior]
        VAR Variacion = [Variacion vs Mes Anterior]

        VAR IconoHTML = 
            SWITCH(
                TRUE(),
                Variacion > 0, "<span style='color: green; font-size: 16px;'>▲</span>", // Flecha arriba
                Variacion < 0, "<span style='color: red; font-size: 16px;'>▼</span>",  // Flecha abajo
                "<span style='color: gray; font-size: 16px;'>—</span>"              // Guión
            )
            
        RETURN IconoHTML & " " & FORMAT(Variacion, "0.0%")
        """,
        language='dax'
    )

st.markdown("---")
st.success("¡Ahora tienes la base conceptual y ejemplos de código DAX/SVG listos para probar con el visualizador HTML Content en Power BI!")
