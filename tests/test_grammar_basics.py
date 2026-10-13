"""
Pruebas unitarias para modelos, parser y validador de Gramática Libre de Contexto.
"""
import unittest
import sys
import os

# Asegurar que src esté en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.grammar import Grammar
from src.models.production import Production
from src.parser.grammar_parser import GrammarParser
from src.parser.validator import GrammarValidator


class TestGrammarBasics(unittest.TestCase):

    def test_production_creation(self):
        p1 = Production("S", ("A", "B"))
        self.assertEqual(p1.left, "S")
        self.assertEqual(p1.right, ("A", "B"))
        self.assertFalse(p1.is_epsilon())

        p_eps = Production("A", ("ε",))
        self.assertTrue(p_eps.is_epsilon())

    def test_grammar_validation_valid(self):
        text = """
        Variables: S, A, B
        Terminales: a, b
        Inicial: S
        Producciones:
        S -> AB | a
        A -> a
        B -> b
        """
        g = GrammarParser.from_text_definition(text)
        result = GrammarValidator.validate(g)
        self.assertTrue(result.is_valid, msg=result.get_summary())

    def test_grammar_validation_unknown_symbol(self):
        # La variable D y terminal c no fueron declarados
        g = Grammar(
            variables={"S", "A"},
            terminals={"a", "b"},
            start_symbol="S",
            productions=[
                Production("S", ("A", "D")),  # D no declarada
                Production("A", ("c",)),      # c no declarada
            ]
        )
        result = GrammarValidator.validate(g)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("D" in err for err in result.errors))
        self.assertTrue(any("c" in err for err in result.errors))

    def test_grammar_validation_invalid_start_symbol(self):
        g = Grammar(
            variables={"S", "A"},
            terminals={"a"},
            start_symbol="X",  # X no pertenece a V
            productions=[Production("S", ("a",))]
        )
        result = GrammarValidator.validate(g)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("X" in err for err in result.errors))

    def test_case_sensitivity_variables_lowercase(self):
        # Variables declaradas en minúsculas deben ser válidas si coinciden exactamente
        text = """
        Variables: s, a, b
        Terminales: 0, 1
        Inicial: s
        Producciones:
        s -> a b | 0
        a -> 0
        b -> 1
        """
        g = GrammarParser.from_text_definition(text)
        result = GrammarValidator.validate(g)
        self.assertTrue(result.is_valid, msg=result.get_summary())

    def test_case_sensitivity_mismatch(self):
        # Variable declarada como 's' pero en producciones se usó 'S'
        text = """
        Variables: s, a
        Terminales: 0
        Inicial: s
        Producciones:
        S -> a
        a -> 0
        """
        g = GrammarParser.from_text_definition(text)
        result = GrammarValidator.validate(g)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("sensible a mayúsculas" in err for err in result.errors))


if __name__ == "__main__":
    unittest.main()

