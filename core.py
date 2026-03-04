import os
from sentence_transformers import SentenceTransformer, util
from PIL import Image

def analizar_carpeta(ruta_carpeta):
    print("⏳ Cargando el modelo CLIP...")
    modelo = SentenceTransformer('clip-ViT-B-32')
    
    # 1. Buscar todas las imágenes en la carpeta
    archivos = [f for f in os.listdir(ruta_carpeta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if len(archivos) < 2:
        print(f"❌ Necesitas al menos 2 imágenes en la carpeta '{ruta_carpeta}' para comparar.")
        return

    print(f"🖼️ Procesando {len(archivos)} imágenes...")
    
    # 2. Cargar las imágenes en memoria
    imagenes = []
    nombres = []
    for archivo in archivos:
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        imagenes.append(Image.open(ruta_completa))
        nombres.append(archivo)
        
    # 3. Generar todos los vectores matemáticos de golpe (Batch processing)
    print("🧠 Extrayendo características visuales...")
    embeddings = modelo.encode(imagenes)
    
    # 4. Comparar todos contra todos
    print("📊 Calculando similitudes...\n")
    matriz_similitud = util.cos_sim(embeddings, embeddings)
    
    print("-" * 40)
    print("📋 RESULTADOS DE SIMILITUD:")
    print("-" * 40)
    
    # 5. Recorrer la matriz para mostrar los pares (evitando duplicados y comparar consigo misma)
    encontrados = False
    for i in range(len(archivos)):
        for j in range(i + 1, len(archivos)):
            similitud = matriz_similitud[i][j].item() * 100
            
            if similitud >= 90:
                print(f"🔥 ALTA SIMILITUD ({similitud:.2f}%): '{nombres[i]}' y '{nombres[j]}'")
                encontrados = True
            elif similitud >= 75:
                print(f"🟡 SIMILITUD MEDIA ({similitud:.2f}%): '{nombres[i]}' y '{nombres[j]}'")
                encontrados = True
                
    if not encontrados:
        print("🤷‍♀️ No se encontraron pósters con similitud mayor al 75%. Todos parecen únicos.")

# --- ZONA DE PRUEBA ---
if __name__ == "__main__":
    carpeta_prueba = "posters"
    if not os.path.exists(carpeta_prueba):
        os.makedirs(carpeta_prueba)
        print(f"📁 He creado la carpeta '{carpeta_prueba}'. ¡Mete algunas imágenes ahí y vuelve a ejecutar!")
    else:
        analizar_carpeta(carpeta_prueba)