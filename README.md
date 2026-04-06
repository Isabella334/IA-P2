# Inteligencia Artificial | Proyecto 2
---

## 🎥 Video explicativo

> 📺 [link]

---

## 🗂️ Tasks

### Task 1 — Configuración Segura de la Red (CSP y Factor Graphs)
Antes de que la red entre en funcionamiento, se debe asignar un protocolo de
seguridad a cada servidor. La restricción es que ningún par de servidores
conectados directamente puede compartir el mismo protocolo, para evitar
vulnerabilidades de movimiento lateral. Se modela como un CSP sobre un grafo
de 18 nodos con 4 protocolos disponibles (Rojo, Verde, Azul, Amarillo) y se
implementa Backtracking Search en tres versiones de complejidad creciente:
puro, con Forward Checking, y con Forward Checking + heurística MRV.

### Task 2 — Defensa Adversarial (Juegos de Suma Cero)
Con la red operativa, un atacante ha penetrado el sistema. Se modela la
situación como un juego adversarial por turnos de suma cero: la Defensa (MAX)
y el Hacker (MIN) se turnan para capturar nodos adyacentes, cada uno con un
valor de información asignado aleatoriamente. Se implementa Minimax con Poda
Alfa-Beta para optimizar el árbol de búsqueda, y una función de evaluación
heurística con profundidad limitada (d_max = 4) dado que explorar el árbol
completo es computacionalmente inviable.

### Task 3 — Incertidumbre y Latencia (Expectiminimax y MDPs)
El entorno ahora es no determinista: cada acción de captura tiene un 80% de
probabilidad de éxito y un 20% de fallar, perdiendo el turno. Se extiende el
algoritmo de la Fase 2 a un árbol Expectiminimax incorporando nodos de azar
que ponderan los resultados por probabilidad. Se compara el comportamiento del
agente Minimax clásico (que asume un mundo perfecto) contra el agente
Expectiminimax (que entiende el riesgo) en este entorno estocástico, y se
formula teóricamente el escenario sin oponente como un MDP usando la Ecuación
de Bellman.

---

## ⚙️ Requisitos
```bash
pip install matplotlib networkx
```

Python 3.11 o superior.

## ▶️ Cómo ejecutar

Desde la carpeta de cada task:

```bash
# Task 1
cd Task1
python backtracking.py

# Task 2
cd Task2
python main.py

# Task 3
cd Task3
python main.py
```