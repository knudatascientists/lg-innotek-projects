import sys

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from settings import *

from_class = uic.loadUiType("./GUI/test.ui")[0]


class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.menu1Button.clicked.connect(self.menu1_pushed)
        self.menu2Button.clicked.connect(self.menu2_pushed)
        self.findPathButton.clicked.connect(self.findPath_pushed)
        self.testButton.clicked.connect(self.test_pushed)
        self.cnn = False
        self.debug = False
        self.cnn_checkBox.stateChanged.connect(self.cnn_change)
        self.debug_checkBox.stateChanged.connect(self.debug_change)
        self.set_directory()

    def menu1_pushed(self):
        self.set_directory()
        self.debugView.close()
        self.write_log_text("전체 이미지 검사")

    def menu2_pushed(self):
        self.set_directory()
        self.debugView.show()
        self.write_log_text("단일 이미지 검사")

    def findPath_pushed(self):
        folderpath = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.set_directory(folderpath)
        self.write_log_text("경로 가져오기")

    def test_pushed(self):
        self.write_log_text(f"testing products..., cnn : {self.cnn}, debug : {self.debug}")

    def cnn_change(self):
        if self.cnn_checkBox.isChecked():
            self.cnn = True
        else:
            self.cnn = False

    def debug_change(self):
        if self.debug_checkBox.isChecked():
            self.debug = True
        else:
            self.debug = False

    def set_directory(self, path=FOLDER_PATH):
        self.pathLabel.clear()
        self.pathLabel.setText(path)

    def set_log_text_color(self, qcolor):
        if qcolor == "red":
            qcolor = QColor(255, 0, 0)

        else:
            qcolor = QColor(0, 0, 0)
        self.logText.setCurrentFont(qcolor)

    def write_log_text(self, log_text, qcolor="black"):
        if qcolor != "black":
            self.fset_log_text_color(qcolor)
        self.logText.append(log_text)
        if qcolor != "black":
            self.logText.setCurrentFont(QColor(0, 0, 0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
