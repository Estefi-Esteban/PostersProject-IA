# 🎞️ Visual Match Pro (AI Deduplicator)

An advanced, production-ready AI image deduplication engine. This project utilizes a hybrid mathematical and artificial intelligence approach to group visual collections, automatically detecting identical clones and semantic variants (e.g., same composition, different texts or compression ratios).

If you are a Recruiter or Developer, this project showcases my abilities in **Software Engineering**, **Applied AI (HuggingFace/SentenceTransformers)**, **Asynchronous Processing**, and **Data Pipeline Management**.

## 🚀 Key Features

This project utilizes a **Cluster-First Greedy-Pruning** architecture, moving away from naive matching, achieving highly accurate semantic groupings without losing visual fidelity:

*   **Fase 0 - Stress Filtering:** Automatically rejects files not matching minimum printing specs.
*   **Fase 1 - CLIP Semantic librarian:** Utilizes `clip-ViT-B-32` to mathematically 'understand' composition concepts and groups related image variations into families.
*   **Fase 2 - pHash Clone Limiter:** Within confirmed semantic families, heavily prunes structural clones (miniscule compressions, identical variants) via hashing matrices.
*   **Zero-Disk Memory Pipeline:** Includes advanced DevOps scripts (`db_purger.py`) mapped to memory through `io.BytesIO` and asynchronous network layers, preventing disk SSD damage in massive SQL operations. 

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Estefi-Esteban/VisualMatch-AI
   cd VisualMatch-AI
   ```

2. **System Setup using [uv](https://docs.astral.sh/uv/) (Highly Recommended):**
   *(uv handles virtual environments natively and downloads packages instantly)*
   ```bash
   uv sync
   ```

---

## 💻 Usage & Demos

### 1. Interactive UI Dashboard (`src/web/app.py`)
Run the Streamlit frontend. It applies the Singleton-managed CLIP model to analyze uploaded ZIP files or drag-and-dropped images, rendering aesthetic classifications logic live.

```bash
uv run streamlit run src/web/app.py
```

### 2. Automated File Purging (`scripts/local_purger.py`)
Drop any batch of images into `data/posters/` and execute this local implementation of the AI purger.

```bash
uv run python scripts/local_purger.py
```

### 3. Database Async Purging (`scripts/db_purger.py`)
The enterprise solution. Acts as an asynchronous backend service. It connects to SQL interfaces and reads raw remote links, computing neural embeddings fully in RAM, followed by targeted forced garbage collection (`gc.collect`) to prevent GPU/RAM memory leaks.

```bash
# Note: Fails gracefully and alerts you if SQL DB schema does not exist locally.
uv run python scripts/db_purger.py
```

---

## 📂 Architecture Layout

```text
VisualMatch-AI/
├── data/
│   └── posters/          # General local directory for testing files
├── scripts/
│   ├── local_purger.py   # General folder parsing script
│   └── db_purger.py      # Async DB/Network operations
├── src/
│   ├── core/
│   │   ├── analyzer.py   # AI & Mathematical Engine (Singleton pattern)
│   │   └── paths.py      # Cross-OS path resolvers
│   └── web/
│       └── app.py        # Streamlit graphical interface
├── legacy/               # Archive of early monolithic prototypes
├── pyproject.toml        
└── README.md
```

---

**Developed strictly focusing on Memory Efficency, Pattern Classification, and Production Robustness.**