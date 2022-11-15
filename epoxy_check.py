import os

import cv2

import img_preprocess
import predict_models
from settings import *


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
        print(self.folderPath)

    @classmethod
    def from_path(cls, folderPath):
        """_summary_

        Args:
            folderPath (_type_): _description_

        Returns:
            _type_: _description_
        """
        return cls(folderPath)

    def img_preprocess(self, img):
        preprocessed_img = img_preprocess.preproces(img)
        return preprocessed_img

    # 각 조건별 검사 기능 함수
    def check_model1(self, img):
        return False

    def check_model2(self, img):
        return False

    def check_model3(self, img):
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
        img = self.img_preprocess(img)

        if test:
            # 임시로 축소
            img_test = cv2.resize(
                img, (0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_CUBIC
            )
            cv2.imshow("img", img_test)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return False

        if self.check_type == "rule-base":
            if not self.check_model1(img):
                return False
            elif not self.check_model2(img):
                return False
            elif not self.check_model3(img):
                return False
            else:
                return True
        else:
            self.check_model_cnn(img)

    def check_folder(self, test=False):
        if test:
            for imgName in os.listdir(self.folderPath)[:5]:
                self.check_product(self.folderPath + imgName, test=True)
            return 0
        self.result = [
            "OK" if self.check_product(self.folderPath + imgName) else "NG"
            for imgName in os.listdir(self.folderPath)
        ]
