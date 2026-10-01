"""
Validador de Gramáticas Libres de Contexto (GLC)
"""
from typing import List, Tuple
from src.models.grammar import Grammar
from src.models.production import Production


class GrammarValidationResult:
    """Contenedor para el resultado de validación con su lista de errores y advertencias."""

    def __init__(self, is_valid: bool, errors: List[str], warnings: List[str] = None):
        self.is_valid: bool = is_valid
        self.errors: List[str] = errors
        self.warnings: List[str] = warnings if warnings else []

    def __bool__(self) -> bool:
        return self.is_valid

    def get_summary(self) -> str:
        lines = []
        if self.is_valid:
            lines.append("[OK] La gramática es válida.")
        else:
            lines.append(f"[ERROR] Se encontraron {len(self.errors)} error(es) en la definición de la gramática:")
            for err in self.errors:
                lines.append(f"   • {err}")
        if self.warnings:
            lines.append(f"[ADVERTENCIA] Advertencias ({len(self.warnings)}):")
            for w in self.warnings:
                lines.append(f"   • {w}")
        return "\n".join(lines)


class GrammarValidator:
    """
    Realiza las comprobaciones formales de una Gramática Libre de Contexto:
    1. Que exista al menos una variable.
    2. Que exista al menos un terminal.
    3. Que exista un símbolo inicial.
    4. Que el símbolo inicial pertenezca al conjunto de variables.
    5. Que los conjuntos de variables y terminales sean disjuntos.
    6. Que toda producción tenga una variable válida en el lado izquierdo.
    7. Que todos los símbolos utilizados en el lado derecho hayan sido declarados en V o T.
    8. Que no existan símbolos desconocidos.
    """

    @classmethod
    def validate(cls, grammar: Grammar) -> GrammarValidationResult:
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Al menos una variable
        if not grammar.variables:
            errors.append("Error: Debe existir al menos una variable (símbolo no terminal).")

        # 2. Al menos un terminal
        if not grammar.terminals:
            errors.append("Error: Debe existir al menos un símbolo terminal.")

        # 3. Símbolo inicial no vacío
        if not grammar.start_symbol:
            errors.append("Error: No se ha definido un símbolo inicial para la gramática.")
        # 4. Símbolo inicial pertenece a V
        elif grammar.start_symbol not in grammar.variables:
            errors.append(
                f"Error: El símbolo inicial '{grammar.start_symbol}' no pertenece al conjunto de variables {grammar.variables}."
            )

        # 5. V y T deben ser conjuntos disjuntos (V ∩ T = ∅)
        intersection = grammar.variables.intersection(grammar.terminals)
        if intersection:
            errors.append(
                f"Error: Conflicto entre variables y terminales. Los siguientes símbolos están en ambos conjuntos: {intersection}."
            )

        # 6. Al menos una producción
        if not grammar.productions:
            errors.append("Error: No se registraron reglas de producción en la gramática.")

        # 7. Validar cada producción
        valid_symbols = grammar.variables.union(grammar.terminals).union({Production.EPSILON})
        
        for idx, prod in enumerate(grammar.productions, start=1):
            # Lado izquierdo debe pertenecer a V
            if prod.left not in grammar.variables:
                errors.append(
                    f"Error en producción #{idx} ({prod}): El lado izquierdo '{prod.left}' no fue declarado como variable."
                )

            # Lado derecho no debe estar vacío
            if not prod.right:
                errors.append(
                    f"Error en producción #{idx} ({prod.left} ->): El lado derecho no contiene ningún símbolo."
                )

            # Validar que cada símbolo del lado derecho exista en V o T o sea ε
            for symbol in prod.right:
                if symbol not in valid_symbols:
                    if symbol.isupper():
                        errors.append(
                            f"Error en producción {prod.left} -> {' '.join(prod.right)}: La variable '{symbol}' no fue declarada en V."
                        )
                    else:
                        errors.append(
                            f"Error en producción {prod.left} -> {' '.join(prod.right)}: El símbolo terminal '{symbol}' no fue declarado en T."
                        )

            # Si produce epsilon, no debe estar acompañado de otros símbolos en la misma producción (ej: S -> ε A es inválido)
            if Production.EPSILON in prod.right and len(prod.right) > 1:
                errors.append(
                    f"Error en producción {prod.left} -> {' '.join(prod.right)}: La cadena vacía (ε) no puede combinarse con otros símbolos en la misma regla."
                )

        # Advertencia: Variables declaradas pero sin producciones en su lado izquierdo
        vars_with_prods = {p.left for p in grammar.productions}
        vars_without_prods = grammar.variables - vars_with_prods
        if vars_without_prods:
            warnings.append(
                f"Las siguientes variables fueron declaradas pero no tienen producciones asociadas: {vars_without_prods}."
            )

        is_valid = len(errors) == 0
        return GrammarValidationResult(is_valid, errors, warnings)
