"""
Parser y lector de Gramáticas Libres de Contexto (GLC)
"""
from typing import Set, List, Tuple
from src.models.grammar import Grammar
from src.models.production import Production


class GrammarParser:
    """
    Permite parsear gramáticas a partir de cadenas de texto, archivos o entradas de usuario.
    Soporta formato con tuberías (S -> AB | a | ε) y formato de una producción por línea.
    """

    @staticmethod
    def parse_symbol_list(input_str: str) -> Set[str]:
        """
        Convierte una cadena como 'S, A, B' o 'S A B' o 'a, b' en un conjunto de símbolos.
        """
        cleaned = input_str.replace(",", " ").strip()
        return set(s.strip() for s in cleaned.split() if s.strip())

    @classmethod
    def parse_production_line(cls, line: str) -> Tuple[str, List[Tuple[str, ...]]]:
        """
        Parsea una línea como:
        'S -> AB | a | ε' o 'S -> A B | a'
        Retorna (lado_izquierdo, lista_de_lados_derechos)
        """
        line = line.strip()
        if not line or line.startswith("#"):
            return ("", [])

        if "->" not in line and "::=" not in line:
            raise ValueError(f"Formato de producción inválido (falta '->' o '::='): {line}")

        separator = "->" if "->" in line else "::="
        parts = line.split(separator, 1)
        left = parts[0].strip()
        right_raw = parts[1].strip()

        alternatives = [alt.strip() for alt in right_raw.split("|")]
        rights: List[Tuple[str, ...]] = []

        for alt in alternatives:
            if not alt or alt in (Production.EPSILON, "epsilon", "lambda", "λ"):
                rights.append((Production.EPSILON,))
            elif " " in alt:
                # Separado por espacios explícitos
                symbols = tuple(s for s in alt.split() if s)
                rights.append(symbols)
            else:
                # Sin espacios: cada caracter es un símbolo
                symbols = tuple(alt)
                rights.append(symbols)

        return (left, rights)

    @classmethod
    def from_text_definition(cls, text: str) -> Grammar:
        """
        Parsea una definición completa de gramática en formato texto.
        Ejemplo:
            Variables: S, A, B
            Terminales: a, b
            Inicial: S
            Producciones:
            S -> ASA | aB | ε
            A -> B
            B -> b
        """
        variables: Set[str] = set()
        terminals: Set[str] = set()
        start_symbol: str = ""
        productions: List[Production] = []

        lines = [line.strip() for line in text.strip().splitlines() if line.strip() and not line.strip().startswith("#")]

        in_productions_section = False

        for line in lines:
            lower = line.lower()
            if lower.startswith("variables:") or lower.startswith("v =") or lower.startswith("v:"):
                val = line.split(":", 1)[-1] if ":" in line else line.split("=", 1)[-1]
                val = val.replace("{", "").replace("}", "")
                variables.update(cls.parse_symbol_list(val))
            elif lower.startswith("terminales:") or lower.startswith("terminals:") or lower.startswith("t =") or lower.startswith("t:"):
                val = line.split(":", 1)[-1] if ":" in line else line.split("=", 1)[-1]
                val = val.replace("{", "").replace("}", "")
                terminals.update(cls.parse_symbol_list(val))
            elif lower.startswith("inicial:") or lower.startswith("inicio:") or lower.startswith("s =") or lower.startswith("s:"):
                val = line.split(":", 1)[-1] if ":" in line else line.split("=", 1)[-1]
                start_symbol = val.strip()
            elif lower.startswith("producciones:") or lower.startswith("p =") or lower.startswith("p:"):
                in_productions_section = True
            elif "->" in line or "::=" in line:
                left, right_list = cls.parse_production_line(line)
                if left:
                    for right in right_list:
                        productions.append(Production(left, right))

        # Si el símbolo inicial no fue declarado explícitamente pero hay producciones, tomamos la primera
        if not start_symbol and productions:
            start_symbol = productions[0].left

        # Si variables o terminales no se especificaron explícitamente, se pueden inferir:
        if not variables:
            variables = {p.left for p in productions}
        if not terminals:
            all_symbols = set()
            for p in productions:
                for s in p.right:
                    if s != Production.EPSILON:
                        all_symbols.add(s)
            terminals = all_symbols - variables

        return Grammar(
            variables=variables,
            terminals=terminals,
            productions=productions,
            start_symbol=start_symbol,
        )
