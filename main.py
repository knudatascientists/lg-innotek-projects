#  통합 파일
from epoxy_check import EpoxyCheck
from pyqt_test import MainWindow
from settings import *


class testWindow(MainWindow):
    def __init__(self):
        super().__init__()

    def test_pushed(self):
        super().test_pushed()
        print("overieded")


if __name__ == "__main__":
    # checkModel = EpoxyCheck.from_path(FOLDER_PATH)
    # checkModel.check_folder(test = True)
    # print(checkModel.result)

    # checkModel = EpoxyCheck(debug=True)

    # checkModel.check_product(test_np_path1, test_only=1, show=True)
    # checkModel.check_product(test_np_path2, test_only=2, show=True)
    # checkModel.check_product(test_np_path3, test_only=3, show=True)

    testWindow.start_gui_only()
