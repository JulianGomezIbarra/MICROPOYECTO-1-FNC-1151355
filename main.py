"""
Punto de Entrada Principal (Main)
Microproyecto #1: Depuración y Conversión de GLC a Forma Normal de Chomsky
Universidad Francisco de Paula Santander (UFPS)
Teoría de la Computación 2026/02
"""
import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Compatibilidad de codificación en Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.ui.console_menu import ConsoleMenu
from src.ui.gui_app import run_gui


def main():
    """Función principal de inicio del aplicativo."""
    if "--cli" in sys.argv or "--consola" in sys.argv:
        try:
            menu = ConsoleMenu()
            menu.run()
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario. Saliendo...")
            sys.exit(0)
    else:
        # Por defecto abre la GUI de escritorio
        try:
            run_gui()
        except Exception:
            # Si falla el entorno gráfico, fallback a consola
            menu = ConsoleMenu()
            menu.run()


if __name__ == "__main__":
    main()
