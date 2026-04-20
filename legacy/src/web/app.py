import streamlit as st
import imagehash
from sentence_transformers import util
from PIL import Image
import zipfile
import io

# Senior Imports
from src.core.analyzer import get_model
from src.core.paths import POSTERS_DIR

# 1. Configuración de página
st.set_page_config(page_title="Poster Match Pro", page_icon="🎞️", layout="wide")

# 2. CSS
st.markdown("""
    <style>
    [data-testid="stImage"] img { border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.3); transition: transform 0.2s ease; }
    [data-testid="stImage"] img:hover { transform: scale(1.05); }
    .grupo-box { background-color: #1e1e2f; padding: 10px 15px; border-radius: 8px; border-left: 4px solid #a855f7; margin-top: 10px; margin-bottom: 5px; }
    .unico-box { background-color: #1a202c; padding: 10px 15px; border-radius: 8px; border-left: 4px solid #3b82f6; margin-top: 30px; margin-bottom: 15px; }
    .badge-clon { color: #4ade80; font-weight: bold; font-size: 13px; text-align: center; margin-bottom: 2px; }
    .badge-variante { color: #fb923c; font-weight: bold; font-size: 13px; text-align: center; margin-bottom: 2px; }
    [data-testid="caption"] { font-size: 11px !important; text-align: center; word-wrap: break-word; }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_analysis_model():
    return get_model()

modelo = load_analysis_model()

# --- PANEL LATERAL DE CONTROL ---
st.sidebar.header("⚙️ Ajustes de Precisión")
limite_phash = st.sidebar.slider("Fase 1: Tolerancia pHash (Clones)", min_value=0, max_value=15, value=5, step=1)
umbral_ia = st.sidebar.slider("Fase 2: Similitud IA (Variantes)", min_value=0.70, max_value=0.99, value=0.94, step=0.01)

st.title("🎞️ Analizador Visual Híbrido")
st.markdown("Clasifica campañas: Sube imágenes sueltas o un **archivo ZIP** con tus carpetas.")
st.divider()

# 3. UPLOADER
archivos_subidos = st.file_uploader(
    "📥 Arrastra aquí tus pósters sueltos o un archivo .ZIP", 
    type=["jpg", "jpeg", "png", "zip"], 
    accept_multiple_files=True
)

if archivos_subidos:
    if st.button("🚀 Procesar Campaña", type="primary"):
        
        with st.spinner("🧠 Extrayendo archivos y aplicando Filtro Híbrido..."):
            imagenes = []
            nombres = []
            
            # --- LÓGICA DE EXTRACCIÓN (Imágenes sueltas y ZIPs) ---
            for archivo in archivos_subidos:
                if archivo.name.lower().endswith('.zip'):
                    with zipfile.ZipFile(archivo, 'r') as z:
                        for info_archivo in z.infolist():
                            if info_archivo.filename.lower().endswith(('.png', '.jpg', '.jpeg')) and '__MACOSX' not in info_archivo.filename:
                                try:
                                    img_data = z.read(info_archivo.filename)
                                    img = Image.open(io.BytesIO(img_data)).convert('RGB')
                                    imagenes.append(img)
                                    nombres.append(info_archivo.filename)
                                except Exception as e:
                                    st.warning(f"No se pudo leer la imagen {info_archivo.filename} del ZIP.")
                else:
                    imagenes.append(Image.open(archivo).convert('RGB'))
                    nombres.append(archivo.name)
            
            if len(imagenes) < 2:
                st.error("⚠️ Se necesitan al menos 2 imágenes válidas para comparar.")
                st.stop()

            # --- FASE 1: BARREDORA (pHash) ---
            hashes = [imagehash.phash(img) for img in imagenes]
            
            # --- FASE 2: OJO CLÍNICO (IA CLIP) ---
            embeddings = modelo.encode(imagenes)
            matriz_similitud = util.cos_sim(embeddings, embeddings)
            
            # --- ALGORITMO DE AGRUPACIÓN ---
            visitados = set()
            grupos = []
            
            for i in range(len(nombres)):
                if i not in visitados:
                    grupo_actual = [i]
                    visitados.add(i)
                    
                    for j in range(i + 1, len(nombres)):
                        if j not in visitados:
                            es_clon = abs(hashes[i] - hashes[j]) <= limite_phash
                            es_variante = matriz_similitud[i][j].item() >= umbral_ia
                            
                            if es_clon or es_variante:
                                grupo_actual.append(j)
                                visitados.add(j)
                    
                    if len(grupo_actual) > 1:
                        grupos.append(grupo_actual)

            # --- IDENTIFICAR PÓSTERS ÚNICOS ---
            indices_agrupados = set([idx for grupo in grupos for idx in grupo])
            indices_unicos = [i for i in range(len(nombres)) if i not in indices_agrupados]

        # 5. Dashboard
        st.success(f"✅ Análisis completado. Se procesaron {len(imagenes)} imágenes.")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Analizados", len(imagenes))
        col2.metric("Familias Detectadas", len(grupos))
        col3.metric("Pósters Únicos", len(indices_unicos))
        st.divider()

        # 6. Renderizado de Familias
        if grupos:
            for idx, grupo in enumerate(grupos):
                st.markdown(f"<div class='grupo-box'><h4>📁 Familia Visual {idx + 1}</h4></div>", unsafe_allow_html=True)
                
                cols = st.columns(6)
                for i, img_idx in enumerate(grupo):
                    es_clon = False
                    if i > 0 and abs(hashes[grupo[0]] - hashes[img_idx]) <= limite_phash:
                        es_clon = True
                    
                    with cols[i % 6]:
                        if es_clon:
                            st.markdown(f"<p class='badge-clon'>🟢 Clon Exacto</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p class='badge-variante'>🟠 Variante (IA)</p>", unsafe_allow_html=True)
                            
                        nombre_corto = nombres[img_idx].split('/')[-1] if '/' in nombres[img_idx] else nombres[img_idx]
                        st.image(imagenes[img_idx], caption=nombre_corto, use_container_width=True)

        # 7. Renderizado de Pósters Únicos
        if indices_unicos:
            st.markdown(f"<div class='unico-box'><h4>⭐ Composiciones Únicas</h4></div>", unsafe_allow_html=True)
            cols_unicos = st.columns(6)
            for i, img_idx in enumerate(indices_unicos):
                with cols_unicos[i % 6]:
                    nombre_corto = nombres[img_idx].split('/')[-1] if '/' in nombres[img_idx] else nombres[img_idx]
                    st.image(imagenes[img_idx], caption=nombre_corto, use_container_width=True)
