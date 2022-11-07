
from predict_models.model3_hs import *
from settings import *
import os

class EpoxyCheck:
    def __init__(self, folderPath= ''):
        if folderPath =='':
            self.folderPath = FOLDER_PATH
        else:
            self.folderPath = folderPath
        self.result = ['NG' for i in range(len(os.listdir(self.folderPath))) ]


    @classmethod
    def from_path(cls, folderPath):
        return cls(folderPath)

    def check_model1(self):
        pass
    
    def check_model2(self):
        pass
    
    def check_model3(self):
        pass
    
    def check_model_cnn(self):
        pass
    
    def check_product(self):
        pass
    