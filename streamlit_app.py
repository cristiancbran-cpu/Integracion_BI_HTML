import streamlit as st

# --- Configuración de la Página ---
st.set_page_config(page_title="Guía: HTML Content en Power BI", layout="wide")

st.title("💡 Visualizador HTML Content en Power BI")
st.header("Convierte Medidas DAX en Visualizaciones Dinámicas (HTML/SVG)")

st.markdown(
    """
    El visualizador **HTML Content** (generalmente un visualizador personalizado) permite inyectar código HTML, CSS y SVG directamente en un informe de Power BI para crear visualizaciones personalizadas.
    """
)

st.markdown("---")

# --- Definición de Pestañas ---

tab1, tab2, tab3 = st.tabs(["1. ¿Qué es y Cómo Funciona?", "2. Aplicación y Código DAX", "3. Ejemplos Prácticos (SVG/HTML)"])

# ----------------------------------------------------------------------
# PESTAÑA 1: Conceptos (Sin cambios significativos)
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
        El funcionamiento se basa en generar una *única medida DAX* cuyo resultado es una **cadena de código HTML o SVG completa**.
        
        1.  **Cálculo DAX:** Se utiliza DAX para calcular valores, realizar comparaciones.
        2.  **Concatenación:** El resultado del cálculo se concatena con etiquetas HTML/SVG.
        3.  **Visualización:** El visualizador HTML Content toma esa cadena de código DAX y la renderiza.
        """
    )
    
    st.markdown("---")
    st.subheader("Requisitos Previos")
    st.warning("Necesitas descargar e importar un visualizador personalizado de HTML Content desde AppSource de Microsoft.")


# ----------------------------------------------------------------------
# PESTAÑA 2: Aplicación y Código DAX (Añadido Visual Conceptual)
# ----------------------------------------------------------------------
with tab2:
    st.subheader("Pasos para la Aplicación en Power BI")
    # ... (Pasos de aplicación sin cambios) ...
    st.markdown(
        """
        1.  **Importar Visualizador:** Importa el visualizador **HTML Content** (o similar) desde el mercado de AppSource.
        2.  **Crear Medida DAX:** Escribe una medida DAX que incluya el código HTML/SVG necesario.
        3.  **Colocar la Medida:** Arrastra esa medida DAX al campo principal del visualizador HTML Content.
        4.  **Configuración:** Asegúrate de que la configuración del visualizador esté activa para interpretar el HTML.
        """
    )
    
    st.subheader("Ejemplo Base de Medida DAX (Semáforo Condicional)")
    st.markdown("El código DAX decide el color y el valor a mostrar.")
    
    col_code, col_visual = st.columns(2)

    with col_code:
        st.code(
            """
            // Medida que genera el círculo de color y el valor
            VAR VentasActuales = [Total Ventas] 
            VAR ColorSemaforo = 
                SWITCH(
                    TRUE(),
                    VentasActuales >= 100000, "green",
                    VentasActuales >= 50000, "orange",
                    "red"
                )
            VAR IconoHTML = 
                "<span style='font-size: 20px; color: " & ColorSemaforo & ";'>&#9679;</span>"
            
            RETURN
                IconoHTML & " " & FORMAT(VentasActuales, "$#,0")
            """,
            language='dax'
        )
    
    with col_visual:
        st.markdown("#### ✨ Visual en Power BI (Conceptual)")
        st.markdown("Si [Total Ventas] fuera **$120,000**:")
        st.markdown(
            """
            <div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px; background-color: #f9f9f9;'>
                <span style='font-size: 20px; color: green;'>&#9679;</span> 
                <span style='font-size: 16px; font-weight: bold;'>$120,000</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("Si [Total Ventas] fuera **$30,000**:")
        st.markdown(
            """
            <div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px; background-color: #f9f9f9;'>
                <span style='font-size: 20px; color: red;'>&#9679;</span> 
                <span style='font-size: 16px; font-weight: bold;'>$30,000</span>
            </div>
            """,
            unsafe_allow_html=True
        )


