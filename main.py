#  통합 파일
import os

from epoxy_check import EpoxyCheck
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
        testWindow.checkModel.folderPath = self.folderPath
        testWindow.checkModel.saveFolderPath = self.saveFolderPath
        testWindow.checkModel.debug = self.debug
        testWindow.checkModel.cnn = self.cnn

        try:
            testWindow.checkModel.check_folder(test=True, test_only=3, progress=self.progressBar)
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
        testWindow.checkModel.cnn = self.cnn
        try:
            result, debug_image = testWindow.checkModel.check_product(self.folderPath, return_debug_image=True)
        except:
            print("path error!")

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
