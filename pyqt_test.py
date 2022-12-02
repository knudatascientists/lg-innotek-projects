import sys

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from settings import *

from_class = uic.loadUiType("./GUI/test.ui")[0]
help_class = uic.loadUiType("./GUI/help.ui")[0]


class MainWindow(QDialog, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.menu1_pushed()
        self.menu1Button.clicked.connect(self.menu1_pushed)
        self.menu2Button.clicked.connect(self.menu2_pushed)
        self.findPathButton.clicked.connect(self.findPath_pushed)
        self.savePathButton.clicked.connect(self.findSavePath_pushed)
        self.testButton.clicked.connect(self.test_pushed)
        self.debug_checkBox.stateChanged.connect(self.debug_change)

        self.help_pushButton.clicked.connect(self.help_pushed)
        self.debug = False

    def menu1_pushed(self):
        self.test_type = "all"
        self.saveFrame.show()
        self.logText.clear()
        self.progressBar.show()
        self.set_directory()
        self.imageLabel.close()
        self.debugLabel.close()
        self.set_saveDirectory()
        self.write_log_text("전체 이미지 검사")

    def menu2_pushed(self):
        self.test_type = "one"
        self.saveFrame.close()
        self.logText.clear()
        self.progressBar.close()
        self.debug_checkBox.setCheckState(2)
        self.set_directory(test_np_path1)
        self.imageLabel.show()
        self.debugLabel.show()
        self.write_log_text("단일 이미지 검사")

    def findPath_pushed(self):
        if self.test_type == "one":
            folderpath = QFileDialog.getOpenFileName(self, "Select image")[0]
            self.set_directory(folderpath)
        else:
            folderpath = QFileDialog.getExistingDirectory(self, "Select Folder")
            self.set_directory(folderpath + "/")

    def findSavePath_pushed(self):
        folderpath = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.set_saveDirectory(folderpath + "/")

    def test_pushed(self):
        if self.test_type == "one":
            self.write_log_text(f"testing {self.folderPath}...")
        else:
            self.write_log_text(f"testing {self.folderPath}...  debug : {self.debug}")

    def help_pushed(self):
        help = HelpWindow()
        help.exec_()

    def debug_change(self):
        if self.debug_checkBox.isChecked():
            self.debug = True
            self.debugLabel.show()

        else:
            self.debug = False
            self.debugLabel.close()

    def set_saveDirectory(self, path=SAVE_FOLDER_PATH):
        self.saveFolderPath = path
        self.savePathLabel.clear()
        self.savePathLabel.setText(path)

    def set_directory(self, path=FOLDER_PATH):
        self.folderPath = path
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

    @classmethod
    def start_gui_only(cls):
        app = QApplication(sys.argv)
        myWindow = cls()
        myWindow.show()
        sys.exit(app.exec_())


class HelpWindow(QDialog, help_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()


if __name__ == "__main__":
    MainWindow.start_gui_only()
