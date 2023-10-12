import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

# Create a QApplication
app = QApplication(sys.argv)

# Enable high-DPI scaling
app.setAttribute(Qt.AA_EnableHighDpiScaling)

# Create a simple window with a button
window = QMainWindow()
button = QPushButton("Hello, PyQt!")
window.setCentralWidget(button)
window.show()

# Start the application event loop
sys.exit(app.exec_())
