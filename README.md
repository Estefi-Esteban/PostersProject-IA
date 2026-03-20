# 🎞️ Poster Match (PostersProject-IA)

Un analizador visual híbrido diseñado para clasificar campañas publicitarias, detectar pósters duplicados y agrupar variantes visuales. Utiliza una combinación de algoritmos tradicionales (pHash) e Inteligencia Artificial (CLIP) para limpiar y organizar directorios de imágenes masivos.

## 🚀 Características Principales

Este proyecto se divide en dos módulos principales:

* **`app.py` (Dashboard Visual):** Una interfaz web interactiva construida con Streamlit. Permite subir imágenes sueltas o archivos `.ZIP`, ajustar los parámetros de tolerancia en tiempo real y visualizar de forma gráfica las "familias visuales" y los pósters únicos.
* **`core.py` (Motor de Producción):** Un script *headless* (sin interfaz) diseñado para procesar carpetas enteras de forma masiva. Ideal para automatizar la limpieza de archivos, conservando solo la imagen de mayor calidad (resolución) por cada grupo de duplicados/variantes.

## 🧠 ¿Cómo funciona el Filtro Híbrido?

El sistema analiza las imágenes en dos fases para optimizar rendimiento y precisión:

1.  **Fase 1: La Barredora (pHash):** Busca clones exactos o imágenes con variaciones minúsculas (compresión, pequeños recortes). Es muy rápido y descarta la "basura" evidente.
2.  **Fase 2: El Ojo Clínico (IA - CLIP):** Utiliza el modelo `clip-ViT-B-32` de OpenAI (vía `sentence-transformers`) para "entender" la composición de la imagen. Agrupa variantes (por ejemplo, el mismo póster pero con textos en distintos idiomas o ligeros cambios de diseño).

## 🛠️ Instalación

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/Estefi-Esteban/PostersProject-IA]
   cd PostersProject-IA

2. Crea un entorno virtual e instala las dependencias. Puedes usar el método tradicional con Python o la alternativa ultrarrápida con uv:

    **Opción A: Python tradicional (venv + pip)**
    ```bash
    python -m venv venv 
    source venv\Scripts\activate
    ```

    **Opción B: Usando uv (Recomendado por velocidad)**
    
    Requiere tener [uv](https://docs.astral.sh/uv/) instalado. Puedes instalarlo con:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    Una vez instalado, sincroniza las dependencias del proyecto:
    ```bash
    uv sync
    ```
    Esto creará automáticamente el entorno virtual y descargará todas las dependencias.

---

## 💻 Uso
El proyecto tiene dos formas de ejecutarse dependiendo de lo que necesites hacer:

**1. Interfaz Gráfica (Dashboard)**
Para visualizar el análisis, ajustar parámetros en tiempo real y subir archivos ZIP o sueltos:

```bash
# Con el entorno virtual activado (Opción A)
streamlit run app.py

# Con uv (Opción B)
uv run streamlit run app.py
```
Se abrirá una pestaña en tu navegador web automáticamente.


**2. Script de Limpieza Masiva (Terminal)**
Si solo quieres limpiar una carpeta de forma automática conservando los archivos de mayor calidad:

```bash
# Con el entorno virtual activado (Opción A)
python core.py

# Con uv (Opción B)
uv run python core.py
```

**Nota:** Al ejecutar core.py por primera vez, se creará automáticamente una carpeta llamada posters en la raíz del proyecto. Solo tienes que meter tus imágenes ahí dentro y volver a ejecutar el script.

---

## 📂 Estructura del Proyecto
```text
PostersProject-IA/
│
├── app.py               # Interfaz de usuario con Streamlit
├── core.py              # Lógica interna y ejecución por terminal
├── requirements.txt     # Dependencias del proyecto
├── .gitignore           # Archivos ignorados por Git
├── README.md            # Documentación
└── posters/             # (Se genera automáticamente) Carpeta de prueba
```

---