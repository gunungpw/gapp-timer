import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
)
from PySide6.QtCore import QTimer, QTime
from PySide6.QtGui import QFont, Qt


class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("gapp-timer")
        self.setGeometry(100, 100, 400, 200)

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Timer display
        self.time_label = QLabel("00:00")
        self.time_label.setFont(QFont("Arial", 48))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.time_label)

        # Input fields for minutes and seconds
        self.input_layout = QHBoxLayout()
        self.min_input = QLineEdit("0")
        self.min_input.setPlaceholderText("Minutes")
        self.sec_input = QLineEdit("0")
        self.sec_input.setPlaceholderText("Seconds")
        self.input_layout.addWidget(self.min_input)
        self.input_layout.addWidget(self.sec_input)
        self.layout.addLayout(self.input_layout)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.pause_button = QPushButton("Pause")
        self.reset_button = QPushButton("Reset")
        self.set_button = QPushButton("Set Timer")
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.pause_button)
        self.button_layout.addWidget(self.reset_button)
        self.button_layout.addWidget(self.set_button)
        self.layout.addLayout(self.button_layout)

        # Timer setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_left = QTime(0, 0, 0)
        self.timer_running = False

        # Connect buttons to functions
        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.reset_button.clicked.connect(self.reset_timer)
        self.set_button.clicked.connect(self.set_timer)

    def start_timer(self):
        if not self.timer_running and self.time_left > QTime(0, 0, 0):
            self.timer.start(1000)  # Update every second
            self.timer_running = True
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.set_button.setEnabled(False)

    def pause_timer(self):
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.set_button.setEnabled(True)

    def reset_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.time_left = QTime(0, 0, 0)
        self.time_label.setText("00:00")
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.set_button.setEnabled(True)

    def set_timer(self):
        try:
            minutes = int(self.min_input.text()) if self.min_input.text() else 0
            seconds = int(self.sec_input.text()) if self.sec_input.text() else 0
            if minutes >= 0 and seconds >= 0:
                self.time_left = QTime(0, minutes, seconds)
                self.time_label.setText(self.time_left.toString("mm:ss"))
                self.start_button.setEnabled(True)
                self.pause_button.setEnabled(False)
        except ValueError:
            self.time_label.setText("Invalid input")

    def update_timer(self):
        self.time_left = self.time_left.addSecs(-1)
        self.time_label.setText(self.time_left.toString("mm:ss"))
        if self.time_left == QTime(0, 0, 0):
            self.timer.stop()
            self.timer_running = False
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.set_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec())
