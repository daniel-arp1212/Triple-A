"""Entry point for the Triple A framework."""

import sys

from PySide6.QtWidgets import QApplication

from triple_a.config import load_settings
from triple_a.gui import MainWindow


def main() -> int:
    settings = load_settings()

    app = QApplication(sys.argv)
    window = MainWindow(settings=settings)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
