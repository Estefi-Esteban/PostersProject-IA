from pathlib import Path

# Project Root (PostersProject-IA/)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Source Code
SRC_DIR = ROOT_DIR / "src"
CORE_DIR = SRC_DIR / "core"
WEB_DIR = SRC_DIR / "web"

# Data & Assets
DATA_DIR = ROOT_DIR / "data"
POSTERS_DIR = DATA_DIR / "posters"

# Ensure directories exist
POSTERS_DIR.mkdir(parents=True, exist_ok=True)
