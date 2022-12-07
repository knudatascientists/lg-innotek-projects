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
            testWindow.checkModel.check_folder(progress=self.progressBar)
            n_product = len(testWindow.checkModel.result)
            found_OK = sum(testWindow.checkModel.result)
            self.write_log_text(f"\n총 {n_product}개의 제품 이미지 중 {found_OK}개의 정상 이미지 발견!")
            self.write_log_text(f"\n          overkill ratio : {round(found_OK/n_product *100,2)}%")
        except:
            self.write_log_text("error")
            print("error!")

    def image_test(self):
        """Test product image."""
        testWindow.checkModel.debug = self.debug
        try:
            result, img, debug_image, test_text = testWindow.checkModel.check_product(
                self.pathLabel.text(), return_debug_image=True, test_type=self.test_type
            )

            print(f'\n검사 결과 : {"OK" if result else "NG"}')
            self.write_log_text(f'검사 결과 : {"OK" if result else "NG"}')
            self.write_log_text(f"\t\t{test_text}\n")

            testWindow.checkModel.debug = False
            result = testWindow.checkModel.check_product(self.pathLabel.text(), test_type=self.test_type, test_only=1)
            self.write_log_text(f"----1번 조건 검사 결과 : {'OK' if result else 'NG'}")

            result = testWindow.checkModel.check_product(self.pathLabel.text(), test_type=self.test_type, test_only=2)
            self.write_log_text(f"----2번 조건 검사 결과 : {'OK' if result else 'NG'}")

            result = testWindow.checkModel.check_product(self.pathLabel.text(), test_type=self.test_type, test_only=3)
            self.write_log_text(f"----3번 조건 검사 결과 : {'OK' if result else 'NG'}")

            testWindow.checkModel.debug = self.debug

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

        except:
            self.write_log_text("error")
            print("error!")


if __name__ == "__main__":
    testWindow.start_gui_only()
