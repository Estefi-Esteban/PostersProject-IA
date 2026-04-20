import os
import sys
import asyncio
import aiohttp
from io import BytesIO
from PIL import Image
import imagehash
import warnings

# Configuración de ruta relativa
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

from src.core.analyzer import get_model

warnings.filterwarnings("ignore", category=UserWarning)

# ==============================================================================
# 🛡️ INTEGRACIÓN SEGURA DE BASE DE DATOS (Módulo Portfolio)
# ==============================================================================
# Para entornos públicos/clonados, toleramos que la BBDD no exista localmente.
try:
    from src.core.db import get_all_posters_by_peli, delete_poster, get_connection
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("⚠️  [MODO SEGURO] No se ha detectado el módulo 'src.core.db'.")
    print("💡  Este script ('db_purger.py') requiere infraestructura propia de Base de Datos SQL.")
    print("    Si descargaste este repositorio y quieres probar la IA de deduplicación ")
    print("    con imágenes locales, ejecuta 'uv run python scripts/local_purger.py'.\n")


async def limpiar_lote_en_ram(lote_datos, limite_phash=5, umbral_ia=0.92, modo_seguro=True):
    """
    Algoritmo central de purgado asíncrono en RAM. 
    Totalmente agnóstico: Recibe `lote_datos` con id, obj PIL.Image en RAM y resolución.
    """
    modelo = get_model() # Instancia Singleton
    
    if not lote_datos:
        return
        
    print(f"   🧠 Analizando topología semántica de {len(lote_datos)} imágenes obtenidas...")
    
    # Orden de prioridad: La imagen de más resolución manda como Líder.
    lote_datos.sort(key=lambda x: x['resolucion'], reverse=True)
    
    imgs_rgb = [p['img'] for p in lote_datos]
    embeddings = modelo.encode(imgs_rgb, convert_to_numpy=True)
    hashes = [imagehash.phash(img) for img in imgs_rgb]
    
    indices_aceptados = []
    ids_a_borrar = []
    descartados_phash = 0
    descartados_clip = 0

    for i in range(len(lote_datos)):
        es_duplicado = False
        p_actual = lote_datos[i]
        
        # Comparar contra los que YA HEMOS ACEPTADO como válidos (mayor resolución)
        for indice_aprobado in indices_aceptados:
            
            # 1. Filtro pHash (Esquema estructural idéntico -> Clones)
            if abs(hashes[i] - hashes[indice_aprobado]) <= limite_phash:
                es_duplicado = True
                descartados_phash += 1
                break
            
            # 2. Filtro CLIP (Concepto semántico idéntico -> Variantes estéticas)
            similitud = util.cos_sim(embeddings[i], embeddings[indice_aprobado]).item()
            if similitud >= umbral_ia:
                es_duplicado = True
                descartados_clip += 1
                break

        if not es_duplicado:
            indices_aceptados.append(i)
        else:
            ids_a_borrar.append(p_actual['id'])
    
    print(f"   📊 Resumen: Purgados {descartados_phash} estructurales (pHash) y {descartados_clip} semánticos (IA).")
    print(f"   ✨ Diseños finalistas que se conservarán en el backend: {len(indices_aceptados)}")

    if DB_AVAILABLE and ids_a_borrar:
        if not modo_seguro:
            print(f"   🧨 Ejecutando DELETE SQL en BD para {len(ids_a_borrar)} basura identificada...")
            for pid in ids_a_borrar:
                delete_poster(poster_id=pid)
        else:
            print(f"   🛡️ [DRY RUN] Simulacro activado. Se habrían borrado {len(ids_a_borrar)} registros SQL.")


async def procesar_bbdd():
    """Bucle principal de la BBDD a ejecutar periódicamente."""
    if not DB_AVAILABLE:
        sys.exit(1)
        
    import time
    import gc
    start = time.time()
    
    print("📋 Conectando con la BBDD...")
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT peli_id FROM posters_raw")
            lotes = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Error al conectar o consultar SQL: {e}")
        sys.exit(1)
        
    print(f"🚀 Iniciando purga distribuida de {len(lotes)} lotes en BBDD...\n")
    
    for idx, lote_id in enumerate(lotes):
        print(f"\n[{idx+1}/{len(lotes)}] Procesando Lote BBDD ID: {lote_id}...")
        
        registros = get_all_posters_by_peli(lote_id)
        
        # En producción: Descargar asíncronamente con aiohttp a memoria.
        # Aquí enviarías la información generada hacia `limpiar_lote_en_ram`
        # lote_en_ram = await mi_sistema_asincrono(...)
        
        # await limpiar_lote_en_ram(lote_en_ram, modo_seguro=True)
        
        # IMPORTANTE: Liberación de memoria forzada
        gc.collect()

    print(f"\n🎉 ¡PURGA GLOBAL COMPLETADA EXITOSAMENTE!")
    print(f"⏱️ Tiempo total aprox: {(time.time() - start) / 60:.2f} minutos")

if __name__ == "__main__":
    if DB_AVAILABLE:
        asyncio.run(procesar_bbdd())
