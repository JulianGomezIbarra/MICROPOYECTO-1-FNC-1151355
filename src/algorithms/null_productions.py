"""
Algoritmo de Identificación y Eliminación de Producciones Nulas.
"""
from typing import Set, List, Tuple
from itertools import product
from src.models.grammar import Grammar
from src.models.production import Production
from src.history.transformation_step import TransformationStep


class NullProductionsEliminator:
    """
    Identifica variables anulables (que pueden derivar en ε)
    y elimina las producciones nulas generando las reglas equivalentes.
    """

    @classmethod
    def find_nullable_variables(cls, grammar: Grammar) -> Set[str]:
        """
        Determina inductivamente el conjunto V_null de variables anulables:
        Paso 1: V_null_0 = { A in V | A -> ε in P }
        Paso 2: Repetir hasta punto fijo:
                Si existe A -> Y1 Y2 ... Yk tal que Y_i in V_null para todo i,
                entonces agregar A a V_null.
        """
        nullable: Set[str] = set()

        # Paso base: reglas directas a epsilon
        for prod in grammar.productions:
            if prod.is_epsilon():
                nullable.add(prod.left)

        # Paso inductivo: punto fijo
        changed = True
        while changed:
            changed = False
            for prod in grammar.productions:
                if prod.left not in nullable and not prod.is_epsilon():
                    # Comprobar si todos los símbolos del lado derecho son variables anulables
                    if prod.right and all(sym in nullable for sym in prod.right):
                        nullable.add(prod.left)
                        changed = True

        return nullable

    @classmethod
    def eliminate(cls, grammar: Grammar) -> Tuple[Grammar, TransformationStep]:
        """
        Ejecuta el proceso completo de eliminación de producciones nulas:
        1. Halla las variables anulables.
        2. Para cada regla A -> alfa, genera todas las variantes combinatorias
           omitiendo variables anulables.
        3. Elimina las reglas A -> ε.
        4. Registra el paso de transformación.
        """
        initial_grammar = grammar.clone()
        nullable_vars = cls.find_nullable_variables(grammar)

        removed_productions: List[Production] = []
        added_productions: List[Production] = []
        new_productions_set: Set[Production] = set()

        # Identificar las producciones nulas directas que se eliminarán
        for prod in grammar.productions:
            if prod.is_epsilon():
                removed_productions.append(prod)

        # Generar combinaciones para cada producción no nula
        for prod in grammar.productions:
            if prod.is_epsilon():
                continue

            right_symbols = prod.right
            # Encontrar índices donde aparecen variables anulables
            nullable_indices = [i for i, s in enumerate(right_symbols) if s in nullable_vars]

            if not nullable_indices:
                # No contiene variables anulables, se conserva tal cual
                new_productions_set.add(prod)
                continue

            # Generar combinaciones (conservar o eliminar cada posición anulable)
            # Para cada posición anulable, podemos elegir incluirla (True) o excluirla (False)
            choices = product([True, False], repeat=len(nullable_indices))
            for choice in choices:
                # Construir el lado derecho según la combinación
                # Mapa de exclusión:
                exclude_pos = set(
                    nullable_indices[i] for i, keep in enumerate(choice) if not keep
                )

                new_right = tuple(
                    sym for idx, sym in enumerate(right_symbols) if idx not in exclude_pos
                )

                # Si el nuevo lado derecho quedó vacío, equivale a producir epsilon (la omitimos)
                if not new_right:
                    continue

                new_prod = Production(prod.left, new_right)
                if new_prod not in grammar.productions:
                    if new_prod not in added_productions:
                        added_productions.append(new_prod)
                new_productions_set.add(new_prod)

        # Construir la nueva gramática resultante
        result_grammar = Grammar(
            variables=set(grammar.variables),
            terminals=set(grammar.terminals),
            productions=list(new_productions_set),
            start_symbol=grammar.start_symbol,
        )

        step = TransformationStep(
            stage_name="Eliminación de producciones nulas (ε)",
            initial_grammar=initial_grammar,
            identified_elements=nullable_vars,
            removed_productions=removed_productions,
            added_productions=added_productions,
            result_grammar=result_grammar,
            description=(
                f"Se identificaron {len(nullable_vars)} variable(s) anulable(s): {sorted(list(nullable_vars))}. "
                f"Se eliminaron las producciones directas a ε y se generaron las combinaciones equivalentes."
            ),
        )

        return result_grammar, step
