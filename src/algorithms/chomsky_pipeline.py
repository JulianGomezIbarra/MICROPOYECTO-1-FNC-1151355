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
        Ejecuta todas las etapas consecutivamente en orden canónico (Modo Automático):
        1. Validación inicial.
        2. Eliminación de nulas.
        3. Eliminación de unitarias.
        4. Eliminación de inútiles (no generadoras).
        5. Eliminación de inalcanzables.
        6. Sustitución de terminales en producciones compuestas.
        7. Reducción de producciones largas.
        8. Validación automática FNC.
        """
        if not self.original_grammar:
            return False, "Error: No hay una gramática cargada para procesar."

        # Restauramos desde original
        self.current_grammar = self.original_grammar.clone()
        self.history.clear()

        # Validación
        val_res = self.validate_current()
        if not val_res.is_valid:
            return False, f"La gramática presenta errores y no puede procesarse:\n{val_res.get_summary()}"

        # 1. Nulas
        self.step_null_productions()
        # 2. Unitarias
        self.step_unit_productions()
        # 3. No generadoras
        self.step_useless_symbols()
        # 4. Inalcanzables
        self.step_unreachable_symbols()
        # 5. Sustitución de terminales y Binarización
        self.step_convert_to_chomsky()

        # Validación final FNC
        fnc_check = self.validate_fnc()
        return fnc_check.is_fnc, fnc_check.get_report()

    def validate_fnc(self) -> FNCValidationResult:
        """Verifica automáticamente si la gramática actual está en FNC."""
        if not self.current_grammar:
            return FNCValidationResult(False, [])
        return FNCValidator.validate(self.current_grammar)
