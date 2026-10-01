# MANUAL DE USUARIO
## Aplicativo para Depuración y Conversión de GLC a Forma Normal de Chomsky (FNC)

**Universidad Francisco de Paula Santander (UFPS)**  
**Facultad de Ingeniería — Departamento de Sistemas**  
**Asignatura:** Teoría de la Computación  

---

## 1. PRESENTACIÓN DEL SISTEMA
El **Aplicativo para Depuración y Conversión de Gramáticas Libres de Contexto a Forma Normal de Chomsky** es una herramienta de software diseñada para asistir a estudiantes y docentes en el aprendizaje y verificación del proceso formal de depuración y normalización de gramáticas independientes del contexto (GLC).

El sistema toma una gramática formal $G = (V, T, P, S)$, verifica la corrección de su definición matemática y permite transformarla —bien sea de manera **paso a paso** o de manera **completamente automática**— a su forma canónica equivalente en **Forma Normal de Chomsky (FNC)**. 

### Características Principales:
- **Doble Interfaz:** Dispone de una **Interfaz Gráfica de Escritorio (GUI)** intuitiva desarrollada en Tkinter y de una **Interfaz de Línea de Comandos (CLI)** interactiva por consola.
- **Transparencia Didáctica:** En cada etapa expone con exactitud los elementos matemáticos identificados, las reglas eliminadas, las reglas agregadas y la gramática intermedia resultante.
- **Validación Rigurosa:** Comprueba consistencia de conjuntos disjuntos, símbolos no declarados y cumplimiento estricto de las reglas $A \to BC$ o $A \to a$ en la gramática final.
- **Portabilidad Total:** Implementado exclusivamente con la biblioteca estándar de Python, sin necesidad de librerías de terceros ni procesos de compilación complejos.

---

## 2. REQUISITOS PARA EJECUTAR EL PROGRAMA
Para la ejecución del aplicativo se requiere únicamente:

- **Tecnología / Lenguaje:** **Python 3.8** o superior (compatible y probado en Python 3.8, 3.9, 3.10, 3.11, 3.12 y 3.14).
- **Sistema Operativo:** 
  - Microsoft Windows (10 u 11).
  - Distribuciones Linux (Ubuntu, Debian, Fedora, Arch, etc.).
  - macOS (10.15 Catalina o superior).
- **Dependencias y Librerías:** 
  - **Ninguna librería externa requerida.** El aplicativo utiliza módulos nativos de Python (`tkinter`, `sys`, `os`, `re`, `itertools`, `collections`).
  - *Nota para usuarios de Linux:* En algunas distribuciones mínimas de Linux, Tkinter se instala por separado con el gestor de paquetes (por ejemplo: `sudo apt-get install python3-tk`). Si no se dispone de entorno gráfico, el sistema conmuta automáticamente al modo consola.

---

## 3. INSTALACIÓN Y EJECUCIÓN PASO A PASO

### Paso 1: Obtener el código del proyecto
Descargue los archivos del aplicativo o clone el repositorio desde GitHub mediante la terminal:
```bash
git clone https://github.com/JulianGomezIbarra/MICROPOYECTO-1-FNC-1151355.git
```
O simplemente descomprima la carpeta `MICROPOYECTO-1-FNC-1151355-main` en su equipo.

### Paso 2: Abrir una terminal o consola de comandos
Abra **PowerShell**, **Símbolo del sistema (CMD)** o la terminal de su sistema operativo y diríjase a la carpeta raíz del proyecto:
```bash
cd ruta/a/MICROPOYECTO-1-FNC-1151355-main
```
*(Ejemplo en Windows: `cd C:\Users\YO\Downloads\MICROPOYECTO-1-FNC-1151355-main`)*.

### Paso 3: Ejecutar el aplicativo

#### A) Modo Interfaz Gráfica (GUI) - Recomendado:
Por defecto, al iniciar el archivo principal se desplegará la ventana visual:
```bash
python main.py
```
*(En Windows también puede ejecutarse con `py main.py` o haciendo doble clic sobre `main.py`).*

#### B) Modo Consola / Terminal (CLI):
Si prefiere trabajar directamente en la terminal o no dispone de servidor gráfico:
```bash
python main.py --cli
```
o también:
```bash
python main.py --consola
```

---

## 4. INGRESO DE UNA GRAMÁTICA

El sistema modela formalmente la gramática como una 4-tupla $G = (V, T, P, S)$. Para registrarla correctamente, se deben ingresar sus 4 componentes:

