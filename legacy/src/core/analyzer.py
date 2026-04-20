import os
import imagehash
from PIL import Image
from sentence_transformers import SentenceTransformer, util
import warnings
from src.core.paths import POSTERS_DIR

warnings.filterwarnings("ignore", category=UserWarning)

# Singleton for the model to avoid re-loading
_MODELO_IA = None

def get_model():
    global _MODELO_IA
    if _MODELO_IA is None:
        print("⏳ Cargando modelo de IA (CLIP)...")
        _MODELO_IA = SentenceTransformer('clip-ViT-B-32')
    return _MODELO_IA

def limpiar_carpeta_hibrido(ruta_carpeta, limite_phash=5, umbral_ia=0.88):
    """
    Algoritmo de producción para procesar masivamente sin interfaz.
    Devuelve la lista de archivos definitivos que debes conservar.
    """
    modelo = get_model()
    
    if not os.path.exists(ruta_carpeta):
        print(f"⚠️ La carpeta {ruta_carpeta} no existe.")
        return []

    archivos = [f for f in os.listdir(ruta_carpeta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if len(archivos) <= 1:
        return archivos

    # 1. Cargar metadatos y ordenar por "Calidad" (Resolución)
    posters = []
    for archivo in archivos:
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        try:
            img = Image.open(ruta_completa)
            posters.append({
                'archivo': archivo,
                'ruta': ruta_completa,
                'resolucion': img.width * img.height,
                'img': img
            })
        except Exception as e:
            print(f"⚠️ Error leyendo {archivo}: {e}")
            
    posters.sort(key=lambda x: x['resolucion'], reverse=True)

    # ==========================================
    # FASE 1: LA BARREDORA (pHash) - Duplicados exactos
    # ==========================================
    print(f"\n🧹 Fase 1 (pHash): Analizando {len(posters)} imágenes...")
    sobrevivientes_fase1 = []
    hashes_vistos = []

    for p in posters:
        hash_actual = imagehash.phash(p['img'])
        es_duplicado = False
        for hv in hashes_vistos:
            if abs(hash_actual - hv) <= limite_phash:
                es_duplicado = True
                break
                
        if not es_duplicado:
            hashes_vistos.append(hash_actual)
            sobrevivientes_fase1.append(p)
        else:
            print(f"   🗑️ Descartado por pHash (Clon): {p['archivo']}")

    if len(sobrevivientes_fase1) <= 1:
        return [p['archivo'] for p in sobrevivientes_fase1]

    # ==========================================
    # FASE 2: EL OJO CLÍNICO (IA) - Variantes visuales
    # ==========================================
    print(f"🧠 Fase 2 (IA): Analizando los {len(sobrevivientes_fase1)} sobrevivientes...")
    posters_finales = []
    indices_descartados = set()
    
    rutas_fase2 = [p['ruta'] for p in sobrevivientes_fase1]
    embeddings = modelo.encode(rutas_fase2, convert_to_numpy=True)

    for i in range(len(sobrevivientes_fase1)):
        if i in indices_descartados: continue
        
        posters_finales.append(sobrevivientes_fase1[i])
        
        for j in range(i + 1, len(sobrevivientes_fase1)):
            if j in indices_descartados: continue
            
            similitud = util.cos_sim(embeddings[i], embeddings[j]).item()
            if similitud >= umbral_ia:
                indices_descartados.add(j)
                print(f"   🗑️ Descartado por IA (Variante): {sobrevivientes_fase1[j]['archivo']}")

    print("-" * 40)
    print(f"✅ Resultado final: De {len(posters)} pósters, nos quedamos con {len(posters_finales)}")
    return [p['archivo'] for p in posters_finales]

if __name__ == "__main__":
    # Test execution using standard data directory
    definitivos = limpiar_carpeta_hibrido(str(POSTERS_DIR))
    print(f"\n🌟 ARCHIVOS A CONSERVAR EN {POSTERS_DIR}: {definitivos}")
