from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QApplication,
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtCore import Qt
import sys
import tuichat


class ClientMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainWindow = QWidget()
        self.initUi()

    def initUi(self):
        client = tuichat.client.Client(mode='gui')
        self.connectToServer(client)

        self.chatDisplayTextEdit = QTextEdit()
        self.chatDisplayTextEdit.setReadOnly(True)

        self.messageTextEdit = QTextEdit()
        self.messageTextEdit.setPlaceholderText('Enter a message')

        self.sendButton = QPushButton()
        self.sendButton.setText('Send')

        self.messagePanel = QHBoxLayout()
        self.messagePanel.addWidget(self.messageTextEdit, 5)
        self.messagePanel.addWidget(self.sendButton, 1)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.chatDisplayTextEdit, 5)
        self.layout.addLayout(self.messagePanel, 1)

        self.mainWindow.setLayout(self.layout)
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('TuiChat Client')
        self.setCentralWidget(self.mainWindow)
        self.show()

    def connectToServer(self, client_obj):
        connectWindow = ConnectWindow(client_obj, self)
        response = connectWindow.exec_()
        if response == QDialog.Accepted:
            self.client = connectWindow.client


class ConnectWindow(QDialog):
    def __init__(self, client, parent=None):
        super().__init__(parent)
        self.client = client
        self.initWindow()

    def initWindow(self):
        layout = QFormLayout()

        hostLabel = QLabel('Host')
        portLabel = QLabel('Port')

        self.hostLineEdit = QLineEdit()
        self.portLineEdit = QLineEdit()

        okButton = QPushButton('Connect')
        okButton.clicked.connect(self.connectToServer)

        layout.addRow(hostLabel, self.hostLineEdit)
        layout.addRow(portLabel, self.portLineEdit)
        layout.addWidget(okButton)

        layout.setFormAlignment(Qt.AlignCenter)
        layout.setVerticalSpacing(10)

        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)
        self.move(300, 300)
        self.resize(self.sizeHint())
        self.setWindowTitle('Connect')
        self.show()

    def connectToServer(self):
        self.client.connect(host=self.hostLineEdit.text(), port=int(self.portLineEdit.text()))
        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ClientMainWindow()
    sys.exit(app.exec_())
