"""
Interfaz de Consola Interactiva (CLI).
"""
import sys
import os
from typing import Optional
from src.models.grammar import Grammar
from src.models.production import Production
from src.parser.grammar_parser import GrammarParser
from src.parser.validator import GrammarValidator
from src.algorithms.chomsky_pipeline import ChomskyPipeline


class ConsoleColors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


class ConsoleMenu:
    """Controlador de la interfaz de consola interactiva."""

    def __init__(self):
        self.pipeline: ChomskyPipeline = ChomskyPipeline()

    def print_banner(self):
        print(f"{ConsoleColors.CYAN}{ConsoleColors.BOLD}")
        print("=" * 70)
        print(" UNIVERSIDAD FRANCISCO DE PAULA SANTANDER - UFPS")
        print(" TEORÍA DE LA COMPUTACIÓN - MICROPROYECTO #1")
        print(" DEPURACIÓN Y FORMA NORMAL DE CHOMSKY (FNC)")
        print("=" * 70)
        print(f"{ConsoleColors.ENDC}")

    def show_menu(self):
        print(f"\n{ConsoleColors.BOLD}--- MENÚ PRINCIPAL ---{ConsoleColors.ENDC}")
        print("1. Ingresar gramática")
        print("2. Mostrar gramática original")
        print("3. Validar gramática")
        print("4. Eliminar producciones nulas")
        print("5. Eliminar producciones unitarias")
        print("6. Eliminar variables inútiles")
        print("7. Eliminar variables inalcanzables")
        print("8. Convertir a Forma Normal de Chomsky")
        print("9. Ejecutar proceso completo")
        print("10. Mostrar historial de transformaciones")
        print("11. Mostrar gramática final")
        print("12. Ingresar nueva gramática")
        print("13. Salir")
        print("-" * 35)

    def opt_1_ingresar_gramatica(self):
        print(f"\n{ConsoleColors.BOLD}>>> 1. Ingresar Gramática Libre de Contexto <<<{ConsoleColors.ENDC}")
        print("Opciones de entrada:")
        print("  [1] Ingresar manualmente paso a paso (Variables, Terminales, Símbolo inicial, Producciones)")
        print("  [2] Cargar una de las gramáticas de prueba preconfiguradas")
        print("  [3] Pegar definición en bloque de texto")
        sub_opt = input("Seleccione método de entrada [1/2/3]: ").strip()

        if sub_opt == "2":
            self._cargar_gramatica_ejemplo()
            return
        elif sub_opt == "3":
            self._ingresar_bloque_texto()
            return

        print("\nIngrese los datos solicitados:")
        vars_raw = input("• Ingrese las variables no terminales separadas por coma o espacio (ej: S, A, B): ")
        variables = GrammarParser.parse_symbol_list(vars_raw)

        terms_raw = input("• Ingrese los símbolos terminales separados por coma o espacio (ej: a, b): ")
        terminals = GrammarParser.parse_symbol_list(terms_raw)

        start_symbol = input("• Ingrese el símbolo inicial (ej: S): ").strip()

        print("\n• Ingrese las reglas de producción una por una.")
        print("  Formato soportado: S -> AB | a | ε  ó  S -> A B")
        print("  Escriba 'FIN' o presione Enter en una línea vacía para terminar.\n")

        productions = []
        prod_count = 1
        while True:
            line = input(f"  Regla #{prod_count}: ").strip()
            if not line or line.upper() == "FIN":
                break
            try:
                left, rights = GrammarParser.parse_production_line(line)
                if left:
                    for right in rights:
                        productions.append(Production(left, right))
                    prod_count += 1
            except Exception as e:
                print(f"  {ConsoleColors.FAIL}Error de formato en la regla: {e}{ConsoleColors.ENDC}")

        g = Grammar(variables, terminals, productions, start_symbol)
        self.pipeline.set_grammar(g)
        print(f"\n{ConsoleColors.GREEN}[OK] Gramática registrada con éxito ({len(productions)} producciones).{ConsoleColors.ENDC}")

    def _cargar_gramatica_ejemplo(self):
        print("\n--- Seleccione una Gramática de Prueba ---")
        print("[1] Ejemplo 1: Nulas, unitarias, inútiles y conversión a FNC completa")
        print("    S -> aB | bA | ε,  A -> a | aS | bAA,  B -> b | bS | aBB")
        print("[2] Ejemplo 2: Variables anulables y recursivas")
        print("    S -> ABaC,  A -> BC | ε,  B -> b | ε,  C -> D,  D -> d")
        print("[3] Ejemplo 3: Símbolos no generadores e inalcanzables")
        print("    S -> AB | a,  A -> a,  B -> BC,  C -> c,  D -> d")

        choice = input("Seleccione ejemplo [1-3]: ").strip()
        ejemplos = {
            "1": """
                Variables: S, A, B
                Terminales: a, b
                Inicial: S
                Producciones:
                S -> aB | bA
                A -> a | aS | bAA
                B -> b | bS | aBB
            """,
            "2": """
                Variables: S, A, B, C, D
                Terminales: a, b, d
                Inicial: S
                Producciones:
                S -> ABaC
                A -> BC | ε
                B -> b | ε
                C -> D
                D -> d
            """,
            "3": """
                Variables: S, A, B, C, D
                Terminales: a, b, c, d
                Inicial: S
                Producciones:
                S -> AB | a
                A -> a
                B -> BC
                C -> c
                D -> d
            """
        }
        text = ejemplos.get(choice, ejemplos["1"])
        g = GrammarParser.from_text_definition(text)
        self.pipeline.set_grammar(g)
        print(f"\n{ConsoleColors.GREEN}[OK] Gramática de prueba cargada con éxito:{ConsoleColors.ENDC}\n")
        print(g.to_formatted_string())

    def _ingresar_bloque_texto(self):
        print("\nPegue la definición de la gramática. Cuando termine, ingrese 'FIN' en una línea vacía:")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "FIN":
                break
            lines.append(line)
        text = "\n".join(lines)
        try:
            g = GrammarParser.from_text_definition(text)
            self.pipeline.set_grammar(g)
            print(f"\n{ConsoleColors.GREEN}[OK] Gramática registrada con éxito.{ConsoleColors.ENDC}")
        except Exception as e:
            print(f"\n{ConsoleColors.FAIL}Error al parsear la gramática: {e}{ConsoleColors.ENDC}")

    def opt_2_mostrar_gramatica_original(self):
        print(f"\n{ConsoleColors.BOLD}>>> 2. Gramática Original Registrada <<<{ConsoleColors.ENDC}")
        if not self.pipeline.original_grammar:
            print(f"{ConsoleColors.WARNING}No hay ninguna gramática registrada. Seleccione la opción 1 primero.{ConsoleColors.ENDC}")
            return
        print(self.pipeline.original_grammar.to_formatted_string())

    def opt_3_validar_gramatica(self):
        print(f"\n{ConsoleColors.BOLD}>>> 3. Validación de la Gramática <<<{ConsoleColors.ENDC}")
        if not self.pipeline.current_grammar:
            print(f"{ConsoleColors.WARNING}No hay ninguna gramática registrada.{ConsoleColors.ENDC}")
            return
        res = self.pipeline.validate_current()
        if res.is_valid:
            print(f"{ConsoleColors.GREEN}{res.get_summary()}{ConsoleColors.ENDC}")
        else:
            print(f"{ConsoleColors.FAIL}{res.get_summary()}{ConsoleColors.ENDC}")

    def opt_4_eliminar_nulas(self):
        print(f"\n{ConsoleColors.BOLD}>>> 4. Eliminación de Producciones Nulas <<<{ConsoleColors.ENDC}")
        if not self._check_grammar():
            return
        step = self.pipeline.step_null_productions()
        if step:
            print(step.to_formatted_report())

    def opt_5_eliminar_unitarias(self):
        print(f"\n{ConsoleColors.BOLD}>>> 5. Eliminación de Producciones Unitarias <<<{ConsoleColors.ENDC}")
        if not self._check_grammar():
            return
        step = self.pipeline.step_unit_productions()
        if step:
            print(step.to_formatted_report())

    def opt_6_eliminar_inutiles(self):
        print(f"\n{ConsoleColors.BOLD}>>> 6. Eliminación de Variables Inútiles (No generadoras) <<<{ConsoleColors.ENDC}")
        if not self._check_grammar():
            return
        step = self.pipeline.step_useless_symbols()
        if step:
            print(step.to_formatted_report())

    def opt_7_eliminar_inalcanzables(self):
        print(f"\n{ConsoleColors.BOLD}>>> 7. Eliminación de Variables Inalcanzables <<<{ConsoleColors.ENDC}")
        if not self._check_grammar():
            return
        step = self.pipeline.step_unreachable_symbols()
        if step:
            print(step.to_formatted_report())

    def opt_8_convertir_fnc(self):
        print(f"\n{ConsoleColors.BOLD}>>> 8. Conversión a Forma Normal de Chomsky <<<{ConsoleColors.ENDC}")
        if not self._check_grammar():
            return
        step_term, step_bin = self.pipeline.step_convert_to_chomsky()
        if step_term:
            print(step_term.to_formatted_report())
        if step_bin:
            print(step_bin.to_formatted_report())

    def opt_9_proceso_completo(self):
        print(f"\n{ConsoleColors.BOLD}>>> 9. Ejecutar Proceso Completo (Modo Automático) <<<{ConsoleColors.ENDC}")
        if not self._check_grammar():
            return
        print("Iniciando ejecución secuencial completa...\n")
        success, report = self.pipeline.execute_full_process()
        print(self.pipeline.history.get_full_report())
        print("=" * 65)
        print(report)
        print("=" * 65)

    def opt_10_mostrar_historial(self):
        print(f"\n{ConsoleColors.BOLD}>>> 10. Historial de Transformaciones <<<{ConsoleColors.ENDC}")
        print(self.pipeline.history.get_full_report())

    def opt_11_mostrar_gramatica_final(self):
        print(f"\n{ConsoleColors.BOLD}>>> 11. Gramática Resultante Final <<<{ConsoleColors.ENDC}")
        if not self.pipeline.current_grammar:
            print(f"{ConsoleColors.WARNING}No hay ninguna gramática cargada.{ConsoleColors.ENDC}")
            return
        print(self.pipeline.current_grammar.to_formatted_string())
        print("\nVerificación de cumplimiento de FNC:")
        val = self.pipeline.validate_fnc()
        print(val.get_report())

    def opt_12_reiniciar(self):
        print(f"\n{ConsoleColors.BOLD}>>> 12. Reiniciar Proceso e Ingresar Nueva Gramática <<<{ConsoleColors.ENDC}")
        confirm = input("¿Está seguro de reiniciar el proceso actual? (s/n): ").strip().lower()
        if confirm == "s":
            self.opt_1_ingresar_gramatica()

    def _check_grammar(self) -> bool:
        if not self.pipeline.current_grammar:
            print(f"{ConsoleColors.WARNING}Error: No hay ninguna gramática cargada. Seleccione la opción 1 primero.{ConsoleColors.ENDC}")
            return False
        return True

    def run(self):
        self.print_banner()
        while True:
            self.show_menu()
            choice = input(f"{ConsoleColors.BOLD}Seleccione una opción [1-13]: {ConsoleColors.ENDC}").strip()
            if choice == "1":
                self.opt_1_ingresar_gramatica()
            elif choice == "2":
                self.opt_2_mostrar_gramatica_original()
            elif choice == "3":
                self.opt_3_validar_gramatica()
            elif choice == "4":
                self.opt_4_eliminar_nulas()
            elif choice == "5":
                self.opt_5_eliminar_unitarias()
            elif choice == "6":
                self.opt_6_eliminar_inutiles()
            elif choice == "7":
                self.opt_7_eliminar_inalcanzables()
            elif choice == "8":
                self.opt_8_convertir_fnc()
            elif choice == "9":
                self.opt_9_proceso_completo()
            elif choice == "10":
                self.opt_10_mostrar_historial()
            elif choice == "11":
                self.opt_11_mostrar_gramatica_final()
            elif choice == "12":
                self.opt_12_reiniciar()
            elif choice == "13":
                print(f"\n{ConsoleColors.GREEN}Gracias por utilizar el aplicativo.{ConsoleColors.ENDC}\n")
                break
            else:
                print(f"{ConsoleColors.FAIL}Opción no válida. Por favor elija un número entre 1 y 13.{ConsoleColors.ENDC}")