### 4.1. Variables No Terminales ($V$)
- Representan los símbolos no terminales que pueden derivar en otras cadenas.
- **Formato:** Ingréselas separadas por comas o espacios. Se recomienda el uso de letras mayúsculas.
- **Ejemplo:** `S, A, B, C` o `S A B C`

### 4.2. Símbolos Terminales ($T$)
- Representan los caracteres del alfabeto del lenguaje que forman las cadenas válidas.
- **Formato:** Ingréselos separados por comas o espacios. Se recomienda el uso de letras minúsculas o números.
- **Ejemplo:** `a, b, c` o `0, 1`

### 4.3. Símbolo Inicial ($S$)
- Es la variable a partir de la cual inician todas las derivaciones del lenguaje.
- **Formato:** Debe ser una sola variable que exista obligatoriamente dentro del conjunto $V$.
- **Ejemplo:** `S`

### 4.4. Reglas de Producción ($P$)
- Expresan cómo una variable del lado izquierdo genera cadenas en el lado derecho.
- **Sintaxis soportada:**
  - Separador de asignación: flecha `->` o `::=`.
  - Agrupación de alternativas: barra vertical `|`.
  - Notación de cadena vacía: `ε`, `lambda` o `epsilon`.
  - Espaciado: puede escribir las variables juntas (ej. `AB`) o separadas por espacios (ej. `A B`).
- **Ejemplo:**
  ```text
  S -> aB | bA | ε
  A -> a | aS | bAA
  B -> b | bS | aBB
  ```

---

### Métodos de Ingreso según la Interfaz

#### En la Interfaz Gráfica (GUI):
1. **Campos de formulario:** Escriba las variables en el campo *Variables (V)*, los terminales en *Terminales (T)*, el símbolo inicial en *Símbolo Inicial (S)* y las producciones en el área de texto *Reglas de Producción (P)*.
2. **Botón "Cargar Gramática":** Al hacer clic, el sistema procesa los 4 campos y sincroniza la gramática activa.
3. **Cargar desde Archivo:** Con el botón *Cargar desde Archivo...* puede abrir directamente cualquier archivo de texto (`.txt`) con la definición formal.
4. **Ejemplos Rápidos:** Cuenta con botones para cargar instantáneamente el *Ejemplo 1 (Completo)*, *Ejemplo 2 (Anulables)* y *Ejemplo 3 (Inútiles)*.

#### En la Interfaz de Consola (CLI):
Al elegir la opción **1** del menú principal:
- **[1] Ingreso Guiado:** El sistema le pregunta paso a paso cada elemento y le permite ingresar producciones regla por regla hasta escribir `FIN` o presionar Enter en blanco.
- **[2] Gramáticas Preconfiguradas:** Permite elegir entre 3 gramáticas clásicas de libros de texto.
- **[3] Pegar Bloque de Texto:** Permite pegar directamente un texto estructurado como:
  ```text
  Variables: S, A, B
  Terminales: a, b
  Inicial: S
  Producciones:
  S -> aB | bA
  A -> a | aS | bAA
  B -> b | bS | aBB
  FIN
  ```

---

## 5. VALIDACIÓN DE LA GRAMÁTICA

Antes de ejecutar cualquier transformación, es indispensable validar que la definición sea formalmente correcta.

### ¿Cómo ejecutar la validación?
- **En la GUI:** Haga clic en el botón **"Validar Gramática"** del panel *2. Transformaciones y Operaciones*.
- **En la CLI:** Seleccione la opción **3. Validar gramática** del menú principal.

### Comprobaciones que realiza el validador:
1. **Existencia:** Que $V$, $T$ y $P$ no estén vacíos.
2. **Pertenencia del inicial:** Que el símbolo inicial $S$ pertenezca formalmente a $V$ ($S \in V$).
3. **Conjuntos disjuntos:** Que ningún símbolo esté definido a la vez como terminal y no terminal ($V \cap T = \emptyset$).
4. **Lado izquierdo válido:** Que el lado izquierdo de cada producción sea un elemento de $V$.
5. **Lado derecho conocido:** Que todos los símbolos que aparecen a la derecha hayan sido declarados en $V$, en $T$, o sean la cadena vacía $\varepsilon$.

### Interpretación de la salida:
- **Si es válida:** Muestra el mensaje:
  ```text
  [OK] La gramática es VÁLIDA y cumple con todos los requisitos formales.
  ```
- **Si contiene errores:** Detalla la lista de inconsistencias exactas (por ejemplo: símbolos no declarados, colisiones entre $V$ y $T$, o símbolo inicial faltante) para que el usuario pueda corregirlos antes de proseguir.

