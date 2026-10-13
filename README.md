# Aplicativo para Depuración y Conversión de GLC a Forma Normal de Chomsky (FNC)

**Universidad Francisco de Paula Santander (UFPS)**  
**Teoría de la Computación 2026/02 - Microproyecto #1**

---

## 📌 Descripción General
Aplicativo desarrollado en **Python** que permite ingresar una **Gramática Libre de Contexto (GLC)** formalmente definida como $G = (V, T, P, S)$, validar sus componentes y realizar de forma automática o paso a paso el proceso completo de depuración y transformación hasta obtener una gramática equivalente en **Forma Normal de Chomsky (FNC)**.

El sistema registra y expone cada transformación intermedia, indicando claramente:
- Gramática inicial de la etapa.
- Elementos identificados (variables anulables, pares unitarios, variables no generadoras, inalcanzables, etc.).
- Reglas de producción eliminadas.
- Reglas de producción agregadas.
- Gramática resultante de cada fase.

---

## 🚀 Etapas del Proceso de Conversión
1. **Validación Inicial de la GLC**:
   - Existencia de variables, terminales y símbolo inicial ($S \in V$).
   - Soporte flexible para variables y terminales tanto en mayúsculas como en minúsculas.
   - Detección de símbolos no declarados e integridad sintáctica.
2. **Eliminación de Variables Inútiles**:
   - Identificación del conjunto de variables generadoras ($V_{gen}$).
   - Eliminación de variables no generadoras y producciones asociadas.
3. **Eliminación de Variables Inalcanzables**:
   - Identificación de variables alcanzables mediante recorrido BFS desde el símbolo inicial $S$.
   - Eliminación de variables inaccesibles.
4. **Eliminación de Producciones Nulas ($A \to \varepsilon$)**:
   - Identificación inductiva del conjunto de variables anulables ($V_{null}$).
   - Soporte para épsilon / lambda en mayúsculas o minúsculas (`ε`, `λ`, `epsilon`, `EPSILON`, `lambda`, `LAMBDA`, `eps`).
   - Sustitución combinatoria y remoción de reglas vacías.
5. **Eliminación de Producciones Unitarias ($A \to B$)**:
   - Determinación de pares unitarios transitivos mediante punto fijo.
   - Sustitución de reglas unitarias por producciones no unitarias equivalentes.
6. **Conversión a Forma Normal de Chomsky (FNC)**:
   - **Sustitución de terminales**: En producciones de longitud $\ge 2$, los terminales se reemplazan por variables auxiliares ($X_i \to a$).
   - **Reducción de producciones largas**: Producciones con más de 2 no terminales se binarizan en cascada ($X_j \dots$).
7. **Presentación de la Gramática Final y Validación FNC**:
   - Presentación formal de la tupla $G = (V, T, P, S)$ en FNC.
   - Verificación estricta de que todas las reglas cumplan $A \to BC$ o $A \to a$.

---

## 📁 Estructura del Proyecto
```text
├── src/
│   ├── models/            # Modelos de datos (Grammar, Production, Symbol)
│   ├── parser/            # Validador y parser de gramáticas
│   ├── algorithms/        # Algoritmos de transformación (Null, Unit, Useless, Chomsky)
│   ├── history/           # Trazabilidad e historial paso a paso
│   └── ui/                # Menú interactivo y vistas por consola
├── tests/                 # Batería de pruebas unitarias con pytest/unittest
├── gramaticas_ejemplo/    # Archivos de gramáticas de prueba
├── docs/                  # Documento técnico y Manual de usuario
├── main.py                # Punto de entrada de la aplicación
├── requirements.txt       # Dependencias (si aplica)
└── README.md              # Documentación general
```

---

## 💻 Requisitos y Ejecución

### Opción 1: Ejecutable directo (Sin necesidad de instalar Python)
Para la profesora o usuarios sin Python configurado en su equipo:
- Simplemente hacer doble clic sobre **`Chomsky_FNC.exe`** (o en **`EJECUTAR.bat`**).
- Abrirá de inmediato la Interfaz Gráfica (GUI) en pantalla completa/ventana de escritorio.

### Opción 2: Desde código fuente (con Python)
- Requiere **Python 3.8+**
- Ejecución de la interfaz gráfica:
  ```bash
  python main.py
  ```
- Opcional por consola (CLI):
  ```bash
  python main.py --cli
  ```

---

## 👥 Integrantes
- Estudiantes de Teoría de la Computación - UFPS
