import os

import cv2
import numpy as np
import pandas as pd
import tqdm
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

import img_preprocess
import test_models
from settings import *


class EpoxyCheck:
    """_summary_

    Returns:
        _type_: _description_
    """

    scoreNames = ["accuracy", "f1", "precision", "recall", "auc"]

    # 이미지 로드
    def __init__(self, folderPath="", check_type="rule-base", debug=False):
        """_summary_

        Args:
            folderPath (str, optional): _description_. Defaults to "".
            check_type (str, optional): _description_. Defaults to "rule-base".
        """
        if folderPath == "":
            pass
        else:
            self.folderPath = folderPath
            y_true = str.upper(self.folderPath[-3:-1])
            if y_true not in ["OK", "NG"]:
                y_true = "OK"
            self.y_true = [int(img_name[-6:-4] != "NG") for img_name in os.listdir(self.folderPath)]
            self.result = [0 for i in range(len(self.y_true))]

        self.score = pd.DataFrame(columns=EpoxyCheck.scoreNames)

        self.check_type = check_type

        if debug:
            try:
                os.mkdir("debug_images")
            except:
                pass
        try:
            print("검사 이미지 폴더 경로 :", self.folderPath)
        except:
            pass

    @classmethod
    def from_path(cls, folderPath=FOLDER_PATH):
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
    def check_model1(self, img, show):
        return False

    def check_model2(self, img, show):
        return False

    def check_model3(self, img, show):
        return test_models.model_hs(img, show)

    def check_model_cnn(self, img):
        return False

    def check_product(self, imgPath, test=False, test_only=0, show=False):
        """_summary_

        Args:
            imgPath (_type_): _description_
            test (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        img = cv2.imread(imgPath)

        if test:
            # 임시로 축소
            img_test = img_preprocess.img_resize(img, resize_size=1600)
            cv2.imshow("img", img_test)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        if test_only:
            return eval(f"self.check_model{test_only}(img, show = show)")

        if self.check_type == "rule-base":
            if self.check_model1(img) == "NG":
                return 0
            elif self.check_model2(img) == "NG":
                return 0
            elif self.check_model3(img) == "NG":
                return 0
            else:
                return 1
        else:
            return int(self.check_model_cnn(img) == "NG")

    def check_folder(self, test=False, print_score=False, test_only=0):
        if test:
            for imgName in os.listdir(self.folderPath)[:5]:
                print(self.check_product(self.folderPath + imgName, test=True, test_only=test_only))
        else:
            self.result = [
                int(self.check_product(self.folderPath + imgName, test_only=test_only) == "OK")
                for imgName in tqdm.tqdm(os.listdir(self.folderPath))
            ]

        if print_score:
            self.calcScore(print_score=print_score)
        else:
            self.calcScore()
        return self.score

    def calcScore(self, print_score=False):
        try:
            result = pd.Series(
                [
                    accuracy_score(self.y_true, self.result),
                    f1_score(self.y_true, self.result, pos_label=1),
                    precision_score(self.y_true, self.result, pos_label=1),
                    recall_score(self.y_true, self.result, pos_label=1),
                    roc_auc_score(self.y_true, self.result),
                ],
                index=EpoxyCheck.scoreNames,
            )
        except:
            result = pd.Series(
                [
                    accuracy_score(self.y_true, self.result),
                    f1_score(self.y_true, self.result, pos_label=1),
                    precision_score(self.y_true, self.result, pos_label=1),
                    recall_score(self.y_true, self.result, pos_label=1),
                    0,
                ],
                index=EpoxyCheck.scoreNames,
            )
        self.score.loc[len(self.score), :] = result
        if print_score:
            print(result)

    def getScore(self):
        try:
            return self.score[-1]
        except:
            print("No Score")


if __name__ == "__main__":
    test_model = EpoxyCheck.from_path(folderPath="O:/lg/team/images/overkill/")
    result = test_model.check_folder(print_score=True, test_only=3)
