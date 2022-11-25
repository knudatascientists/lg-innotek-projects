#  통합 파일
from epoxy_check import EpoxyCheck
from settings import *

# checkModel = EpoxyCheck.from_path(FOLDER_PATH)
# checkModel.check_folder(test = True)
# print(checkModel.result)

checkModel = EpoxyCheck()

# checkModel.check_product(test_np_path1, test_only=1, show=True)
# checkModel.check_product(test_np_path2, test_only=2, show=True)
checkModel.check_product(test_np_path3, test_only=3, show=True)

# for _ in range(10000):
#     print("영효형 바보")
