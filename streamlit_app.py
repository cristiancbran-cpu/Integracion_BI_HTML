import streamlit as st
import os
from dotenv import load_dotenv

# Importaciones de LangChain, ahora modulares
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader

# Corregido: La función 'create_stuff_documents_chain' DEBE importarse desde su ruta completa.
# Es la única que suele requerir la ruta larga.
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

import tempfile
# ... el resto del código ...

# Cargar variables de entorno (para desarrollo local)
load_dotenv()

# --- Configuración de Streamlit ---
st.set_page_config(page_title="Asistente DAX y Visualización para Power BI", layout="wide")
st.title("📊 Asistente de Power BI (DAX & Visualización)")
st.caption("Sube la estructura de tus datos (tablas/columnas) y pregunta sobre medidas DAX o código de visualización (HTML/SVG).")

# ----------------------------------------------------
# PASO 1: Vincular la Clave de API (Opción más segura)
# ----------------------------------------------------
api_key = os.getenv("GOOGLE_API_KEY") 

if not api_key:
    with st.sidebar:
        st.warning("⚠️ Introduce tu clave de API de Gemini para continuar.")
        api_key_input = st.text_input("Clave de API de Google Gemini", type="password")
    
    if api_key_input:
        api_key = api_key_input
    else:
        st.info("Introduce la clave de API en la barra lateral.")
        st.stop()

os.environ["GOOGLE_API_KEY"] = api_key

# --- Funciones de RAG ---

def process_documents(uploaded_file):
    """
    Carga el archivo (estructura de datos), lo divide y crea un vector store.
    """
    if uploaded_file is None:
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_file_path = tmp_file.name

    try:
        # Intentar determinar el cargador basado en la extensión
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext in ['txt', 'md']:
            loader = TextLoader(temp_file_path, encoding="utf-8")
        elif ext == 'csv':
            # CSVLoader necesita saber la columna de texto a usar, por defecto lo usa todo
            loader = CSVLoader(temp_file_path, encoding="utf-8")
        else:
            st.error(f"Tipo de archivo no soportado ({ext}). Por favor, usa TXT, MD o CSV.")
            os.remove(temp_file_path)
            return None
        
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
        )
        texts = text_splitter.split_documents(documents)

        # Crear Embeddings y Vector Store
        embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004") 
        vectorstore = Chroma.from_documents(texts, embeddings)
        
        os.remove(temp_file_path)
        
        return vectorstore.as_retriever()
        
    except Exception as e:
        st.error(f"Error al procesar el documento: {e}")
        if os.path.exists(temp_file_path):
             os.remove(temp_file_path)
        return None


def get_rag_chain(retriever):
    """
    Crea la cadena RAG para generar el código DAX o la visualización.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    
    # Prompt de sistema especializado para Power BI
    system_prompt = (
        "Eres un experto consultor de Power BI. Tu tarea es generar código (DAX, HTML o SVG) "
        "o dar consejos de visualización SOLAMENTE basándote en la ESTRUCTURA DE TABLAS proporcionada. "
        "Cuando el usuario pida una MEDIDA, genera el código DAX completo. "
        "Cuando el usuario pida un CÓDIGO DE VISUALIZACIÓN (HTML o SVG), genera solo el código, "
        "pero advierte que debe usarse con una medida DAX que concatene el resultado. "
        "Asegúrate de que las referencias a tablas y columnas (ej. 'Tabla[Columna]') sean sintácticamente correctas. "
        "\n\nContexto de la estructura de datos: \n{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    # Esta cadena no necesita historial de chat, solo la pregunta y el contexto de los datos.
    return create_retrieval_chain(retriever, document_chain)


# --- Lógica de la Aplicación Streamlit ---

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "processing_done" not in st.session_state:
    st.session_state.processing_done = False


# Sidebar para subir el archivo
with st.sidebar:
    st.header("1. Carga la Estructura de Datos")
    st.markdown("Copia y pega la estructura de tus tablas y columnas en un archivo **.txt** o sube un **.csv** representativo.")
    
    uploaded_file = st.file_uploader(
        "Sube archivo (.txt, .csv)",
        type=["txt", "csv", "md"],
        accept_multiple_files=False
    )
    
    if st.button("Procesar Estructura"):
        if uploaded_file:
            with st.spinner("Creando contexto de datos..."):
                retriever = process_documents(uploaded_file)
                if retriever:
                    st.session_state.rag_chain = get_rag_chain(retriever)
                    st.session_state.processing_done = True
                    st.success("¡Estructura de datos procesada! Ahora puedes preguntar en el panel principal.")
                else:
                    st.session_state.processing_done = False
        else:
            st.warning("Por favor, sube un archivo con la estructura de datos primero.")
    
    st.markdown("---")
    st.write("Impulsado por Gemini 2.5 Flash y RAG.")


# Panel principal
st.header("💬 Pregunta al Asistente")

if not st.session_state.processing_done:
    st.info("Sube la estructura de tus datos en la barra lateral para empezar.")
else:
    # Entrada de pregunta
    user_question = st.text_area(
        "Escribe aquí tu pregunta o solicitud (Ejemplos abajo):",
        placeholder="Ej: Necesito una medida DAX para calcular las ventas de los últimos 6 meses del contexto de [Ventas] y la columna [Fecha]."
    )
    
    if st.button("Generar Solución"):
        if user_question and st.session_state.rag_chain:
            with st.spinner("Gemini está generando el código..."):
                try:
                    # La cadena RAG invoca el LLM con la pregunta y el contexto de los datos
                    response = st.session_state.rag_chain.invoke({"input": user_question})
                    
                    # El resultado de create_retrieval_chain está en 'answer'
                    assistant_response = response["answer"]
                    
                    st.subheader("🛠️ Solución Generada")
                    st.markdown(assistant_response)

                except Exception as e:
                    st.error(f"Error al generar la respuesta: {e}")
        else:
            st.warning("Por favor, escribe una pregunta.")

    st.markdown("---")
    st.subheader("💡 Ejemplos de Solicitudes:")
    st.markdown(
        "* **DAX:** 'Crea la medida DAX de una cuenta acumulada de los ingresos de la tabla de Facturas a lo largo del tiempo.'\n"
        "* **Visualización (HTML/SVG):** 'Crea el código SVG para mostrar un semáforo (rojo, amarillo, verde) basado en si el valor es menor a 1000, entre 1000 y 5000, o mayor a 5000. Debe ser un código que se use en una medida DAX.'\n"
        "* **Consejo de Gráfico:** 'Con las columnas [Fecha], [Categoría de Producto] y [Ventas], ¿qué gráfico es mejor para visualizar la tendencia y la contribución de la categoría?'"
    )
