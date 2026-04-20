import sys
import shutil
from pathlib import Path

# Configuración de ruta relativa para asegurar importaciones
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from src.core.analyzer import limpiar_carpeta_hibrido
from src.core.paths import POSTERS_DIR

def main():
    print("🚀 Iniciando Local Purger (IA Deduplicator)")
    print("-" * 40)
    
    target_dir = POSTERS_DIR
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
        print(f"📁 Se ha creado la carpeta local: {target_dir}")
        print("💡 Por favor, añade imágenes allí y vuelve a ejecutar este script.")
        return

    # Este purger local usa la arquitectura CLUSTER-FIRST del Motor Central
    archivos_conservados = limpiar_carpeta_hibrido(str(target_dir))
    
    print("\n" + "=" * 40)
    print(f"🌟 ANÁLISIS FINALIZADO")
    print(f"📍 Carpeta escaneada: {target_dir}")
    if archivos_conservados:
        print(f"📊 Archivos definitivos que deberías conservar: {len(archivos_conservados)}")
    print("=" * 40)

if __name__ == "__main__":
    main()
