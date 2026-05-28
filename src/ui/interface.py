import sys
import argparse
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit

MESSAGE_LIMIT = 256

parser = argparse.ArgumentParser(description="IP Required and Mode")
parser.add_argument("-i", "--ip", type=str, required=True, help="IP Required to connect")
parser.add_argument("-m", "--mode", type=str, required=True, help="User connection mode")
args = parser.parse_args()

def CheckFlags():
     global args
     if args.mode == "server":
          print(f"[!] You ran qChat in server mode.\nIP: {None}")
     elif args.mode == "client" and args.ip is not None:
          print("[*] You ran qChat in client mode.")
     else:
          print(f"[?] Missing required arguments. Please check your flags.")
          exit(0) # Turn off qChat

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

if __name__ == "__main__":
     CheckFlags()

     app = QApplication(sys.argv)

     window = MainWindow()
     window.show()

     app.exec()