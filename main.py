#  통합 파일
import os

import cv2
from PyQt5.QtGui import *

from epoxy_check import EpoxyCheck
from img_preprocess import img_resize
from pyqt_test import MainWindow
from settings import *


class testWindow(MainWindow):
    checkModel = EpoxyCheck(debug=False, clear_log=True)

    def __init__(self):
        super().__init__()

    def test_pushed(self):
        super().test_pushed()
        print(self.folderPath)
        if self.test_type == "all":
            self.folder_test()
        else:
            self.image_test()

    def folder_test(self, test=False):
        testWindow.checkModel.set_save_path(saveFolderPath=self.saveFolderPath)
        testWindow.checkModel.set_debug_path(debugPath=self.saveFolderPath)
        testWindow.checkModel.folderPath = self.folderPath
        testWindow.checkModel.saveFolderPath = self.saveFolderPath
        testWindow.checkModel.debug = self.debug
        # testWindow.checkModel.cnn = self.cnn

        try:
            testWindow.checkModel.check_folder(test=False, test_only=3, progress=self.progressBar)
        except:
            print("path error!")

    """
        # y_true = int(self.folderPath[-3:-1] != "ng")
        # img_len = len(os.listdir(self.folderPath))
        # progress_value = 0

        # if test:
        #     for imgName in os.listdir(self.folderPath)[:5]:
        #         testWindow.checkModel.y_true.append(y_true)
        #         testWindow.checkModel.result.append(
        #             testWindow.checkModel.check_product(self.folderPath + imgName, test_only=3, test=test)
        #         )

        #         progress_value += 1
        #         self.progressBar.setValue(progress_value * 10)

        # else:
        #     for imgName in os.listdir(self.folderPath):
        #         testWindow.checkModel.y_true.append(y_true)
        #         testWindow.checkModel.result.append(
        #             testWindow.checkModel.check_product(self.folderPath + imgName, test_only=3, test=test)
        #         )

        #         progress_value += 1
        #         # print(progress_value, "/", img_len, ":", int(progress_value / img_len * 100))
        #         self.progressBar.setValue(int(progress_value / img_len * 100))
"""

    # 검사 결과 출력 기능 추가하기

    def image_test(self):
        # testWindow.checkModel.cnn = self.cnn
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

    # 검사 결과 출력 기능 추가하기


if __name__ == "__main__":
    # checkModel = EpoxyCheck.from_path(FOLDER_PATH)
    # checkModel.check_folder(test = True)
    # print(checkModel.result)

    # checkModel.check_product(test_np_path1, test_only=1, show=True)
    # checkModel.check_product(test_np_path2, test_only=2, show=True)
    # checkModel.check_product(test_np_path3, test_only=3, show=True)
    # checkModel.check_product(test_np_path3, test_only=4, show=True)

    testWindow.start_gui_only()
