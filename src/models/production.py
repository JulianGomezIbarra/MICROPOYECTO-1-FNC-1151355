"""
Modelos de datos para Gramáticas Libres de Contexto (GLC)
"""
from typing import List, Tuple, Set


class Production:
    """
    Representa una regla de producción de la forma A -> alfa,
    donde A es un símbolo no terminal (variable) y alfa es una secuencia
    de símbolos (terminales y/o variables), o la cadena vacía ('ε' o 'epsilon').
    """
    EPSILON = "ε"

    def __init__(self, left: str, right: Tuple[str, ...]):
        self.left: str = left.strip()
        # Normalizamos: si la tupla está vacía o contiene epsilon/ε, se estandariza a ('ε',)
        cleaned_right: List[str] = [sym.strip() for sym in right if sym.strip()]
        if not cleaned_right or cleaned_right == ["ε"] or cleaned_right == ["epsilon"] or cleaned_right == ["lambda"] or cleaned_right == ["λ"]:
            self.right: Tuple[str, ...] = (self.EPSILON,)
        else:
            self.right = tuple(cleaned_right)

    @classmethod
    def from_string(cls, left: str, right_str: str) -> "Production":
        """
        Crea una producción a partir de una cadena para el lado derecho.
        Si la cadena tiene espacios (ej. 'A B' o 'a B'), se separa por espacios.
        Si no tiene espacios pero tiene varios caracteres (ej. 'AB'), cada caracter es un símbolo.
        """
        right_str = right_str.strip()
        if not right_str or right_str in (cls.EPSILON, "epsilon", "lambda", "λ"):
            return cls(left, (cls.EPSILON,))
        
        # Si tiene espacios, dividimos por espacios
        if " " in right_str:
            symbols = tuple(s for s in right_str.split() if s)
        else:
            symbols = tuple(right_str)
        return cls(left, symbols)

    def is_epsilon(self) -> bool:
        """Determina si la producción es nula (A -> ε)."""
        return len(self.right) == 1 and self.right[0] == self.EPSILON

    def is_unit(self, variables: Set[str]) -> bool:
        """Determina si la producción es unitaria (A -> B con B perteneciente a V)."""
        return len(self.right) == 1 and self.right[0] in variables

    def is_terminal_only(self, terminals: Set[str]) -> bool:
        """Determina si la producción produce un solo símbolo terminal (A -> a)."""
        return len(self.right) == 1 and self.right[0] in terminals

    def is_binary_variables(self, variables: Set[str]) -> bool:
        """Determina si la producción produce exactamente dos variables (A -> BC)."""
        return (
            len(self.right) == 2
            and self.right[0] in variables
            and self.right[1] in variables
        )

    def is_in_chomsky_form(self, variables: Set[str], terminals: Set[str]) -> bool:
        """
        Comprueba si la producción cumple la Forma Normal de Chomsky:
        A -> BC  (con B, C en V)  ó  A -> a  (con a en T).
        """
        return self.is_terminal_only(terminals) or self.is_binary_variables(variables)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Production):
            return False
        return self.left == other.left and self.right == other.right

    def __hash__(self) -> int:
        return hash((self.left, self.right))

    def __repr__(self) -> str:
        return f"{self.left} -> {' '.join(self.right)}"

    def to_string_compact(self) -> str:
        """Representación compacta sin espacios si son caracteres simples."""
        if self.is_epsilon():
            return f"{self.left} -> ε"
        # Si los símbolos tienen longitud mayor a 1, usamos espacios para claridad
        if any(len(sym) > 1 for sym in self.right):
            return f"{self.left} -> {' '.join(self.right)}"
        return f"{self.left} -> {''.join(self.right)}"
