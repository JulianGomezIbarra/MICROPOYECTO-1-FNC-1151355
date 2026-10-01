"""
Validador de Forma Normal de Chomsky (FNC).
"""
from typing import List, Tuple
from src.models.grammar import Grammar
from src.models.production import Production


class FNCValidationResult:
    """Resultado de la verificación de Forma Normal de Chomsky."""

    def __init__(self, is_fnc: bool, non_compliant_productions: List[Tuple[Production, str]]):
        self.is_fnc: bool = is_fnc
        self.non_compliant: List[Tuple[Production, str]] = non_compliant_productions

    def __bool__(self) -> bool:
        return self.is_fnc

    def get_report(self) -> str:
        lines = []
        if self.is_fnc:
            lines.append("[EXITO] VERIFICACION EXITOSA: La gramatica resultante se encuentra estrictamente en Forma Normal de Chomsky (FNC).")
            lines.append("  Todas las producciones cumplen con el formato A -> BC (con B, C en V) o A -> a (con a en T).")
        else:
            lines.append(f"[NO CONFORME] La gramatica NO cumple completamente con la Forma Normal de Chomsky.")
            lines.append(f"  Se detectaron {len(self.non_compliant)} produccion(es) no conformes:")
            for prod, reason in self.non_compliant:
                lines.append(f"   • {prod} -> Motivo: {reason}")
        return "\n".join(lines)


class FNCValidator:
    """Verifica si una gramática dada se encuentra en Forma Normal de Chomsky."""

    @classmethod
    def validate(cls, grammar: Grammar) -> FNCValidationResult:
        non_compliant: List[Tuple[Production, str]] = []

        for prod in grammar.productions:
            # Caso 1: A -> a (longitud 1 con símbolo terminal)
            if len(prod.right) == 1:
                sym = prod.right[0]
                if sym not in grammar.terminals:
                    if sym in grammar.variables:
                        non_compliant.append((prod, f"Es una producción unitaria ({prod.left} -> {sym}); no permitida en FNC."))
                    elif sym == Production.EPSILON:
                        non_compliant.append((prod, "Es una producción nula (ε); no permitida en FNC pura."))
                    else:
                        non_compliant.append((prod, f"El símbolo '{sym}' no es un terminal declarado."))
            # Caso 2: A -> BC (longitud 2 con variables)
            elif len(prod.right) == 2:
                b, c = prod.right[0], prod.right[1]
                if b not in grammar.variables:
                    non_compliant.append((prod, f"El primer símbolo '{b}' no es una variable no terminal."))
                elif c not in grammar.variables:
                    non_compliant.append((prod, f"El segundo símbolo '{c}' no es una variable no terminal."))
            # Caso 3: Longitud mayor a 2 o vacía
            else:
                non_compliant.append(
                    (prod, f"La longitud del lado derecho es {len(prod.right)}; en FNC debe ser exactamente 1 (terminal) o 2 (variables).")
                )

        return FNCValidationResult(len(non_compliant) == 0, non_compliant)
