import os
import imagehash
from PIL import Image
from sentence_transformers import SentenceTransformer, util
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Singleton para evitar recargas constantes del modelo
_MODELO_IA = None

def get_model():
    global _MODELO_IA
    if _MODELO_IA is None:
        print("⏳ Cargando modelo de Inteligencia Artificial (CLIP)...")
        _MODELO_IA = SentenceTransformer('clip-ViT-B-32')
    return _MODELO_IA

def limpiar_carpeta_hibrido(ruta_carpeta, limite_phash=3, umbral_ia=0.92, min_width=800):
    """
    Algoritmo de producción para procesar masivamente sin interfaz.
    Arquitectura CLUSTER-FIRST: Filtro de tamaño -> Agrupación Semántica (CLIP) -> Limpieza Clones (pHash)
    """
    modelo = get_model()
    archivos = [f for f in os.listdir(ruta_carpeta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if len(archivos) <= 1:
        return archivos

    # ==========================================
    # FASE 0: CARGAR Y FILTRAR POR TAMAÑO MÍNIMO
    # ==========================================
    print(f"\n📏 Fase 0 (Tamaño): Descartando imágenes pequeñas (width < {min_width}px)...")
    posters = []
    for archivo in archivos:
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        try:
            img = Image.open(ruta_completa).convert('RGB')
            if img.width >= min_width:
                posters.append({
                    'archivo': archivo,
                    'ruta': ruta_completa,
                    'resolucion': img.width * img.height,
                    'img': img
                })
            else:
                print(f"   🗑️ Descartado por resolución baja ({img.width}x{img.height}): {archivo}")
        except Exception as e:
            print(f"⚠️ Error leyendo {archivo}: {e}")
            
    # CRÍTICO: Ordenar descendentemente por resolución para que el "Líder" de cualquier grupo
    # siempre sea matemáticamente la imagen de mayor calidad.
    posters.sort(key=lambda x: x['resolucion'], reverse=True)

    if not posters:
        msg = "   ⚠️ No hay imágenes que superen el filtro de tamaño."
        print(msg)
        return []

    # ==========================================
    # FASE 1: EL BIBLIOTECARIO (CLUSTERING CON CLIP)
    # ==========================================
    print(f"\n🧠 Fase 1 (IA): Clasificando {len(posters)} imágenes en grupos semánticos...")
    rutas = [p['ruta'] for p in posters]
    embeddings = modelo.encode(rutas, convert_to_numpy=True)

    clusters = []
    asignados = set()

    for i in range(len(posters)):
        if i in asignados: continue
        
        # El elemento i crea un "Nuevo Grupo" y es su Líder (es el de mayor resolución no asignado)
        nuevo_cluster = [posters[i]]
        asignados.add(i)
        
        for j in range(i + 1, len(posters)):
            if j in asignados: continue
            
            similitud = util.cos_sim(embeddings[i], embeddings[j]).item()
            if similitud >= umbral_ia:
                nuevo_cluster.append(posters[j])
                asignados.add(j)
                print(f"   🔗 Variante Enlazada [Similitud: {similitud:.4f}]:\n      ➡️ {posters[j]['archivo']}\n      ⬇️ Al líder: {posters[i]['archivo']}")
                
        clusters.append(nuevo_cluster)

    print(f"\n📊 Resultado Fase 1: Se han montado {len(clusters)} conceptos de diseño distintos.")

    print("\n--- RESUMEN DE CÚMULOS VISUALES ---")
    for idx, grupo in enumerate(clusters):
        print(f"📦 Familia {idx + 1} ({len(grupo)} imágenes) - Líder: {grupo[0]['archivo']}")
        for p in grupo[1:]:
            print(f"   ├─ {p['archivo']}")
    print("-----------------------------------")

    # ==========================================
    # FASE 2: EL LIMITADOR DE CLONES (pHash)
    # ==========================================
    print("\n🧹 Fase 2 (pHash): Eliminando clones idénticos dentro de cada grupo...")
    posters_finales = []

    for idx, grupo in enumerate(clusters):
        lider = grupo[0] # El de mayor resolución siempre es el índice 0
        hashes_vistos = [{'hash': imagehash.phash(lider['img']), 'archivo': lider['archivo']}]
        posters_finales.append(lider)
        
        for p in grupo[1:]:
            hash_actual = imagehash.phash(p['img'])
            es_clon = False
            distancia_min = 999
            clon_de = ""
            
            for hv in hashes_vistos:
                dist = abs(hash_actual - hv['hash'])
                if dist < distancia_min:
                    distancia_min = dist
                    clon_de = hv['archivo']
                if dist <= limite_phash:
                    es_clon = True
                    break
            
            if not es_clon:
                # Es una variante válida (p. ej. la versión sin texto del mismo diseño)
                hashes_vistos.append({'hash': hash_actual, 'archivo': p['archivo']})
                posters_finales.append(p)
            else:
                print(f"   🗑️ Grupo {idx+1} | Eliminado CLON EXACTO [Distancia pHash: {distancia_min}]:\n      🚫 {p['archivo']}\n      ✅ Es idéntico a: {clon_de}")

    print("-" * 40)
    print(f"✅ Resultado final: De {len(archivos)} archivos iniciales, se conservan {len(posters_finales)} imágenes ÚNICAS de máxima calidad.")
    return [p['archivo'] for p in posters_finales]
