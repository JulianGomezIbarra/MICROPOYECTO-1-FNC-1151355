"""
Orquestador del flujo de transformación a Forma Normal de Chomsky.
Maneja tanto el Modo Paso a Paso como el Modo Automático.
"""
from typing import Tuple, Optional
from src.models.grammar import Grammar
from src.history.transformation_step import HistoryManager, TransformationStep
from src.parser.validator import GrammarValidator, GrammarValidationResult
from src.algorithms.null_productions import NullProductionsEliminator
from src.algorithms.unit_productions import UnitProductionsEliminator
from src.algorithms.useless_symbols import UselessSymbolsEliminator
from src.algorithms.chomsky_converter import ChomskyConverter
from src.algorithms.fnc_validator import FNCValidator, FNCValidationResult


class ChomskyPipeline:
    """
    Controlador central del proceso de transformación.
    Mantiene la gramática original, la gramática en su estado actual,
    el historial de pasos y el estado de avance.
    """

    def __init__(self, original_grammar: Optional[Grammar] = None):
        self.original_grammar: Optional[Grammar] = original_grammar.clone() if original_grammar else None
        self.current_grammar: Optional[Grammar] = original_grammar.clone() if original_grammar else None
        self.history: HistoryManager = HistoryManager()
        self.step_executed = {
            "validated": False,
            "null_eliminated": False,
            "unit_eliminated": False,
            "useless_eliminated": False,
            "unreachable_eliminated": False,
            "terminals_substituted": False,
            "long_reduced": False,
        }

    def set_grammar(self, grammar: Grammar) -> None:
        """Establece una nueva gramática y reinicia el proceso."""
        self.original_grammar = grammar.clone()
        self.current_grammar = grammar.clone()
        self.history.clear()
        for k in self.step_executed:
            self.step_executed[k] = False

    def validate_current(self) -> GrammarValidationResult:
        """Valida los componentes de la gramática actual."""
        if not self.current_grammar:
            return GrammarValidationResult(False, ["No hay ninguna gramática cargada."])
        res = GrammarValidator.validate(self.current_grammar)
        if res.is_valid:
            self.step_executed["validated"] = True
        return res

    def step_null_productions(self) -> Optional[TransformationStep]:
        """Ejecuta la eliminación de producciones nulas."""
        if not self.current_grammar:
            return None
        self.current_grammar, step = NullProductionsEliminator.eliminate(self.current_grammar)
        self.history.add_step(step)
        self.step_executed["null_eliminated"] = True
        return step

    def step_unit_productions(self) -> Optional[TransformationStep]:
        """Ejecuta la eliminación de producciones unitarias."""
        if not self.current_grammar:
            return None
        self.current_grammar, step = UnitProductionsEliminator.eliminate(self.current_grammar)
        self.history.add_step(step)
        self.step_executed["unit_eliminated"] = True
        return step

    def step_useless_symbols(self) -> Optional[TransformationStep]:
        """Ejecuta la eliminación de variables inútiles (no generadoras)."""
        if not self.current_grammar:
            return None
        self.current_grammar, step = UselessSymbolsEliminator.eliminate_non_generating(self.current_grammar)
        self.history.add_step(step)
        self.step_executed["useless_eliminated"] = True
        return step

    def step_unreachable_symbols(self) -> Optional[TransformationStep]:
        """Ejecuta la eliminación de variables inalcanzables."""
        if not self.current_grammar:
            return None
        self.current_grammar, step = UselessSymbolsEliminator.eliminate_unreachable(self.current_grammar)
        self.history.add_step(step)
        self.step_executed["unreachable_eliminated"] = True
        return step

    def step_convert_to_chomsky(self) -> Tuple[Optional[TransformationStep], Optional[TransformationStep]]:
        """
        Ejecuta la conversión a FNC:
        1. Sustitución de terminales.
        2. Binarización de producciones largas.
        """
        if not self.current_grammar:
            return None, None
        
        # 1. Terminales
        self.current_grammar, step_term = ChomskyConverter.substitute_terminals(self.current_grammar)
        self.history.add_step(step_term)
        self.step_executed["terminals_substituted"] = True

        # 2. Binarización
        self.current_grammar, step_bin = ChomskyConverter.reduce_long_productions(self.current_grammar)
        self.history.add_step(step_bin)
        self.step_executed["long_reduced"] = True

        return step_term, step_bin

    def execute_full_process(self) -> Tuple[bool, str]:
        """
        Ejecuta todas las etapas consecutivamente según el algoritmo requerido (Modo Automático):
        1. Validación inicial de la GLC.
        2. Eliminación de variables inútiles (no generadoras).
        3. Eliminación de variables inalcanzables.
        4. Eliminación de producciones nulas (ε).
        5. Eliminación de producciones unitarias.
        6. Conversión de producciones a FNC (sustitución de terminales y binarización).
        7. Presentación y validación final de la gramática en FNC.
        """
        if not self.original_grammar:
            return False, "Error: No hay una gramática cargada para procesar."

        # Restauramos desde original
        self.current_grammar = self.original_grammar.clone()
        self.history.clear()

        # Validación inicial
        val_res = self.validate_current()
        if not val_res.is_valid:
            return False, f"La gramática presenta errores y no puede procesarse:\n{val_res.get_summary()}"

        # 1. Variables inútiles (no generadoras)
        self.step_useless_symbols()
        # 2. Variables inalcanzables
        self.step_unreachable_symbols()
        # 3. Producciones nulas
        self.step_null_productions()
        # 4. Producciones unitarias
        self.step_unit_productions()
        # 5. Conversión a FNC (sustitución de terminales y reducción binaria)
        self.step_convert_to_chomsky()

        # 6. Validación y verificación final FNC
        fnc_check = self.validate_fnc()
        return fnc_check.is_fnc, fnc_check.get_report()

    def get_final_chomsky_presentation(self) -> str:
        """
        Presenta formalmente la gramática final en Forma Normal de Chomsky
        junto con el informe de verificación de cumplimiento de FNC.
        """
        if not self.current_grammar:
            return "No hay ninguna gramática cargada."

        fnc_check = self.validate_fnc()
        lines = [
            "=" * 65,
            " PRESENTACIÓN DE LA GRAMÁTICA FINAL EN FORMA NORMAL DE CHOMSKY (FNC)",
            "=" * 65,
            "Definición formal G = (V, T, P, S):",
            self.current_grammar.to_formatted_string(),
            "-" * 65,
            "ESTADO DE CUMPLIMIENTO CON LA FORMA NORMAL DE CHOMSKY:",
            fnc_check.get_report(),
            "=" * 65,
        ]
        return "\n".join(lines)

    def validate_fnc(self) -> FNCValidationResult:
        """Verifica automáticamente si la gramática actual está en FNC."""
        if not self.current_grammar:
            return FNCValidationResult(False, [])
        return FNCValidator.validate(self.current_grammar)

