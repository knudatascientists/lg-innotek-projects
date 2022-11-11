
from predict_models.model3_hs import *
from settings import *
import os

class EpoxyCheck:
    def __init__(self, folderPath= '',check_type = 'rule-base'):
        if folderPath =='':
            self.folderPath = FOLDER_PATH
        else:
            self.folderPath = folderPath
        self.check_type = check_type
        self.result = ['NG' for i in range(len(os.listdir(self.folderPath)))]


    @classmethod
    def from_path(cls, folderPath):
        return cls(folderPath)


    # 각 조건별 검사 기능 함수
    def check_model1(self,imgPath):
        return False
    
    def check_model2(self,imgPath):
        return False
    
    def check_model3(self,imgPath):
        return False
    
    def check_model_cnn(self,imgPath):
        return False
    
    def check_product(self, imgPath):
        if self.check_type == 'rule-base':
            if not self.check_model1(self,imgPath):
                return False
            elif not self.check_model2(self,imgPath):
                return False
            elif not self.check_model3(self,imgPath):
                return False
            else: return True
        else:
            self.check_model_cnn(self,imgPath)
    
    def check_folder(self):
        self.result = ['OK' if self.check_product(self.folderPath+imgName) else 'NG' for imgName in os.listdir(self.folderPath)]
