import os

import cv2

import img_preprocess
from settings import *
from test_models import *


class EpoxyCheck:
    """_summary_

    Returns:
        _type_: _description_
    """

    # 이미지 로드
    def __init__(self, folderPath="", check_type="rule-base"):
        """_summary_

        Args:
            folderPath (str, optional): _description_. Defaults to "".
            check_type (str, optional): _description_. Defaults to "rule-base".
        """
        if folderPath == "":
            self.folderPath = FOLDER_PATH
        else:
            self.folderPath = folderPath
        self.check_type = check_type
        self.result = ["NG" for i in range(len(os.listdir(self.folderPath)))]
        self.score = 0
        print(self.folderPath)

    @classmethod
    def from_path(cls, folderPath):
        """Get test object with image data from FolderPath.

        Args:
            folderPath (str): folder location where image data is.

        Returns:
            class object
        """
        return cls(folderPath)

    def img_preprocess(self, img):
        item_img, item_gray, item_bin = img_preprocess.preprocess(img)
        return item_img, item_gray, item_bin

    # 각 조건별 검사 기능 함수
    def check_model1(self, img):
        return False

    def check_model2(self, img):
        return False

    def check_model3(self, img, gray, bin):
        return False

    def check_model_cnn(self, img):
        return False

    def check_product(self, imgPath, test=False):
        """_summary_

        Args:
            imgPath (_type_): _description_
            test (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        img = cv2.imread(imgPath)
        img, gray, bin = self.img_preprocess(img)

        if test:
            # 임시로 축소
            img_test = img_preprocess.img_resize(img, resize_size=1600)
            cv2.imshow("img", img_test)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return "NG"

        if self.check_type == "rule-base":
            if self.check_model1(img) == "NG":
                return "NG"
            elif self.check_model2(img) == "NG":
                return "NG"
            elif self.check_model3(img, gray, bin) == "NG":
                return "NG"
            else:
                return "OK"
        else:
            return self.check_model_cnn(img)

    def check_folder(self, test=False, return_result=True):
        if test:
            for imgName in os.listdir(self.folderPath)[:5]:
                self.check_product(self.folderPath + imgName, test=True)

        self.result = [self.check_product(self.folderPath + imgName) for imgName in os.listdir(self.folderPath)]

        if return_result:
            self.calcScore()
            return self.score

    def calcScore(self):
        self.score = 0
