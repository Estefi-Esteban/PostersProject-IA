import sys
from pathlib import Path

# Add project root to sys.path to allow module imports
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from src.core.analyzer import limpiar_carpeta_hibrido
from src.core.paths import POSTERS_DIR

def main():
    print("🚀 Iniciando Limpieza de Pósters (Senior CLI)")
    print("-" * 40)
    
    # Use the posters directory defined in paths.py
    target_dir = POSTERS_DIR
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
        print(f"📁 Se ha creado la carpeta: {target_dir}")
        print("💡 Por favor, añade imágenes allí y vuelve a ejecutar este script.")
        return

    definitivos = limpiar_carpeta_hibrido(str(target_dir))
    
    print("\n" + "=" * 40)
    print(f"🌟 ANÁLISIS FINALIZADO")
    print(f"📍 Carpeta: {target_dir}")
    print(f"📊 Archivos conservados: {len(definitivos)}")
    print("=" * 40)

if __name__ == "__main__":
    main()
