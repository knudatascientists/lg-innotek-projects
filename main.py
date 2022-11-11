#  통합 파일
from epoxy_check import EpoxyCheck
from settings import *

checkModel = EpoxyCheck.from_path(FOLDER_PATH)
checkModel.check_folder()
print(checkModel.result)