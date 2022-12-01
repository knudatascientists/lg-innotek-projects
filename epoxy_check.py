import os
from datetime import datetime as dt

import cv2
import pandas as pd
import tqdm
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

import test_models
from settings import *


class EpoxyCheck:
    """Test Class"""

    scoreNames = ["accuracy", "f1", "precision", "recall", "auc"]

    # 이미지 로드
    def __init__(
        self, up_folderPath="", folderPath="", check_type="rule-base", debug=False, cnn=False, clear_log=False
    ):
        """Creat testing object

        Args:
            up_folderPath (str, optional): Path of folder that containing image folders . Defaults to "".
            folderPath (str, optional): Path of image folder. Defaults to "".
            check_type (str, optional): test type. Defaults to "rule-base".
            debug (bool, optional): if True create debug_image folder and save test logs. Defaults to True.
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
        self.cnn = cnn
        self.set_debug_path(clear_log=clear_log)
        # self.set_save_path()
        try:
            print("Testing image folder path :", self.folderPath)
        except:
            try:
                print("Testing image folder path :", self.up_folderPath)
            except:
                pass

    @classmethod
    def from_up_path(cls, up_folderPath=UP_FOLER_PATH, debug=True):
        """Get test object with image data from up_folderPath.

        Args:
            up_folderPath (str, optional): Path of folder that containing image folders . Defaults to "".
            debug (bool, optional): if True create debug_image folder and save test logs. Defaults to True.

        Returns:
            _type_: _description_
        """
        return cls(up_folderPath=up_folderPath, debug=debug)

    @classmethod
    def from_path(cls, folderPath=FOLDER_PATH, debug=True):
        """Get test object with image data from FolderPath.

        Args:
            folderPath (str, optional): Path of image folder. Defaults to "".
            debug (bool, optional): if True create debug_image folder and save test logs. Defaults to True.

        Returns:
            Class object
        """
        return cls(folderPath, debug=debug)

    def set_debug_path(self, debugPath=DEBUG_PATH, clear_log=False):
        """Create debug_image folder

        Args:
            debugPath (_type_, optional): Path where debug_image folder will be Created . Defaults to DEBUG_PATH.
            clear_folder (bool, optional): If True recreate debug_image folder. Defaults to True.
        """
        self.debugPath = debugPath
        if clear_log:
            f = open(debugPath + "test_log.txt", "w")
            f.close()
        else:
            f = open(debugPath + "test_log.txt", "a")
            f.close()

        try:
            os.mkdir(debugPath + "debug_images")
            os.mkdir(debugPath + "debug_images/pred_ok")
            os.mkdir(debugPath + "debug_images/pred_ng")
        except:

            debugPath = debugPath + "debug_images/"
            folder_list = os.listdir(debugPath)
            for folder in folder_list:
                file_list = os.listdir(debugPath + folder + "/")
                try:
                    os.rmdir(debugPath + folder)
                except:

                    for file in file_list:
                        os.remove(debugPath + folder + "/" + file)
                    os.rmdir(debugPath + folder)
            os.rmdir(debugPath[:-1])

            os.mkdir(debugPath[:-1])
            os.mkdir(debugPath + "pred_ok")
            os.mkdir(debugPath + "pred_ng")

    def set_save_path(self, saveFolderPath=SAVE_FOLDER_PATH):
        self.saveFolderPath = saveFolderPath
        try:
            os.mkdir(saveFolderPath + "preds")
            os.mkdir(saveFolderPath + "preds/pred_ok")
            os.mkdir(saveFolderPath + "preds/pred_ng")

        except:

            saveFolderPath = saveFolderPath + "preds/"

            folder_list = os.listdir(saveFolderPath)

            for folder in folder_list:
                file_list = os.listdir(saveFolderPath + folder + "/")
                try:
                    os.rmdir(saveFolderPath + folder)

                except:
                    for file in file_list:
                        os.remove(saveFolderPath + folder + "/" + file)
                    os.rmdir(saveFolderPath + folder)

            os.rmdir(saveFolderPath[:-1])

            os.mkdir(saveFolderPath[:-1])
            os.mkdir(saveFolderPath + "pred_ok")
            os.mkdir(saveFolderPath + "pred_ng")

    def add_test_log(self, text="", image=None, image_name="", NG=True):
        """Save test log and debug image.

        Args:
            text (str, optional): Log text. Defaults to "".
            image (np.Array, optional): Debug image. Defaults to None.
            image_name (str, optional): Debug image name. Defaults to "".
        """
        if len(text):
            f = open(self.debugPath + "test_log.txt", "a")
            f.write(f"[{dt.now().strftime('%Y-%m-%d %H:%M:%S:%f')}] " + text + "\n")
            f.close()
        if image is not None:
            # print("save img to debug_image")
            if NG:
                cv2.imwrite(
                    self.debugPath + "debug_images/pred_ng/" + dt.now().strftime("_%Y_%m_%d__%H_%M_%S") + image_name,
                    image,
                )
            else:
                cnn_image = self.write_cnn_score(image)
                cv2.imwrite(
                    self.debugPath + "debug_images/pred_ok/" + dt.now().strftime("_%Y_%m_%d__%H_%M_%S") + image_name,
                    cnn_image,
                )

    # cnn test 검사 결과 이미지에 적어주기
    def write_cnn_score(self, image):
        image = cv2.putText(
            image,
            f"CNN Model Score : {round(self.get_cnn_score(image),3)}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            3,
            (0, 255, 0),
            3,
        )
        return image

        # 각 조건별 검사 기능 함수
        """Testing models
        """

    def check_model1(self, img, show):
        pred, debug_imgs, cnt = test_models.model_js(img, show=show)
        return pred, debug_imgs

    def check_model2(self, img, show):
        test_result, debug_imgs = test_models.model_hj(img, show=show)
        if test_result == "OK":
            test_result, debug_imgs = test_models.model_ng(img, show=show)
        return test_result, debug_imgs
        # return test_models.model_ng(img, show=show)

    def check_model3(self, img, show):
        test_result, debug_imgs, ratio = test_models.model_hs(img, show=show)

        return (
            test_result,
            debug_imgs,
        )

    def get_cnn_score(self, img):
        proba = test_models.model_iu(img)
        return proba

    def check_all_folder(self, test=False, test_only=0):
        """Test all images in many folders

        Args:
            test (bool, optional): if True work on process_test mode. Defaults to False.
            test_only (int, optional): If not 0 test olny one condition. Defaults to 0.
        """
        self.y_true = []
        self.result = []
        for folderPath in os.listdir(self.up_folderPath):
            if folderPath == ".gitkeep":
                continue

            self.folderPath = self.up_folderPath + folderPath + "/"
            if test:
                pass

            print("current testing foler :", self.folderPath)

            self.check_folder(test=test, test_only=test_only)

    def check_folder(self, test=False, test_only=0, progress=None):
        """Test all images in one folder

        Args:
            test (bool, optional): if True work on process_test mode. Defaults to False.
            test_only (int, optional): If not 0 test olny one condition. Defaults to 0.
        """
        y_true = int(self.folderPath[-3:-1] != "ng")
        img_len = len(os.listdir(self.folderPath))
        if progress is not None:
            progress_value = 0
            progress.setValue(0)
            progress_percent = int(progress_value / img_len * 100)

        if test:
            img_len = 5
            for imgName in tqdm.tqdm(os.listdir(self.folderPath)[:5]):
                self.y_true.append(y_true)
                self.result.append(self.check_product(self.folderPath + imgName, test_only=test_only, test=test))
                if progress is not None:
                    progress_value += 1
                    if progress_percent != int(progress_value / img_len * 100):
                        progress_percent = int(progress_value / img_len * 100)
                        progress.setValue(progress_percent)

        else:
            for imgName in tqdm.tqdm(os.listdir(self.folderPath)):
                self.y_true.append(y_true)
                self.result.append(self.check_product(self.folderPath + imgName, test_only=test_only, test=test))
                if progress is not None:
                    progress_value += 1
                    # print(progress_value, "/", img_len, ":", int(progress_value / img_len * 100))
                    if progress_percent != int(progress_value / img_len * 100):
                        progress_percent = int(progress_value / img_len * 100)
                        progress.setValue(progress_percent)

    def check_product(self, imgPath, test=False, test_only=0, show=False, return_debug_image=False, test_type="all"):
        """Test product image.

        Args:
            imgPath (_type_): Path of product image
            test (bool, optional): if True work on process_test mode. Defaults to False.
            test_only (int, optional): If not 0 test olny one condition. Defaults to 0.
            show (bool, optional): if true show debug image. Defaults to False.

        Returns:
            int: if 1 product is 'OK', if 0 product is 'NG'
        """

        img = cv2.imread(imgPath)

        if test:
            pass

        if test_only:
            test_result, debug_imgs = eval(f"self.check_model{test_only}(img, show = show)")
            self.sort_image(img, imgPath.split("/")[-1], test_result, test_type=test_type)
            # print(test_result, len(debug_imgs))
            if self.debug:
                self.add_test_log(text=f"condition {test_only} test result : {test_result} ({imgPath})")
                if test_result == "NG":
                    self.add_test_log(image=debug_imgs[-1], image_name=imgPath.split("/")[-1])
                else:
                    self.add_test_log(image=img, image_name=imgPath.split("/")[-1], NG=False)

            if return_debug_image:
                if debug_imgs[-1] is None:
                    debug_imgs[-1] = img.copy()
                return int(test_result == "OK"), debug_imgs[-1]

            return int(test_result == "OK")

        else:
            test_result, debug_imgs = self.check_model3(img, show=show)

            if test_result == "NG":
                self.sort_image(img, imgPath.split("/")[-1], test_result, test_type=test_type)
                self.add_test_log(text=f"condition 3 test result : NG ({imgPath})")
                if self.debug:
                    self.add_test_log(image=debug_imgs[-1], image_name=imgPath.split("/")[-1])
                if return_debug_image:
                    return 0, debug_imgs[-1]
                return 0

            test_result, debug_imgs = self.check_model2(img, show=show)
            if test_result == "NG":
                self.sort_image(img, imgPath.split("/")[-1], test_result, test_type=test_type)
                self.add_test_log(text=f"condition 2 test result : NG ({imgPath})")
                if self.debug:
                    self.add_test_log(image=debug_imgs[-1], image_name=imgPath.split("/")[-1])
                if return_debug_image:
                    return 0, debug_imgs[-1]
                return 0

            test_result, debug_imgs = self.check_model1(img, show=show)
            if test_result == "NG":
                self.sort_image(img, imgPath.split("/")[-1], test_result, test_type=test_type)
                self.add_test_log(text=f"condition 1 test result : NG ({imgPath})")
                if self.debug:
                    self.add_test_log(image=debug_imgs[-1], image_name=imgPath.split("/")[-1])
                if return_debug_image:
                    return 0, debug_imgs[-1]
                return 0

            self.sort_image(img, imgPath.split("/")[-1], test_result, test_type=test_type)
            self.add_test_log(text=f"test result : OK ({imgPath})")
            if self.debug:
                self.add_test_log(image=debug_imgs[-1], image_name=imgPath.split("/")[-1], NG=False)
            if return_debug_image:
                return 1, debug_imgs[-1]
            return 1

    def sort_image(self, image, image_name, test_result, test_type="all"):
        if test_type == "one":
            return 0

        if test_result == "OK":
            cv2.imwrite(
                self.saveFolderPath + "preds/pred_ok/" + dt.now().strftime("%Y_%m_%d__%H_%M_%S_") + image_name, image
            )
        else:
            cv2.imwrite(
                self.saveFolderPath + "preds/pred_ng/" + dt.now().strftime("%Y_%m_%d__%H_%M_%S_") + image_name, image
            )

    def calcScore(self):
        """Calculate testing scores"""
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
    result = test_model.check_all_folder(test_only=1)
    test_model.calcScore()
