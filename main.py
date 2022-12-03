import os

import cv2
from PyQt5.QtGui import *

from epoxy_check import EpoxyCheck
from img_preprocess import img_resize
from pyqt_test import MainWindow
from settings import *


class testWindow(MainWindow):
    """connecting test module with Main test GUI window.

    Args:
        MainWindow (class): Main test GUI window.
    """

    checkModel = EpoxyCheck(debug=False, clear_log=True)

    def __init__(self):
        super().__init__()

    def test_pushed(self):
        """start test according to test type"""
        super().test_pushed()
        print(self.folderPath)
        if self.test_type == "all":
            self.folder_test()
        else:
            self.image_test()

    def folder_test(self, test=False):
        """Test all images in one folder

        Args:
            test (bool, optional): if True work on process_test mode. Defaults to False.
        """
        testWindow.checkModel.set_save_path(saveFolderPath=self.saveFolderPath)
        testWindow.checkModel.set_debug_path(debugPath=self.saveFolderPath)
        testWindow.checkModel.folderPath = self.folderPath
        testWindow.checkModel.saveFolderPath = self.saveFolderPath
        testWindow.checkModel.debug = self.debug

        try:
            testWindow.checkModel.check_folder(test=False, test_only=3, progress=self.progressBar)
        except:
            print("path error!")

    def image_test(self):
        """Test product image."""
        testWindow.checkModel.debug = self.debug
        result, img, debug_image, test_text = testWindow.checkModel.check_product(
            self.pathLabel.text(), return_debug_image=True, test_type=self.test_type
        )

        print(f'검사 결과 : {"OK" if result else "NG"}')
        self.write_log_text(f'검사 결과 : {"OK" if result else "NG"}')
        self.write_log_text(f"\t\t{test_text}")

        img = img_resize(img, GUI_IMG_SIZE)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        qImg = QImage(img.data, w, h, w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.resize(pixmap.width(), pixmap.height())

        debug_image = img_resize(debug_image, GUI_IMG_SIZE)
        debug_image = cv2.cvtColor(debug_image, cv2.COLOR_BGR2RGB)
        h, w, c = debug_image.shape
        qImg = QImage(debug_image.data, w, h, w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.debugLabel.setPixmap(pixmap)
        self.debugLabel.resize(pixmap.width(), pixmap.height())


if __name__ == "__main__":
    testWindow.start_gui_only()
