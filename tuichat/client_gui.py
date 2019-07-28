from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PyQt5.QtCore import Qt
import sys
import tuichat.client


class ClientMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        client = tuichat.client.Client()
        self.connectToServer(client)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('TuiChat Client')
        self.show()

    def connectToServer(self, client_obj):
        self.connection = ConnectWindow()


class ConnectWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWindow()

    def initWindow(self):
        layout = QFormLayout()

        hostLabel = QLabel('Host')
        portLabel = QLabel('Port')

        hostLineEdit = QLineEdit()
        portLineEdit = QLineEdit()

        okButton = QPushButton('Connect')

        layout.addRow(hostLabel, hostLineEdit)
        layout.addRow(portLabel, portLineEdit)
        layout.addWidget(okButton)

        layout.setFormAlignment(Qt.AlignCenter)
        layout.setVerticalSpacing(10)

        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)
        self.move(300, 300)
        self.resize(self.sizeHint())
        self.setWindowTitle('Connect')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ClientMainWindow()
    sys.exit(app.exec_())
