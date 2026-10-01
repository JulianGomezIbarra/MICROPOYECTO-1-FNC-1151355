"""
Conversión a Forma Normal de Chomsky (FNC).
"""
from typing import Set, List, Tuple, Dict
from src.models.grammar import Grammar
from src.models.production import Production
from src.history.transformation_step import TransformationStep


class ChomskyConverter:
    """
    Realiza las transformaciones estructurales para que la gramática cumpla FNC:
    1. Sustitución de símbolos terminales en producciones de longitud >= 2.
    2. Binarización / reducción de producciones con longitud > 2.
    3. Generación determinista y única de variables auxiliares.
    """

    @classmethod
    def _generate_new_variable_name(cls, prefix: str, existing_vars: Set[str], counter: int) -> Tuple[str, int]:
        """
        Genera un nombre único de variable auxiliar que no exista en el conjunto.
        """
        current_counter = counter
        while True:
            candidate = f"{prefix}{current_counter}"
            if candidate not in existing_vars:
                return candidate, current_counter + 1
            current_counter += 1

    @classmethod
    def substitute_terminals(cls, grammar: Grammar) -> Tuple[Grammar, TransformationStep]:
        """
        En producciones de longitud >= 2, sustituye los símbolos terminales
        por nuevas variables auxiliares que produzcan exclusivamente ese terminal.
        Ejemplo: Si S -> aB, se crea X_a -> a y la regla queda S -> X_a B.
        """
        initial_grammar = grammar.clone()
        new_vars = set(grammar.variables)
        existing_vars = set(grammar.variables)
        terminal_var_map: Dict[str, str] = {}  # 'a' -> 'X_a' o 'T1'
        
        aux_counter = 1
        removed_productions: List[Production] = []
        added_productions: List[Production] = []
        updated_productions: List[Production] = []

        # 1. Identificar terminales que requieren variable auxiliar
        terminals_to_replace: Set[str] = set()
        for prod in grammar.productions:
            if len(prod.right) >= 2:
                for sym in prod.right:
                    if sym in grammar.terminals:
                        terminals_to_replace.add(sym)

        # 2. Asignar variable auxiliar para cada terminal
        for term in sorted(list(terminals_to_replace)):
            # Buscamos un nombre mnemotécnico o X1, X2...
            var_name, aux_counter = cls._generate_new_variable_name("X", existing_vars, aux_counter)
            existing_vars.add(var_name)
            new_vars.add(var_name)
            terminal_var_map[term] = var_name
            # Agregamos la regla Xi -> a
            aux_prod = Production(var_name, (term,))
            added_productions.append(aux_prod)
            updated_productions.append(aux_prod)

        # 3. Reescribir producciones
        for prod in grammar.productions:
            if len(prod.right) >= 2 and any(sym in terminals_to_replace for sym in prod.right):
                removed_productions.append(prod)
                new_right = tuple(
                    terminal_var_map[sym] if sym in terminal_var_map else sym
                    for sym in prod.right
                )
                new_prod = Production(prod.left, new_right)
                if new_prod not in added_productions:
                    added_productions.append(new_prod)
                updated_productions.append(new_prod)
            else:
                updated_productions.append(prod)

        result_grammar = Grammar(
            variables=new_vars,
            terminals=set(grammar.terminals),
            productions=updated_productions,
            start_symbol=grammar.start_symbol,
        )

        elements_desc = [f"{t} -> {var}" for t, var in sorted(terminal_var_map.items())]

        step = TransformationStep(
            stage_name="Sustitución de terminales en producciones compuestas",
            initial_grammar=initial_grammar,
            identified_elements=elements_desc if elements_desc else ["(Ningún terminal en producciones compuestas)"],
            removed_productions=removed_productions,
            added_productions=added_productions,
            result_grammar=result_grammar,
            description=(
                f"Se sustituyeron los terminales en reglas de longitud >= 2 por variables auxiliares. "
                f"Variables creadas: {list(terminal_var_map.values())}."
            ),
        )

        return result_grammar, step

    @classmethod
    def reduce_long_productions(cls, grammar: Grammar) -> Tuple[Grammar, TransformationStep]:
        """
        Convierte producciones con más de 2 variables en producciones binarias.
        Ejemplo: A -> B C D  se transforma en:
                 A -> B X_1
                 X_1 -> C D
        """
        initial_grammar = grammar.clone()
        new_vars = set(grammar.variables)
        existing_vars = set(grammar.variables)
        aux_counter = 1

        removed_productions: List[Production] = []
        added_productions: List[Production] = []
        final_productions: List[Production] = []

        long_productions = [p for p in grammar.productions if len(p.right) > 2]

        for prod in grammar.productions:
            if len(prod.right) <= 2:
                final_productions.append(prod)
            else:
                removed_productions.append(prod)
                # Binarización en cascada
                symbols = list(prod.right)
                current_left = prod.left

                # Procesamos hasta que queden 2 símbolos
                while len(symbols) > 2:
                    first_sym = symbols.pop(0)
                    new_var, aux_counter = cls._generate_new_variable_name("X", existing_vars, aux_counter)
                    existing_vars.add(new_var)
                    new_vars.add(new_var)

                    # Creamos current_left -> first_sym new_var
                    p_bin = Production(current_left, (first_sym, new_var))
                    added_productions.append(p_bin)
                    final_productions.append(p_bin)

                    current_left = new_var

                # Últimos dos símbolos: current_left -> sym[-2] sym[-1]
                p_last = Production(current_left, tuple(symbols))
                added_productions.append(p_last)
                final_productions.append(p_last)

        result_grammar = Grammar(
            variables=new_vars,
            terminals=set(grammar.terminals),
            productions=final_productions,
            start_symbol=grammar.start_symbol,
        )

        step = TransformationStep(
            stage_name="Reducción de producciones largas a forma binaria (FNC)",
            initial_grammar=initial_grammar,
            identified_elements=[str(p) for p in long_productions] if long_productions else ["(No hay producciones largas > 2)"],
            removed_productions=removed_productions,
            added_productions=added_productions,
            result_grammar=result_grammar,
            description=(
                f"Se descompusieron {len(long_productions)} producción(es) de longitud superior a dos "
                f"en producciones binarias mediante nuevas variables auxiliares."
            ),
        )

        return result_grammar, step
