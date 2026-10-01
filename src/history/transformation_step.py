"""
Módulo de registro y trazabilidad paso a paso de transformaciones.
"""
from typing import List, Set, Any
from src.models.grammar import Grammar
from src.models.production import Production


class TransformationStep:
    """
    Representa una etapa individual de transformación en la gramática.
    Almacena:
    - Nombre de la etapa (ej. 'Eliminación de producciones nulas').
    - Gramática inicial de la etapa.
    - Elementos identificados en la etapa.
    - Producciones eliminadas.
    - Producciones agregadas.
    - Gramática resultante.
    - Descripción o justificación didáctica.
    """

    def __init__(
        self,
        stage_name: str,
        initial_grammar: Grammar,
        identified_elements: Any,
        removed_productions: List[Production],
        added_productions: List[Production],
        result_grammar: Grammar,
        description: str = "",
    ):
        self.stage_name: str = stage_name
        self.initial_grammar: Grammar = initial_grammar.clone()
        self.identified_elements: Any = identified_elements
        self.removed_productions: List[Production] = list(removed_productions)
        self.added_productions: List[Production] = list(added_productions)
        self.result_grammar: Grammar = result_grammar.clone()
        self.description: str = description

    def to_formatted_report(self) -> str:
        """Genera el reporte."""
        lines = []
        separator = "=" * 65
        sub_sep = "-" * 65

        lines.append(separator)
        lines.append(f"ETAPA: {self.stage_name.upper()}")
        lines.append(separator)

        if self.description:
            lines.append(f"Descripción: {self.description}")
            lines.append("")

        lines.append("1. Elementos identificados:")
        if isinstance(self.identified_elements, (set, list, tuple)):
            if not self.identified_elements:
                lines.append("   (Ninguno identificado en esta etapa)")
            else:
                formatted_elems = ", ".join(str(e) for e in sorted(list(self.identified_elements), key=lambda x: str(x)))
                lines.append(f"   {{ {formatted_elems} }}")
        else:
            lines.append(f"   {self.identified_elements}")
        lines.append("")

        lines.append("2. Producciones eliminadas:")
        if not self.removed_productions:
            lines.append("   (Ninguna producción fue eliminada)")
        else:
            for p in self.removed_productions:
                lines.append(f"   [-] {p}")
        lines.append("")

        lines.append("3. Producciones agregadas:")
        if not self.added_productions:
            lines.append("   (Ninguna producción nueva fue agregada)")
        else:
            for p in self.added_productions:
                lines.append(f"   [+] {p}")
        lines.append("")

        lines.append("4. Gramática resultante de la etapa:")
        lines.append(sub_sep)
        for line in self.result_grammar.to_formatted_string().splitlines():
            lines.append(f"   {line}")
        lines.append(sub_sep)
        lines.append("")

        return "\n".join(lines)


class HistoryManager:
    """Gestiona el historial de transformaciones."""

    def __init__(self):
        self.steps: List[TransformationStep] = []

    def add_step(self, step: TransformationStep) -> None:
        self.steps.append(step)

    def clear(self) -> None:
        self.steps.clear()

    def get_full_report(self) -> str:
        if not self.steps:
            return "No se han realizado transformaciones."
        reports = [step.to_formatted_report() for step in self.steps]
        return "\n\n".join(reports)
