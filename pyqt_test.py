import sys

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from settings import *

from_class = uic.loadUiType("./GUI/test.ui")[0]
help_class = uic.loadUiType("./GUI/help.ui")[0]


class MainWindow(QDialog, from_class):
    """Main test GUI window.

    Args:
        QDialog (class): PyQt5.QtWidgets.QDialog
        from_class (class): pyqt window class made on pyqt designer
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        """setting objects on GUI."""
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
        """show all image test GUI window."""
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
        """show one image test GUI window."""
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
        """get path of folder or image on GUI."""
        if self.test_type == "one":
            folderpath = QFileDialog.getOpenFileName(self, "Select image")[0]
            self.set_directory(folderpath)
        else:
            folderpath = QFileDialog.getExistingDirectory(self, "Select Folder")
            self.set_directory(folderpath + "/")

    def findSavePath_pushed(self):
        """get path of folder where test result and debug will be stored on GUI."""
        folderpath = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.set_saveDirectory(folderpath + "/")

    def test_pushed(self):
        """show starting test."""
        if self.test_type == "one":
            self.write_log_text(f"testing {self.folderPath}...")
        else:
            self.write_log_text(f"testing {self.folderPath}...  debug : {self.debug}")

    def help_pushed(self):
        """show help window."""
        help = HelpWindow()
        help.exec_()

    def debug_change(self):
        """change debug mode."""
        if self.debug_checkBox.isChecked():
            self.debug = True
            self.debugLabel.show()

        else:
            self.debug = False
            self.debugLabel.close()

    def set_directory(self, path=FOLDER_PATH):
        """set path of folder or image on GUI."""
        self.folderPath = path
        self.pathLabel.clear()
        self.pathLabel.setText(path)

    def set_saveDirectory(self, path=SAVE_FOLDER_PATH):
        """set path of folder where test result and debug will be stored on GUI."""
        self.saveFolderPath = path
        self.savePathLabel.clear()
        self.savePathLabel.setText(path)

    def set_log_text_color(self, qcolor):
        if qcolor == "red":
            qcolor = QColor(255, 0, 0)

        else:
            qcolor = QColor(0, 0, 0)
        self.logText.setCurrentFont(qcolor)

    def write_log_text(self, log_text, qcolor="black"):
        """write log on GUI."""
        if qcolor != "black":
            self.fset_log_text_color(qcolor)
        self.logText.append(log_text)
        if qcolor != "black":
            self.logText.setCurrentFont(QColor(0, 0, 0))

    @classmethod
    def start_gui_only(cls):
        """create test GUI window"""
        app = QApplication(sys.argv)
        myWindow = cls()
        myWindow.show()
        sys.exit(app.exec_())


class HelpWindow(QDialog, help_class):
    """Help GUI window.

    Args:
        QDialog (class): PyQt5.QtWidgets.QDialog
        help_class (class): pyqt window class made on pyqt designer
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()


if __name__ == "__main__":
    MainWindow.start_gui_only()
