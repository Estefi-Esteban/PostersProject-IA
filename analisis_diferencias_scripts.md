# Análisis Evolutivo: Scripts Legacy vs. Nueva Generación (Carpeta `prueba/`)

Tras revisar en detalle el código comprobamos que los scripts ubicados en la carpeta `prueba/` representan una iteración mucho más **robusta, madura y escalable** (Nueva Generación) en comparación con los scripts que tenemos actualmente desplegados en `src/` (Legacy).

A continuación se detalla por qué la lógica de `prueba/` es técnica y conceptualmente superior en las áreas clave del comparador y limpiador.

---

## 1. Motor de Limpieza Core: `src/core/analyzer.py` (Legacy) vs `prueba/core.py` (Advanced)

El clásico `analyzer.py` tiene un enfoque funcional pero ineficiente y potencialmente destructivo. En cambio, `prueba/core.py` aplica una capa matemática mucho más segura.

### Por qué el enfoque "Prueba" es más robusto:
*   **Arquitectura 'Cluster-First' Segura:** El script legacy ejecutaba pHash "a ciegas" contra todas las imágenes; esto significa que un falso positivo matemático podía borrar un póster legítimo. `prueba/core.py` soluciona esto agrupando **primero** mediante Inteligencia Artificial (Conceptos Semánticos), y solo aplica la destrucción por pHash *dentro del mismo grupo*. Tienen que ser semánticamente iguales para atreverse a compararlos estructuralmente.
*   **Filtros de Calidad Inteligentes (Fase 0):** `prueba/core.py` introduce un control de estrés inicial, descartando en el paso 0 cualquier imagen que no cumpla con un mínimo de impresión real (`min_width=800`). Esto ahorra al modelo IA procesar basura desde el segundo uno.
*   **Gestión del "Liderazgo" de Clúster:** En la iteración nueva, el script ordena la lista masiva descendentemente por resolución, garantizando por diseño matemático que el elemento en el índice `0` de un clúster *siempre* sea el de mayor resolución. Ese se convierte en el "Líder" a conservar.

---

## 2. El Integrador DevOps Asíncrono: `scripts/run_cleanup.py` (Legacy) vs `prueba/purger.py` (Enterprise)

Aquí es donde la diferencia se dispara a un nivel de producción. Nuestro `run_cleanup.py` es un simple observador de carpetas locales (`data/posters/`). `prueba/purger.py` es un motor escalable para entornos de base de datos distribuidas.

### Características Nivel Senior de `purger.py`:
1.  **I/O Zero-Disk (Procesamiento en RAM):** No depende de carpetas locales. Utiliza `aiohttp` y `io.BytesIO` para descargar los pósteres directamente a la memoria RAM, sin escribir un solo bit en el disco duro. Evita destrozar los discos SSD con ciclos de escritura/lectura inútiles al purgar los miles de pósteres de una BBDD.
2.  **Operación Asíncrona (Async/Await):** Puede disparar 100 descargas simultáneas en paralelo frente al legacy secuencial.
3.  **Filtrado Híbrido Greedy Secuencial Dinámico:** Al igual que `core.py`, procesa la memoria cruzando la matriz de la IA y el hashing en un bucle rapidísimo sobre la RAM, identificando falsos clones con mucha más precisión.
4.  **Gestión Manual de Hardware:** Implementa `gc.collect()` para forzar a Python a "limpiar la basura" alojada en la RAM (`Garbage Collector`) tras procesar cada película, mitigando el conocido problema del Memory Leak en los bucles de IA pesados.

---

## 3. Interface Web Visual: `src/web/app.py` (Legacy) vs `prueba/app.py` (Refinada)

El comportamiento de la interfaz gráfica local en `prueba/app.py` demuestra tener un algoritmo de agrupamiento de UI más ajustado.

### Mejoras visuales en "Prueba":
*   **Matriz Exclusiva de IA para Grupos:** En lugar de mezclar factores condicionales indiscriminadamente para la experiencia visual, `prueba/app.py` se basa **exclusivamente en la IA (CLIP)** para armar las carpetas moradas frontales. Usa una similitud `>= 0.80` asegurando mucha mejor cohesión temática que la vista en el script Legacy.
*   **Identificador en Pantalla por pares exactos:** Si detecta internamente similitud `>= 0.98` dentro del sub-grupo, la etiqueta visualmente para el usuario como `Clon Exacto🟢`, sino le adjudica de manera transparente ser `Variante🟠`. El código legacy se enredaba mezclando las reglas de pHash.

