# 🎞️ Poster Match (PostersProject-IA)

Un analizador visual híbrido diseñado para clasificar campañas publicitarias, detectar pósters duplicados y agrupar variantes visuales. Utiliza una combinación de algoritmos tradicionales (pHash) e Inteligencia Artificial (CLIP) para limpiar y organizar directorios de imágenes masivos.

## 🚀 Características Principales

Este proyecto se divide en dos módulos principales integrados en una arquitectura modular:

*   **Dashboard Visual (Streamlit):** Interfaz interactiva para subir imágenes sueltas o archivos `.ZIP`, ajustar parámetros y visualizar "familias visuales".
*   **Motor de Análisis (Engine):** Lógica centralizada para procesar carpetas masivas, conservando solo la imagen de mayor calidad por cada grupo.

## 🧠 ¿Cómo funciona el Filtro Híbrido?

1.  **Fase 1: La Barredora (pHash):** Busca clones exactos o imágenes con variaciones minúsculas.
2.  **Fase 2: El Ojo Clínico (IA - CLIP):** Utiliza `clip-ViT-B-32` para entender la composición y agrupar variantes (misma temática, distinto texto o diseño).

## 🛠️ Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/Estefi-Esteban/PostersProject-IA
    cd PostersProject-IA
    ```

2.  **Configurar entorno con [uv](https://docs.astral.sh/uv/) (Recomendado):**
    ```bash
    uv sync
    ```

---

## 💻 Uso (Nueva Estructura)

### 1. Interfaz Gráfica (Dashboard)
Para visualizar el análisis y subir archivos:
```bash
uv run streamlit run src/web/app.py
```

### 2. Limpieza Masiva (Terminal)
Para limpiar automáticamente la carpeta de imágenes configurada:
```bash
uv run python scripts/run_cleanup.py
```

**Nota:** Por defecto, el script busca imágenes en `data/posters/`. Si la carpeta no existe, el script la creará por ti.

---

## 📂 Estructura del Proyecto (Senior)
```text
PostersProject-IA/
├── data/
│   └── posters/          # Carpeta para tus imágenes (Input)
├── scripts/
│   └── run_cleanup.py    # Punto de entrada para ejecución CLI
├── src/
│   ├── core/
│   │   ├── analyzer.py   # Motor de análisis (Lógica)
│   │   └── paths.py      # Gestión centralizada de rutas
│   └── web/
│       └── app.py        # Interfaz de usuario (Streamlit)
├── pyproject.toml
├── README.md
└── .gitignore
```

---