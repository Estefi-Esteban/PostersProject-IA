import streamlit as st
from sentence_transformers import SentenceTransformer, util
from PIL import Image

# 1. Configuración de página
st.set_page_config(page_title="Poster Match Pro", page_icon="🎞️", layout="wide")

# 2. CSS
st.markdown("""
    <style>
    [data-testid="stImage"] img {
        border-radius: 6px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        transition: transform 0.2s ease;
    }
    [data-testid="stImage"] img:hover {
        transform: scale(1.05);
    }
    .grupo-box {
        background-color: #1e1e2f;
        padding: 10px 15px;
        border-radius: 8px;
        border-left: 4px solid #a855f7; /* Morado para familias */
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .unico-box {
        background-color: #1a202c;
        padding: 10px 15px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6; /* Azul para únicos */
        margin-top: 30px;
        margin-bottom: 15px;
    }
    /* Clases para las etiquetas encima de las fotos */
    .badge-clon {
        color: #4ade80;
        font-weight: bold;
        font-size: 13px;
        text-align: center;
        margin-bottom: 2px;
    }
    .badge-variante {
        color: #fb923c;
        font-weight: bold;
        font-size: 13px;
        text-align: center;
        margin-bottom: 2px;
    }
    [data-testid="caption"] {
        font-size: 11px !important;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def cargar_modelo():
    return SentenceTransformer('clip-ViT-B-32')

modelo = cargar_modelo()

st.title("🎞️ Analizador Visual de Pósters")
st.markdown("Clasifica campañas enteras: agrupa familias visuales, detecta **clones exactos** y separa las **composiciones únicas**.")
st.divider()

archivos_subidos = st.file_uploader(
    "📥 Arrastra aquí todos los pósters", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if archivos_subidos and len(archivos_subidos) >= 2:
    if st.button("🚀 Procesar Campaña", type="primary"):
        
        with st.spinner("🧠 Analizando topología visual y buscando clones..."):
            imagenes = [Image.open(archivo) for archivo in archivos_subidos]
            nombres = [archivo.name for archivo in archivos_subidos]
            
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
                        if matriz_similitud[i][j].item() >= 0.80: 
                            grupo_actual.append(j)
                            visitados.add(j)
                    
                    if len(grupo_actual) > 1:
                        grupos.append(grupo_actual)

            # --- IDENTIFICAR PÓSTERS ÚNICOS ---
            indices_agrupados = set([idx for grupo in grupos for idx in grupo])
            indices_unicos = [i for i in range(len(nombres)) if i not in indices_agrupados]

        # 5. Dashboard
        st.success("✅ Análisis completado")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Analizados", len(archivos_subidos))
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
                    for otro_idx in grupo:
                        if img_idx != otro_idx and matriz_similitud[img_idx][otro_idx].item() >= 0.98:
                            es_clon = True
                            break
                    
                    with cols[i % 6]:
                        if es_clon:
                            st.markdown("<p class='badge-clon'>🟢 Clon Exacto</p>", unsafe_allow_html=True)
                        else:
                            st.markdown("<p class='badge-variante'>🟠 Variante</p>", unsafe_allow_html=True)
                            
                        st.image(imagenes[img_idx], caption=nombres[img_idx], use_container_width=True)

        # 7. Renderizado de Pósters Únicos
        if indices_unicos:
            st.markdown(f"<div class='unico-box'><h4>⭐ Composiciones Únicas</h4><p style='font-size:13px; margin:0;'>No tienen variantes similares en este lote (Similitud < 80%).</p></div>", unsafe_allow_html=True)
            
            cols_unicos = st.columns(6)
            for i, img_idx in enumerate(indices_unicos):
                with cols_unicos[i % 6]:
                    st.image(imagenes[img_idx], caption=nombres[img_idx], use_container_width=True)

elif archivos_subidos and len(archivos_subidos) < 2:
    st.warning("⚠️ Sube al menos 2 imágenes para realizar la comparativa.")