# ----------------------------------------------------------------------
# PESTAÑA 3: Ejemplos Prácticos (Añadido Visual Conceptual)
# ----------------------------------------------------------------------
with tab3:
    st.header("Ejemplos Avanzados de Código para Power BI")

    # --- 1. Barra de Progreso ---
    st.subheader("1. Barra de Progreso Dinámica (SVG)")
    st.markdown("Útil para mostrar el progreso de una métrica hacia un objetivo dentro de una tabla.")
    
    col_code_1, col_visual_1 = st.columns(2)
    
    with col_code_1:
        st.code(
            """
            // DAX: Asumimos que [Progreso %] existe (ej: 0.75)
            VAR Progreso = ROUND([Progreso %] * 100, 0)
            VAR ColorBarra = IF(Progreso >= 100, "teal", "dodgerblue")

            VAR SVGCode =
                "<svg width='100%' height='15'>" & 
                // Barra de fondo gris
                "<rect width='100%' height='100%' fill='#cccccc' rx='3' ry='3' />" &
                // Barra de progreso dinámica
                "<rect width='" & Progreso & "%' height='100%' fill='" & ColorBarra & "' rx='3' ry='3' />" &
                // Texto
                "<text x='50%' y='60%' dominant-baseline='middle' text-anchor='middle' font-size='10' fill='white'>" & 
                Progreso & "%" & 
                "</text>" &
                "</svg>"

            RETURN SVGCode
            """,
            language='dax',
        )
    
    with col_visual_1:
        st.markdown("#### ✨ Visual en Power BI (Conceptual)")
        st.markdown("Si [Progreso %] fuera **75%**:")
        # Renderizado conceptual de la barra (usando HTML/CSS para simular SVG)
        st.markdown(
            """
            <div style="background-color: #cccccc; height: 15px; width: 100%; border-radius: 3px;">
                <div style="width: 75%; background-color: dodgerblue; height: 100%; border-radius: 3px; position: relative; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-size: 10px; font-weight: bold;">75%</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # --- 2. HTML Condicional (Icono de Tendencia) ---
    st.subheader("2. HTML Condicional (Icono de Tendencia)")
    st.markdown("Usando HTML puro y etiquetas `<span>` para mostrar iconos de flechas basados en una variación.")
    
    col_code_3, col_visual_3 = st.columns(2)
    
    with col_code_3:
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
    
    with col_visual_3:
        st.markdown("#### ✨ Visual en Power BI (Conceptual)")
        st.markdown("Si [Variacion] fuera **+5.2%**:")
        st.markdown(
            """
            <div style='padding: 5px;'>
                <span style='color: green; font-size: 16px;'>▲</span> 
                <span style='font-size: 14px;'>5.2%</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("Si [Variacion] fuera **-1.9%**:")
        st.markdown(
            """
            <div style='padding: 5px;'>
                <span style='color: red; font-size: 16px;'>▼</span> 
                <span style='font-size: 14px;'>-1.9%</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    
    # --- 3. Medidor Circular Simple ---
    st.subheader("3. Medidor Circular Simple (Donut SVG)")
    st.markdown("Una visualización de KPI simple que utiliza SVG para dibujar un círculo parcial, ideal para una tarjeta.")
    
    col_code_2, col_visual_2 = st.columns(2)

    with col_code_2:
        st.code(
            """
            // DAX: Medida para el valor a mostrar (0 a 100%)
            VAR Valor = ROUND([Progreso %], 2)
            VAR Radio = 30
            // ... (Cálculo de SVG Code con stroke-dashoffset) ...
            
            VAR SVGCode = // CÓDIGO SVG CONCATENADO
                // ... (código que dibuja el círculo) ...
                "..." 
                // ...
            
            RETURN SVGCode
            """,
            language='dax'
        )
    
    with col_visual_2:
        st.markdown("#### ✨ Visual en Power BI (Conceptual)")
        st.markdown("Si [Progreso %] fuera **85%**:")
        # Renderizado conceptual del círculo (usando HTML/CSS para simular SVG)
        st.markdown(
            """
            <div style="width: 70px; height: 70px; border-radius: 50%; background: radial-gradient(closest-side, white 65%, transparent 65% 100%), conic-gradient(green 85%, lightgray 0);">
                <span style="position: relative; top: 40%; left: 35%; font-size: 14px; font-weight: bold;">85%</span>
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown("---")
st.success("¡La guía está completa! Ahora tienes el código DAX y la representación visual de cómo se verá el resultado en Power BI.")
