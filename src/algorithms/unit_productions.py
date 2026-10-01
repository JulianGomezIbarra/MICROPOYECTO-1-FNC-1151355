"""
Algoritmo de Identificación y Eliminación de Producciones Unitarias.
"""
from typing import Set, List, Tuple, Dict
from src.models.grammar import Grammar
from src.models.production import Production
from src.history.transformation_step import TransformationStep


class UnitProductionsEliminator:
    """
    Identifica producciones unitarias (A -> B con B en V)
    y las sustituye por las reglas equivalentes calculando la clausura unitaria.
    """

    @classmethod
    def find_unit_pairs(cls, grammar: Grammar) -> Set[Tuple[str, str]]:
        """
        Calcula todos los pares unitarios (A, B) tales que A =>* B usando producciones unitarias.
        Paso 1: (A, A) para todo A en V (reflexividad).
        Paso 2: Si (A, B) es un par y existe B -> C en P con C en V, agregar (A, C).
        """
        # Pares unitarios reflexivos iniciales
        pairs: Set[Tuple[str, str]] = set()
        for var in grammar.variables:
            pairs.add((var, var))

        # Producciones unitarias directas
        unit_prods = [p for p in grammar.productions if p.is_unit(grammar.variables)]

        # Clausura transitiva (punto fijo)
        changed = True
        while changed:
            changed = False
            for a, b in list(pairs):
                for p in unit_prods:
                    if p.left == b:
                        target = p.right[0]
                        if (a, target) not in pairs:
                            pairs.add((a, target))
                            changed = True

        return pairs

    @classmethod
    def eliminate(cls, grammar: Grammar) -> Tuple[Grammar, TransformationStep]:
        """
        Elimina las producciones unitarias:
        1. Halla los pares unitarios (A, B).
        2. Para cada par (A, B), si B -> alfa es una producción no unitaria, se agrega A -> alfa.
        3. Se eliminan todas las reglas unitarias A -> B.
        """
        initial_grammar = grammar.clone()
        unit_pairs = cls.find_unit_pairs(grammar)

        # Reglas unitarias a eliminar
        unit_prods_to_remove = [
            p for p in grammar.productions if p.is_unit(grammar.variables)
        ]

        # Reglas no unitarias por variable
        non_unit_prods_by_var: Dict[str, List[Tuple[str, ...]]] = {
            v: [] for v in grammar.variables
        }
        for p in grammar.productions:
            if not p.is_unit(grammar.variables):
                if p.right not in non_unit_prods_by_var[p.left]:
                    non_unit_prods_by_var[p.left].append(p.right)

        added_productions: List[Production] = []
        new_productions_set: Set[Production] = set()

        # Para cada par (A, B), agregamos A -> alfa para cada B -> alfa no unitaria
        for a, b in unit_pairs:
            for right in non_unit_prods_by_var.get(b, []):
                new_prod = Production(a, right)
                if new_prod not in grammar.productions and new_prod not in added_productions:
                    added_productions.append(new_prod)
                new_productions_set.add(new_prod)

        # Construir gramática resultante
        result_grammar = Grammar(
            variables=set(grammar.variables),
            terminals=set(grammar.terminals),
            productions=list(new_productions_set),
            start_symbol=grammar.start_symbol,
        )

        # Filtramos para mostrar los pares no triviales (A != B)
        non_trivial_pairs = {p for p in unit_pairs if p[0] != p[1]}
        formatted_pairs = [f"({a} =>* {b})" for a, b in sorted(list(non_trivial_pairs))]

        step = TransformationStep(
            stage_name="Eliminación de producciones unitarias (A -> B)",
            initial_grammar=initial_grammar,
            identified_elements=formatted_pairs if formatted_pairs else ["(No hay pares unitarios)"],
            removed_productions=unit_prods_to_remove,
            added_productions=added_productions,
            result_grammar=result_grammar,
            description=(
                f"Se detectaron {len(unit_prods_to_remove)} producción(es) unitaria(s) y "
                f"{len(non_trivial_pairs)} par(es) unitario(s) no trivial(es). "
                f"Se sustituyeron por las producciones no unitarias equivalentes."
            ),
        )

        return result_grammar, step
