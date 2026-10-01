"""
Interfaz Gráfica de Usuario (GUI) básica y funcional con Tkinter.
Permite ingresar gramáticas, ejecutar transformaciones paso a paso o en modo completo,
y visualizar el historial y la gramática resultante en FNC.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from typing import Optional

from src.models.grammar import Grammar
from src.parser.grammar_parser import GrammarParser
from src.algorithms.chomsky_pipeline import ChomskyPipeline


class ChomskyGUIApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Conversor de GLC a Forma Normal de Chomsky (FNC) - UFPS")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        self.pipeline: ChomskyPipeline = ChomskyPipeline()

        self._build_ui()

    def _build_ui(self):
        # Frame superior para entrada de gramática
        top_frame = ttk.LabelFrame(self.root, text=" 1. Entrada y Configuración de Gramática ", padding=10)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Campos de texto de entrada básica
        grid_frame = ttk.Frame(top_frame)
        grid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(grid_frame, text="Variables (V):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.txt_vars = ttk.Entry(grid_frame, width=30)
        self.txt_vars.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(grid_frame, text="(ej: S, A, B)").grid(row=0, column=2, sticky=tk.W, pady=2)

        ttk.Label(grid_frame, text="Terminales (T):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.txt_terms = ttk.Entry(grid_frame, width=30)
        self.txt_terms.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(grid_frame, text="(ej: a, b)").grid(row=1, column=2, sticky=tk.W, pady=2)

        ttk.Label(grid_frame, text="Símbolo Inicial (S):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.txt_start = ttk.Entry(grid_frame, width=15)
        self.txt_start.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(grid_frame, text="(ej: S)").grid(row=2, column=2, sticky=tk.W, pady=2)

        ttk.Label(grid_frame, text="Reglas de Producción (P):").grid(row=3, column=0, sticky=tk.NW, pady=2)
        self.txt_prods = scrolledtext.ScrolledText(grid_frame, width=35, height=4, font=("Consolas", 10))
        self.txt_prods.grid(row=3, column=1, columnspan=2, sticky=tk.W, padx=5, pady=2)
        ttk.Label(grid_frame, text="(ej: S -> aSb|bSa|ε)").grid(row=3, column=3, sticky=tk.W, pady=2)

        # Botones de carga rápida al lado derecho
        quick_frame = ttk.LabelFrame(top_frame, text=" Acciones Rápidas ", padding=5)
        quick_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)

        ttk.Button(quick_frame, text="Cargar Gramática", command=self.cargar_gramatica).pack(fill=tk.X, pady=2)
        ttk.Button(quick_frame, text="Cargar desde Archivo...", command=self.cargar_archivo).pack(fill=tk.X, pady=2)
        ttk.Button(quick_frame, text="Ejemplo 1 (Completo)", command=lambda: self.cargar_ejemplo(1)).pack(fill=tk.X, pady=2)
        ttk.Button(quick_frame, text="Ejemplo 2 (Anulables)", command=lambda: self.cargar_ejemplo(2)).pack(fill=tk.X, pady=2)
        ttk.Button(quick_frame, text="Ejemplo 3 (Inútiles)", command=lambda: self.cargar_ejemplo(3)).pack(fill=tk.X, pady=2)
        ttk.Button(quick_frame, text="Limpiar Todo", command=self.limpiar_todo).pack(fill=tk.X, pady=2)

        # Frame intermedio de control y operaciones
        ops_frame = ttk.LabelFrame(self.root, text=" 2. Transformaciones y Operaciones ", padding=10)
        ops_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        btn_row1 = ttk.Frame(ops_frame)
        btn_row1.pack(fill=tk.X, pady=2)

        ttk.Button(btn_row1, text="Validar Gramática", command=self.validar_gramatica).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row1, text="1. Eliminar λ-nulas", command=self.eliminar_nulas).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row1, text="2. Eliminar Unitarias", command=self.eliminar_unitarias).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row1, text="3. Eliminar No Generadoras", command=self.eliminar_inutiles).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row1, text="4. Eliminar Inalcanzables", command=self.eliminar_inalcanzables).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row1, text="5. Convertir a FNC", command=self.convertir_fnc).pack(side=tk.LEFT, padx=3)

        btn_row2 = ttk.Frame(ops_frame)
        btn_row2.pack(fill=tk.X, pady=4)

        ttk.Button(btn_row2, text="▶ EJECUTAR PROCESO COMPLETO", command=self.proceso_completo).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row2, text="Verificar FNC", command=self.verificar_fnc).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row2, text="Ver Gramática Actual", command=self.mostrar_gramatica_actual).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row2, text="Ver Historial Completo", command=self.mostrar_historial).pack(side=tk.LEFT, padx=3)

        # Frame inferior para salida y logs
        out_frame = ttk.LabelFrame(self.root, text=" 3. Salida de Resultados y Traza de Pasos ", padding=10)
        out_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.txt_salida = scrolledtext.ScrolledText(out_frame, font=("Consolas", 10), wrap=tk.WORD)
        self.txt_salida.pack(fill=tk.BOTH, expand=True)

        self._escribir_salida("=== Bienvenido al Asistente de Conversión a FNC ===\n"
                              "Ingrese los componentes de la gramática o cargue uno de los ejemplos preconfigurados.")

    def _escribir_salida(self, texto: str, limpiar: bool = False):
        if limpiar:
            self.txt_salida.delete("1.0", tk.END)
        self.txt_salida.insert(tk.END, texto + "\n")
        self.txt_salida.see(tk.END)

    def _obtener_gramatica_campos(self) -> Optional[Grammar]:
        vars_raw = self.txt_vars.get().strip()
        terms_raw = self.txt_terms.get().strip()
        start = self.txt_start.get().strip()
        prods_raw = self.txt_prods.get("1.0", tk.END).strip()

        if not prods_raw:
            messagebox.showwarning("Atención", "Debe ingresar al menos una regla de producción.")
            return None

        # Si el usuario solo escribió las producciones o llenó el bloque
        bloque = f"Variables: {vars_raw}\nTerminales: {terms_raw}\nInicial: {start}\nProducciones:\n{prods_raw}"
        try:
            g = GrammarParser.from_text_definition(bloque)
            return g
        except Exception as e:
            messagebox.showerror("Error al parsear", f"Error de formato en la gramática:\n{e}")
            return None

    def cargar_gramatica(self):
        g = self._obtener_gramatica_campos()
        if g:
            self.pipeline.set_grammar(g)
            self._escribir_salida("\n[OK] Gramática cargada con éxito:", limpiar=True)
            self._escribir_salida(g.to_formatted_string())
            # Sincronizar campos
            self.txt_vars.delete(0, tk.END)
            self.txt_vars.insert(0, ", ".join(sorted(g.variables)))
            self.txt_terms.delete(0, tk.END)
            self.txt_terms.insert(0, ", ".join(sorted(g.terminals)))
            self.txt_start.delete(0, tk.END)
            self.txt_start.insert(0, g.start_symbol)

    def cargar_archivo(self):
        path = filedialog.askopenfilename(
            title="Seleccionar archivo de gramática",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                contenido = f.read()
            g = GrammarParser.from_text_definition(contenido)
            self.pipeline.set_grammar(g)
            self._cargar_gramatica_a_interfaz(g)
            self._escribir_salida(f"\n[OK] Gramática cargada desde '{path}':", limpiar=True)
            self._escribir_salida(g.to_formatted_string())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    def cargar_ejemplo(self, num: int):
        ejemplos = {
            1: ("S, A, B", "a, b", "S", "S -> aB | bA\nA -> a | aS | bAA\nB -> b | bS | aBB"),
            2: ("S, A, B, C, D", "a, b, d", "S", "S -> ABaC\nA -> BC | ε\nB -> b | ε\nC -> D\nD -> d"),
            3: ("S, A, B, C, D", "a, b, c, d", "S", "S -> AB | a\nA -> a\nB -> BC\nC -> c\nD -> d")
        }
        v, t, s, p = ejemplos[num]
        self.txt_vars.delete(0, tk.END)
        self.txt_vars.insert(0, v)
        self.txt_terms.delete(0, tk.END)
        self.txt_terms.insert(0, t)
        self.txt_start.delete(0, tk.END)
        self.txt_start.insert(0, s)
        self.txt_prods.delete("1.0", tk.END)
        self.txt_prods.insert(tk.END, p)
        self.cargar_gramatica()

    def _cargar_gramatica_a_interfaz(self, g: Grammar):
        self.txt_vars.delete(0, tk.END)
        self.txt_vars.insert(0, ", ".join(sorted(g.variables)))
        self.txt_terms.delete(0, tk.END)
        self.txt_terms.insert(0, ", ".join(sorted(g.terminals)))
        self.txt_start.delete(0, tk.END)
        self.txt_start.insert(0, g.start_symbol)
        
        # Agrupar producciones
        grouped = {}
        for p in g.productions:
            grouped.setdefault(p.left, []).append(p.get_right_as_string())
        lines = [f"{v} -> {' | '.join(alts)}" for v, alts in grouped.items()]
        self.txt_prods.delete("1.0", tk.END)
        self.txt_prods.insert(tk.END, "\n".join(lines))

    def limpiar_todo(self):
        self.txt_vars.delete(0, tk.END)
        self.txt_terms.delete(0, tk.END)
        self.txt_start.delete(0, tk.END)
        self.txt_prods.delete("1.0", tk.END)
        self.txt_salida.delete("1.0", tk.END)
        self.pipeline = ChomskyPipeline()
        self._escribir_salida("Campos y estado reiniciados.")

    def _verificar_cargada(self) -> bool:
        if not self.pipeline.current_grammar:
            # Intentar cargar desde los campos directamente
            self.cargar_gramatica()
            if not self.pipeline.current_grammar:
                messagebox.showwarning("Atención", "Primero debe cargar o ingresar una gramática válida.")
                return False
        return True

    def validar_gramatica(self):
        if not self._verificar_cargada():
            return
        res = self.pipeline.validate_current()
        self._escribir_salida("\n=== VALIDACIÓN DE LA GRAMÁTICA ===")
        self._escribir_salida(res.get_summary())

    def eliminar_nulas(self):
        if not self._verificar_cargada():
            return
        step = self.pipeline.step_null_productions()
        if step:
            self._escribir_salida("\n" + step.to_formatted_report())

    def eliminar_unitarias(self):
        if not self._verificar_cargada():
            return
        step = self.pipeline.step_unit_productions()
        if step:
            self._escribir_salida("\n" + step.to_formatted_report())

    def eliminar_inutiles(self):
        if not self._verificar_cargada():
            return
        step = self.pipeline.step_useless_symbols()
        if step:
            self._escribir_salida("\n" + step.to_formatted_report())

    def eliminar_inalcanzables(self):
        if not self._verificar_cargada():
            return
        step = self.pipeline.step_unreachable_symbols()
        if step:
            self._escribir_salida("\n" + step.to_formatted_report())

    def convertir_fnc(self):
        if not self._verificar_cargada():
            return
        step_term, step_bin = self.pipeline.step_convert_to_chomsky()
        if step_term:
            self._escribir_salida("\n" + step_term.to_formatted_report())
        if step_bin:
            self._escribir_salida("\n" + step_bin.to_formatted_report())

    def proceso_completo(self):
        if not self._verificar_cargada():
            return
        self._escribir_salida("\n" + "=" * 60, limpiar=True)
        self._escribir_salida("EJECUCIÓN DEL PROCESO COMPLETO (MODO AUTOMÁTICO)")
        self._escribir_salida("=" * 60)
        success, report = self.pipeline.execute_full_process()
        self._escribir_salida(self.pipeline.history.get_full_report())
        self._escribir_salida("=" * 60)
        self._escribir_salida(report)
        self._escribir_salida("=" * 60)
        if success:
            messagebox.showinfo("Proceso Completo", "La gramática se transformó exitosamente a FNC.")
        else:
            messagebox.showwarning("Proceso Incompleto", report)

    def verificar_fnc(self):
        if not self._verificar_cargada():
            return
        res = self.pipeline.validate_fnc()
        self._escribir_salida("\n=== VERIFICACIÓN DE CUMPLIMIENTO FNC ===")
        self._escribir_salida(res.get_report())

    def mostrar_gramatica_actual(self):
        if not self._verificar_cargada():
            return
        self._escribir_salida("\n=== GRAMÁTICA EN ESTADO ACTUAL ===")
        self._escribir_salida(self.pipeline.current_grammar.to_formatted_string())

    def mostrar_historial(self):
        if not self._verificar_cargada():
            return
        self._escribir_salida("\n" + self.pipeline.history.get_full_report())


def run_gui():
    root = tk.Tk()
    app = ChomskyGUIApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
