import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit

MESSAGE_LIMIT = 256

class MainWindow(QMainWindow):
     def __init__(self):
          super().__init__()

          self.setWindowTitle("qChat")
          self.setWindowIcon(QIcon("icon.png"))
          self.setFixedSize(QSize(600, 500))

          sendBtn = QPushButton("Send")
          sendBtn.clicked.connect(self.send_message)

          self.textField = QLineEdit()
          self.textField.setMaxLength(MESSAGE_LIMIT)
          self.textField.setPlaceholderText("Enter your text")
          self.textField.returnPressed.connect(self.send_message)

          self.chat_history = QTextEdit()
          self.chat_history.setReadOnly(True)

          input_layout = QHBoxLayout()
          input_layout.addWidget(self.textField, stretch=4)
          input_layout.addWidget(sendBtn, stretch=1)

          main_layout = QVBoxLayout()
          main_layout.addWidget(self.chat_history)
          main_layout.addLayout(input_layout)

          central_widget = QWidget()
          central_widget.setLayout(main_layout)
          self.setCentralWidget(central_widget)

     def send_message(self):
        text = self.textField.text().strip()
        if text:
            self.chat_history.append(text)
            self.textField.clear()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()