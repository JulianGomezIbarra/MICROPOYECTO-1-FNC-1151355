"""
Algoritmos de Identificación y Eliminación de Variables Inútiles e Inalcanzables.
"""
from typing import Set, List, Tuple
from collections import deque
from src.models.grammar import Grammar
from src.models.production import Production
from src.history.transformation_step import TransformationStep


class UselessSymbolsEliminator:
    """
    Gestiona la depuración de variables inútiles:
    1. Fase 1: Identificación y eliminación de variables NO generadoras.
    2. Fase 2: Identificación y eliminación de variables INALCANZABLES.
    """

    @classmethod
    def find_generating_variables(cls, grammar: Grammar) -> Set[str]:
        """
        Determina las variables generadoras (aquellas que derivan en w in T*):
        Paso 1: V_gen_0 = { A in V | A -> w con w in (T U {ε})* }
        Paso 2: Repetir hasta punto fijo:
                Si A -> alfa y todos los símbolos de alfa están en (T U V_gen),
                entonces agregar A a V_gen.
        """
        generating: Set[str] = set()

        # Paso inductivo hasta punto fijo
        changed = True
        while changed:
            changed = False
            for prod in grammar.productions:
                if prod.left not in generating:
                    # Comprobar si todos los símbolos del lado derecho son terminales, epsilon o ya generadores
                    is_gen = True
                    for sym in prod.right:
                        if sym == Production.EPSILON:
                            continue
                        if sym in grammar.terminals:
                            continue
                        if sym in generating:
                            continue
                        # Si es una variable no generadora todavía o símbolo desconocido
                        is_gen = False
                        break

                    if is_gen:
                        generating.add(prod.left)
                        changed = True

        return generating

    @classmethod
    def eliminate_non_generating(cls, grammar: Grammar) -> Tuple[Grammar, TransformationStep]:
        """
        Elimina las variables no generadoras y toda producción que las contenga.
        """
        initial_grammar = grammar.clone()
        generating = cls.find_generating_variables(grammar)
        non_generating = grammar.variables - generating

        removed_productions: List[Production] = []
        valid_productions: List[Production] = []

        for prod in grammar.productions:
            # Si el lado izquierdo no es generador, se elimina
            if prod.left not in generating:
                removed_productions.append(prod)
                continue

            # Si algún símbolo del lado derecho es una variable no generadora, se elimina
            has_non_gen = any(sym in non_generating for sym in prod.right)
            if has_non_gen:
                removed_productions.append(prod)
            else:
                valid_productions.append(prod)

        # Nueva lista de variables: solo las generadoras
        new_variables = set(generating)

        # Actualizar terminales activos
        active_terminals = set()
        for p in valid_productions:
            for s in p.right:
                if s in grammar.terminals:
                    active_terminals.add(s)

        result_grammar = Grammar(
            variables=new_variables,
            terminals=active_terminals if active_terminals else set(grammar.terminals),
            productions=valid_productions,
            start_symbol=grammar.start_symbol,
        )

        step = TransformationStep(
            stage_name="Eliminación de variables inútiles (no generadoras)",
            initial_grammar=initial_grammar,
            identified_elements=non_generating if non_generating else set(),
            removed_productions=removed_productions,
            added_productions=[],
            result_grammar=result_grammar,
            description=(
                f"Variables generadoras identificadas: {sorted(list(generating))}. "
                f"Variables no generadoras (inútiles) eliminadas: {sorted(list(non_generating))}. "
                f"Se eliminaron {len(removed_productions)} producción(es) asociadas."
            ),
        )

        return result_grammar, step

    @classmethod
    def find_reachable_variables(cls, grammar: Grammar) -> Set[str]:
        """
        Determina las variables y símbolos alcanzables a partir del símbolo inicial S.
        Utiliza una búsqueda en anchura (BFS) comenzando desde S.
        """
        if not grammar.start_symbol or grammar.start_symbol not in grammar.variables:
            return set()

        reachable_vars: Set[str] = {grammar.start_symbol}
        queue = deque([grammar.start_symbol])

        while queue:
            current_var = queue.popleft()
            for prod in grammar.get_productions_for(current_var):
                for sym in prod.right:
                    if sym in grammar.variables and sym not in reachable_vars:
                        reachable_vars.add(sym)
                        queue.append(sym)

        return reachable_vars

    @classmethod
    def eliminate_unreachable(cls, grammar: Grammar) -> Tuple[Grammar, TransformationStep]:
        """
        Elimina las variables no alcanzables desde el símbolo inicial.
        """
        initial_grammar = grammar.clone()
        reachable_vars = cls.find_reachable_variables(grammar)
        unreachable_vars = grammar.variables - reachable_vars

        removed_productions: List[Production] = []
        valid_productions: List[Production] = []

        for prod in grammar.productions:
            if prod.left in unreachable_vars or any(sym in unreachable_vars for sym in prod.right):
                removed_productions.append(prod)
            else:
                valid_productions.append(prod)

        # Terminales activos
        active_terminals = set()
        for p in valid_productions:
            for s in p.right:
                if s in grammar.terminals:
                    active_terminals.add(s)

        result_grammar = Grammar(
            variables=set(reachable_vars),
            terminals=active_terminals if active_terminals else set(grammar.terminals),
            productions=valid_productions,
            start_symbol=grammar.start_symbol,
        )

        step = TransformationStep(
            stage_name="Eliminación de variables inalcanzables",
            initial_grammar=initial_grammar,
            identified_elements=unreachable_vars if unreachable_vars else set(),
            removed_productions=removed_productions,
            added_productions=[],
            result_grammar=result_grammar,
            description=(
                f"Variables alcanzables desde '{grammar.start_symbol}': {sorted(list(reachable_vars))}. "
                f"Variables inalcanzables eliminadas: {sorted(list(unreachable_vars))}. "
                f"Se eliminaron {len(removed_productions)} producción(es) que no podían ser accedidas."
            ),
        )

        return result_grammar, step