---

## 6. EJECUCIÓN PASO A PASO

La modalidad paso a paso permite al estudiante u operador observar detalladamente cada fase del algoritmo teórico de forma aislada.

### 6.1. Eliminar producciones nulas ($A \to \varepsilon$)
- **En GUI:** Botón **"1. Eliminar λ-nulas"**.
- **En CLI:** Opción **4. Eliminar producciones nulas**.
- **Procedimiento:**
  1. Identifica el conjunto de variables anulables ($V_{null}$), es decir, aquellas que derivan directa o indirectamente en $\varepsilon$.
  2. Para cada producción que contiene variables anulables, genera todas las combinaciones posibles omitiendo y manteniendo dichas variables.
  3. Elimina las producciones nulas directas $A \to \varepsilon$.

### 6.2. Eliminar producciones unitarias ($A \to B$)
- **En GUI:** Botón **"2. Eliminar Unitarias"**.
- **En CLI:** Opción **5. Eliminar producciones unitarias**.
- **Procedimiento:**
  1. Calcula la clausura unitaria para cada variable determinando todos los pares unitarios $(A, B)$ tales que $A \Rightarrow^* B$ usando solo producciones unitarias.
  2. Si $(A, B)$ es un par unitario y $B \to \alpha$ es una producción no unitaria, se genera la regla equivalente $A \to \alpha$.
  3. Se eliminan todas las reglas unitarias de la forma $A \to B$ con $B \in V$.

### 6.3. Eliminar variables inútiles (No generadoras)
- **En GUI:** Botón **"3. Eliminar No Generadoras"**.
- **En CLI:** Opción **6. Eliminar variables inútiles**.
- **Procedimiento:**
  1. Encuentra inductivamente el conjunto de variables generadoras $V_{gen}$, es decir, aquellas capaces de derivar en cadenas formadas exclusivamente por terminales ($w \in T^*$).
  2. Elimina del conjunto $V$ cualquier variable que no pertenezca a $V_{gen}$.
  3. Elimina toda producción que contenga variables no generadoras en su lado izquierdo o en su lado derecho.

### 6.4. Eliminar variables inalcanzables
- **En GUI:** Botón **"4. Eliminar Inalcanzables"**.
- **En CLI:** Opción **7. Eliminar variables inalcanzables**.
- **Procedimiento:**
  1. Realiza una búsqueda por grafos (BFS/DFS) comenzando desde el símbolo inicial $S$.
  2. Determina el conjunto de variables y terminales alcanzables mediante derivaciones a partir de $S$.
  3. Suprime cualquier variable o producción que haya quedado aislada o desconectada de la raíz de derivación.

### 6.5. Convertir a Forma Normal de Chomsky (FNC)
- **En GUI:** Botón **"5. Convertir a FNC"**.
- **En CLI:** Opción **8. Convertir a Forma Normal de Chomsky**.
- **Procedimiento:**
  1. **Sustitución de terminales en producciones compuestas:** En toda producción con longitud $\ge 2$ que contenga terminales (ej: $S \to aB$), se reemplaza cada terminal $a$ por una variable auxiliar única $X_a$ y se añade la regla unitaria de terminal $X_a \to a$.
  2. **Binarización de producciones largas:** Si existen producciones con más de 2 no terminales (ej: $A \to BCD$), se descomponen en cascada binaria introduciendo nuevas variables auxiliares ($A \to B X_1$, $X_1 \to CD$).

---

## 7. EJECUCIÓN AUTOMÁTICA

Para convertir una gramática de forma integral e inmediata sin necesidad de presionar cada fase por separado:

### ¿Cómo ejecutarla?
- **En la GUI:** Haga clic en el botón principal **"▶ EJECUTAR PROCESO COMPLETO"**.
- **En la CLI:** Seleccione la opción **9. Ejecutar proceso completo** del menú principal.

### Secuencia del Pipeline:
El sistema ejecuta automáticamente la cadena de transformaciones en el **orden canónico estricto** exigido por la teoría formal:
$$\text{Validación} \longrightarrow \text{Eliminar Nulas} \longrightarrow \text{Eliminar Unitarias} \longrightarrow \text{Eliminar No Generadoras} \longrightarrow \text{Eliminar Inalcanzables} \longrightarrow \text{Sustituir Terminales} \longrightarrow \text{Binarizar} \longrightarrow \text{Verificación FNC}$$

Al finalizar, se imprime el informe completo de la traza histórica y se ejecuta el validador final de FNC emitiendo una alerta de confirmación.

