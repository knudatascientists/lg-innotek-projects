import os
from datetime import datetime as dt

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
    def __init__(self, up_folderPath="", folderPath="", check_type="rule-base", debug=True):
        """_summary_

        Args:
            folderPath (str, optional): _description_. Defaults to "".
            check_type (str, optional): _description_. Defaults to "rule-base".
        """
        if up_folderPath == "":
            pass

        else:
            self.up_folderPath = up_folderPath

        if folderPath == "":
            pass
        else:
            self.folderPath = folderPath

        self.y_true = []
        self.result = []

        self.score = pd.DataFrame(columns=EpoxyCheck.scoreNames)

        self.check_type = check_type
        self.debug = debug

        if self.debug:
            self.set_debug_path()

        try:
            print("검사 이미지 폴더 경로 :", self.folderPath)
        except:
            try:
                print("검사 이미지 폴더 경로 :", self.up_folderPath)
            except:
                pass

    @classmethod
    def from_up_path(cls, up_folderPath=UP_FOLER_PATH, debug=True):
        return cls(up_folderPath=up_folderPath, debug=debug)

    @classmethod
    def from_path(cls, folderPath=FOLDER_PATH, debug=True):
        """Get test object with image data from FolderPath.

        Args:
            folderPath (str): folder location where image data is.

        Returns:
            class object
        """
        return cls(folderPath, debug=debug)

    def set_debug_path(self, debugPath=DEBUG_PATH, clear_folder=True):
        self.debugPath = debugPath
        if clear_folder:
            try:
                file_list = os.listdir(debugPath)
                for file in file_list:
                    os.remove(debugPath + file)
                os.rmdir(debugPath[:-1])
            except:
                pass
        os.mkdir(debugPath[:-1])
        f = open(debugPath + "test_log.txt", "w")
        f.close()

    def add_test_log(self, text="", image=None, image_name=""):
        if len(text):
            f = open(self.debugPath + "test_log.txt", "a")
            f.write(f"[{dt.now().strftime('%Y-%m-%d %H:%M:%S:%f')}] " + text + "\n")
            f.close()
        if image is not None:
            print("save img to debug_image")
            cv2.imwrite(self.debugPath + dt.now().strftime("%Y_%m_%d__%H_%M_%S_") + image_name, image)

    # 각 조건별 검사 기능 함수
    def check_model1(self, img, show):
        return test_models.model_js(img, show=show)

    def check_model2(self, img, show):
        test_result, debug_imgs = test_models.model_hj(img, show=show)
        if test_result == "OK":
            test_result, debug_imgs = test_models.model_ng(img, show=show)
        return test_result, debug_imgs
        # return test_models.model_ng(img, show=show)

    def check_model3(self, img, show):
        # test_result, debug_imgs = test_models.model_hs(img, show=show)
        return test_models.model_hs(img, show=show)

    def check_model_cnn(
        self,
        img,
    ):
        return False

    def check_all_folder(self, test=False, test_only=0):
        for folderPath in os.listdir(self.up_folderPath):
            if folderPath == ".gitkeep":
                continue

            self.folderPath = self.up_folderPath + folderPath + "/"
            if test:
                pass

            print("current testing foler :", self.folderPath)

            self.check_folder(test=test, test_only=test_only)

    def check_folder(self, test=False, test_only=0):
        y_true = int(self.folderPath[-3:-1] != "ng")

        if test:
            for imgName in tqdm.tqdm(os.listdir(self.folderPath)[:5]):
                self.y_true.append(y_true)
                self.result.append(self.check_product(self.folderPath + imgName, test_only=test_only, test=test))

                # try:
                #     print(self.check_product(self.folderPath + imgName, test_only=test_only))

                # except:
                #     self.check_product(self.folderPath + imgName, show=True, test=True, test_only=test_only)

        else:
            for imgName in tqdm.tqdm(os.listdir(self.folderPath)):
                self.y_true.append(y_true)
                self.result.append(self.check_product(self.folderPath + imgName, test_only=test_only, test=test))

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
            pass

        if test_only:

            test_result, debug_imgs = eval(f"self.check_model{test_only}(img, show = show)")
            print(test_result, len(debug_imgs))
            if test_result == "NG" and self.debug:
                self.add_test_log(text=f"condition {test_only} test result : NG ({imgPath})")
                for debug_img in debug_imgs:
                    self.add_test_log(image=debug_img, image_name=imgPath.split("/")[-1])
            return int(test_result == "OK")

        elif self.check_type == "rule-base":

            test_result, debug_imgs = self.check_model1(img, show=show)
            if test_result == "NG":
                if self.debug:
                    self.add_test_log(text=f"condition 1 test result : NG ({imgPath})")
                    for debug_img in debug_imgs:
                        self.add_test_log(image=debug_img, image_name=imgPath.spllit("/")[-1])
                return 0

            test_result, debug_imgs = self.check_model2(img, show=show)
            if test_result == "NG":
                if self.debug:
                    self.add_test_log(text=f"condition 2 test result : NG ({imgPath})")
                    for debug_img in debug_imgs:
                        self.add_test_log(image=debug_img, image_name=imgPath.spllit("/")[-1])
                return 0

            test_result, debug_imgs = self.check_model3(img, show=show)
            if test_result == "NG":
                if self.debug:
                    self.add_test_log(text=f"condition 3 test result : NG ({imgPath})")
                    for debug_img in debug_imgs:
                        self.add_test_log(image=debug_img, image_name=imgPath.spllit("/")[-1])
                return 0

            return 1

        else:
            test_result = self.check_model_cnn(img)
            if self.debug:
                self.add_test_log(text=f"CNN model test result : {test_result} ({imgPath})")
            return int(test_result == "NG")

    def calcScore(self):
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
                    0,
                    0,
                    0,
                    0,
                ],
                index=EpoxyCheck.scoreNames,
            )
        self.score.loc[len(self.score), :] = result
        print(result)

    def getScore(self):
        try:
            self.calcScore()
            return self.score[-1]
        except:
            print("No Score")


if __name__ == "__main__":
    test_model = EpoxyCheck.from_up_path()
    result = test_model.check_all_folder(test_only=3)
    test_model.calcScore()
