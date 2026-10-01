"""
Modelo de datos formal para una Gramática Libre de Contexto (GLC)
G = (V, T, P, S)
"""
from typing import Set, List, Dict, Tuple
from src.models.production import Production


class Grammar:
    """
    Representa una Gramática Libre de Contexto formal G = (V, T, P, S)
    Donde:
        V: Conjunto finito de variables o símbolos no terminales.
        T: Conjunto finito de símbolos terminales.
        P: Conjunto finito de reglas de producción.
        S: Símbolo inicial de la gramática (S in V).
    """

    def __init__(
        self,
        variables: Set[str] = None,
        terminals: Set[str] = None,
        productions: List[Production] = None,
        start_symbol: str = "S",
    ):
        self.variables: Set[str] = set(variables) if variables else set()
        self.terminals: Set[str] = set(terminals) if terminals else set()
        self.productions: List[Production] = list(productions) if productions else []
        self.start_symbol: str = start_symbol.strip() if start_symbol else ""

    def add_variable(self, var: str) -> None:
        """Agrega una variable al conjunto V."""
        if var:
            self.variables.add(var.strip())

    def add_terminal(self, term: str) -> None:
        """Agrega un símbolo terminal al conjunto T."""
        if term:
            self.terminals.add(term.strip())

    def add_production(self, prod: Production) -> None:
        """Agrega una producción a P evitando duplicados (RNF08)."""
        if prod not in self.productions:
            self.productions.append(prod)

    def remove_production(self, prod: Production) -> None:
        """Elimina una producción de P."""
        if prod in self.productions:
            self.productions.remove(prod)

    def get_productions_for(self, variable: str) -> List[Production]:
        """Retorna todas las producciones que tienen a 'variable' en su lado izquierdo."""
        return [p for p in self.productions if p.left == variable]

    def clone(self) -> "Grammar":
        """Crea una copia profunda independiente de la gramática."""
        cloned_prods = [Production(p.left, p.right) for p in self.productions]
        return Grammar(
            variables=set(self.variables),
            terminals=set(self.terminals),
            productions=cloned_prods,
            start_symbol=self.start_symbol,
        )

    def get_grouped_productions(self) -> Dict[str, List[Tuple[str, ...]]]:
        """Agrupa las producciones por su lado izquierdo."""
        grouped: Dict[str, List[Tuple[str, ...]]] = {}
        for p in self.productions:
            if p.left not in grouped:
                grouped[p.left] = []
            if p.right not in grouped[p.left]:
                grouped[p.left].append(p.right)
        return grouped

    def to_formatted_string(self) -> str:
        """Retorna una representación textual clara y formal de la gramática."""
        lines = []
        # Ordenamos para presentación determinista y reproducible (RNF11)
        sorted_vars = sorted(list(self.variables))
        sorted_terms = sorted(list(self.terminals))
        
        lines.append(f"V = {{ {', '.join(sorted_vars)} }}")
        lines.append(f"T = {{ {', '.join(sorted_terms)} }}")
        lines.append(f"S = {self.start_symbol}")
        lines.append("P = {")
        
        grouped = self.get_grouped_productions()
        # Aseguramos que el símbolo inicial aparezca de primero en las producciones
        order_vars = [self.start_symbol] + [v for v in sorted_vars if v != self.start_symbol]
        for var in order_vars:
            if var in grouped:
                bodies = []
                for right in grouped[var]:
                    if right == (Production.EPSILON,):
                        bodies.append("ε")
                    elif any(len(s) > 1 for s in right):
                        bodies.append(" ".join(right))
                    else:
                        bodies.append("".join(right))
                lines.append(f"    {var} -> {' | '.join(bodies)}")
        
        # Cualquier otra producción de variables no listadas
        for var, right_list in sorted(grouped.items()):
            if var not in order_vars:
                bodies = []
                for right in right_list:
                    if right == (Production.EPSILON,):
                        bodies.append("ε")
                    elif any(len(s) > 1 for s in right):
                        bodies.append(" ".join(right))
                    else:
                        bodies.append("".join(right))
                lines.append(f"    {var} -> {' | '.join(bodies)}")

        lines.append("}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Grammar(V={len(self.variables)}, T={len(self.terminals)}, P={len(self.productions)}, S='{self.start_symbol}')"
