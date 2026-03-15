"""PySide6 GUI components."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

from triple_a.config import Settings


class MainWindow(QMainWindow):
    """Main application window."""

    signal_request_rebalance = Signal(float)

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        self.setWindowTitle("Triple A - Active Asset Allocation")
        self._setup_ui()

    def _setup_ui(self) -> None:
        self._status_label = QLabel("Initializing...")

        self._force_rebalance_button = QPushButton("Force Rebalance")
        self._force_rebalance_button.clicked.connect(self._on_force_rebalance)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._status_label)
        main_layout.addWidget(self._force_rebalance_button)

        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

    @Slot()
    def _on_force_rebalance(self) -> None:
        self.signal_request_rebalance.emit(self.settings.deviation_threshold)

    def update_status(self, text: str) -> None:
        self._status_label.setText(text)