---

## 8. INTERPRETACIÓN DE RESULTADOS

El sistema emite reportes detallados en cada fase. Para comprender adecuadamente la salida, tenga en cuenta el significado de cada bloque:

### 1. Elementos Identificados
Detalla los conjuntos matemáticos calculados por el algoritmo:
- En nulas: Variables anulables $\{ V_{null} \}$ que pueden producir la cadena vacía.
- En unitarias: Pares unitarios transitivos $\{ (A \Rightarrow^* B) \}$.
- En inútiles: Conjunto de variables generadoras $\{ V_{gen} \}$.
- En inalcanzables: Conjunto de símbolos accesibles desde la raíz $S$.
- En Chomsky: Mapeo de terminales a variables auxiliares (ej: $a \to X_1$).

### 2. Producciones Eliminadas (`[-]`)
Son las reglas de producción que violan las restricciones de la fase en curso y que han sido depuradas para garantizar la normalización. 
- *Ejemplo:* `[-] S -> ε` (eliminada en la fase de nulas) o `[-] A -> B` (eliminada en unitarias).

### 3. Producciones Agregadas (`[+]`)
Son las nuevas reglas generadas para mantener la equivalencia del lenguaje generado por la gramática sin violar la restricción que se acaba de eliminar.
- *Ejemplo:* `[+] S -> a` (agregada por combinatoria en nulas) o `[+] X1 -> a` (creada para sustituir terminales).

### 4. Variables Auxiliares
Símbolos no terminales creados automáticamente por el sistema (con prefijo $X$, tales como $X_1, X_2, X_3 \dots$). Cumplen dos funciones esenciales:
- **Aislar terminales:** Una regla como $X_1 \to a$ permite que reglas complejas como $S \to aB$ se conviertan en $S \to X_1 B$.
- **Binarizar producciones:** Descomponer cadenas de 3 o más variables en pares de 2 variables.

### 5. Gramáticas Intermedias
Es la 4-tupla $G_i = (V_i, T_i, P_i, S_i)$ resultante inmediatamente después de culminar cada fase. Permite al usuario verificar cómo va evolucionando la gramática paso por paso y detectar el impacto específico de cada etapa.

### 6. Gramática Final
Es la gramática obtenida al concluir todo el proceso. Todas sus producciones cumplen rigurosamente con una de las dos formas canónicas de Chomsky:
$$A \longrightarrow BC \quad (B, C \in V) \qquad \text{ó} \qquad A \longrightarrow a \quad (a \in T)$$

---

## 9. MENSAJES DE ERROR MÁS FRECUENTES Y SOLUCIÓN

A continuación se presentan los errores más habituales durante el uso del programa y las instrucciones para resolverlos:

| Mensaje de Error en Pantalla | Causa del Problema | Solución Recomendada |
| :--- | :--- | :--- |
| `Error: El símbolo inicial 'X' no pertenece al conjunto de variables` | El símbolo colocado en el campo *Símbolo Inicial* no fue escrito dentro del conjunto de *Variables (V)*. | Verifique que la letra asignada como símbolo inicial esté incluida en la lista de variables no terminales. |
| `Error en producción: La variable 'D' no fue declarada en V` | Se utilizó una variable no terminal en el lado derecho de una producción que no se encuentra registrada en $V$. | Ingrese `D` en la lista de *Variables (V)* o revise posibles errores tipográficos en la regla. |
| `Error: Conflicto entre variables y terminales` | Un mismo símbolo fue introducido simultáneamente en el campo de variables y en el de terminales ($V \cap T \neq \emptyset$). | Separe claramente los conjuntos. Por convención formal, use letras mayúsculas para variables ($S, A, B$) y minúsculas para terminales ($a, b$). |
| `Formato de producción inválido (falta '->' o '::=')` | Una de las líneas de producción carece del operador flecha o contiene un error de sintaxis. | Escriba la producción siguiendo el formato canónico: `LADO_IZQ -> LADO_DER` (ejemplo: `S -> AB`). |
| `No hay ninguna gramática registrada` | Se intentó hacer clic en alguna transformación o validación sin haber cargado previamente una gramática. | Ingrese los datos en los campos y haga clic en **"Cargar Gramática"**, o use uno de los botones de ejemplos rápidos. |
| `Debe ingresar al menos una regla de producción` | El área de texto de producciones quedó en blanco. | Ingrese al menos una regla de derivación para el símbolo inicial antes de cargar la gramática. |
| `El símbolo inicial 'S' fue eliminado porque no es generador` | La gramática ingresada no produce ninguna cadena finita de terminales desde la raíz $S$ (el lenguaje es vacío $\emptyset$). | Revise las reglas de producción para asegurarse de que exista al menos un camino de derivación hacia cadenas de terminales. |

---

## 10. EJEMPLO COMPLETO DE UTILIZACIÓN

A continuación se ilustra la ejecución paso a paso de un ejercicio práctico representativo:

### 10.1. Ingreso de la Gramática
Se desea transformar a FNC la siguiente gramática libre de contexto:
- **Variables ($V$):** `S, A, B`
- **Terminales ($T$):** `a, b`
- **Símbolo Inicial ($S$):** `S`
- **Reglas de Producción ($P$):**
  ```text
  S -> aB | bA
  A -> a | aS | bAA
  B -> b | bS | aBB
  ```

---

### 10.2. Validación Inicial
Al presionar **"Validar Gramática"**, el sistema evalúa los componentes formales:
```text
=== VALIDACIÓN DE LA GRAMÁTICA ===
[OK] La gramática es válida y cumple con todos los requisitos formales.
```

---

### 10.3. Transformaciones Paso a Paso

#### Paso 1: Eliminación de Producciones Nulas
- **Elementos identificados:** `{ }` (Ninguna variable es anulable).
- **Producciones eliminadas:** Ninguna.
- **Producciones agregadas:** Ninguna.
- **Gramática resultante:** Se conserva idéntica.

#### Paso 2: Eliminación de Producciones Unitarias
- **Elementos identificados:** Pares unitarios reflexivos `{ (A, A), (B, B), (S, S) }`. No hay unitarias directas.
- **Producciones eliminadas:** Ninguna.
- **Producciones agregadas:** Ninguna.
- **Gramática resultante:** Se conserva idéntica.

#### Paso 3: Eliminación de Variables Inútiles (No Generadoras)
- **Elementos identificados:** Variables generadoras `{ A, B, S }`.
  - $A \to a$ genera terminales directamente.
  - $B \to b$ genera terminales directamente.
  - $S \to aB$ y $S \to bA$ generan terminales mediante $A$ y $B$.
- **Producciones eliminadas:** Ninguna.

#### Paso 4: Eliminación de Variables Inalcanzables
- **Elementos identificados:** Símbolos alcanzables desde $S$: `{ S, A, B, a, b }`.
- **Producciones eliminadas:** Ninguna.

#### Paso 5: Conversión a Forma Normal de Chomsky
1. **Sustitución de terminales en producciones compuestas:**
   - Para el terminal `a`: Se crea la variable auxiliar `X1` con la regla `X1 -> a`.
   - Para el terminal `b`: Se crea la variable auxiliar `X2` con la regla `X2 -> b`.
   - Reglas transformadas:
     - `S -> aB` pasa a ser `S -> X1 B`
     - `S -> bA` pasa a ser `S -> X2 A`
     - `A -> aS` pasa a ser `A -> X1 S`
     - `A -> bAA` pasa a ser `A -> X2 A A`
     - `B -> bS` pasa a ser `B -> X2 S`
     - `B -> aBB` pasa a ser `B -> X1 B B`

2. **Binarización de producciones largas ($> 2$ variables):**
   - En `A -> X2 A A` (longitud 3): Se introduce `X3 -> AA` y la regla queda: `A -> X2 X3`.
   - En `B -> X1 B B` (longitud 3): Se introduce `X4 -> BB` y la regla queda: `B -> X1 X4`.

---

### 10.4. Gramática Final Resultante en FNC
```text
=================================================================
GRAMÁTICA RESULTANTE EN FORMA NORMAL DE CHOMSKY (FNC)
=================================================================
V = { A, B, S, X1, X2, X3, X4 }
T = { a, b }
S = S
P = {
    A -> X1 S
    A -> X2 X3
    A -> a
    B -> X1 X4
    B -> X2 S
    B -> b
    S -> X1 B
    S -> X2 A
    X1 -> a
    X2 -> b
    X3 -> AA
    X4 -> BB
}
=================================================================
```

---

### 10.5. Verificación Automática de FNC
Al pulsar **"Verificar FNC"**, el sistema efectúa la inspección formal de cada regla:
```text
[EXITO] VERIFICACIÓN EXITOSA: La gramática resultante se encuentra estrictamente en Forma Normal de Chomsky (FNC).
  Todas las producciones cumplen con el formato A -> BC (con B, C en V) o A -> a (con a en T).
```
Con ello concluye satisfactoriamente el ciclo de depuración y normalización de la gramática.
