import os

import pandas as pd


class productTest:
    def __init__(self, input_path="./log_merge_proj_data/Input/"):
        """제품 검사 클래스 생성

        Args:
            input_path (str, optional): 검사 수치 csv 폴더 경로
            Defaults to "./log_merge_proj_data/Input/".
        """
        self.input_path = input_path
        self.input_data_names = os.listdir(input_path)

    def get_data(self, data_name):
        """csv 파일 불러오기

        Args:
            data_name (str): 폴더 내의 csv 파일 명.cvs

        Returns:
            data (pd.DataFrame): 각 제품 별 검사 측정 값
            data_limit (pd.DataFrame): 문서 상단의 검사 항목 별 임계 값
        """
        data = pd.read_csv(self.input_path + data_name, header=2)
        data_limit = pd.read_csv(
            self.input_path + data_name, header=None, names=data.columns
        ).iloc[:2, 1:]

        # 검사 제품 barcode가 최근 검사 자료만 남도록 중복 제거
        data.drop_duplicates(["barcode"], keep="last", inplace=True)
        data.reset_index(inplace=True, drop=True)
        return data, data_limit

    def getBarcodes(self):
        """각 검사 내의 중복하는 barcode만 필터링"""
        data, data_limit = self.get_data(self.input_data_names[0])
        self.barcode = set(data["barcode"])
        for data_name in self.input_data_names[1:]:
            data, data_limit = self.get_data(data_name)
            self.barcode = self.barcode & set(data["barcode"])
        self.barcode = list(self.barcode)

    def returnResult(self):
        """검사 결과 중 이상치를 보인 검사 항목의 column명을 결과로 반환

        Returns:
            _type_: _description_
        """
        self.result = ["pass" for i in range(len(self.barcode))]
        for col in self.total_limit.columns:
            low, high = list(map(float, self.total_limit[col]))
            self.result = [
                " ".join([r, col]) if d <= low or d >= high else r
                for r, d in zip(self.result, self.total[col])
            ]
        self.result = [r if r == "pass" else r[5:] for r in self.result]

    def dataMerge(self):
        """검사 수치 자료 통합"""
        self.getBarcodes()
        self.datas = []
        self.data_limits = []

        # 각 검사 결과에서 필터링
        for data_name in self.input_data_names:
            data, data_limit = self.get_data(data_name)
            data.set_index("barcode", inplace=True)
            self.data_limits.append(data_limit)
            data = data.loc[self.barcode, :]
            data.sort_index(inplace=True)
            self.datas.append(data)

        # 필터링한 자료와 임계값 자료를 통합
        self.total = pd.concat(self.datas, axis=1)
        self.total_limit = pd.concat(self.data_limits, axis=1)

        # 검사 결과를 result 열로 추가
        self.returnResult()
        self.total["result"] = self.result
        self.total.reset_index(inplace=True)

        self.total_limit = self.total_limit.rename(
            index={0: "low limit", 1: "high limit"}
        ).reset_index()

    def saveOutput(self, name="./work/output2.csv"):
        """출력 형식 맞춘 후 csv 파일로 저장

        Args:
            name (str): 저장 파일 경로/이름
        """
        total = self.total.copy()
        total_limit = self.total_limit.copy()
        total_limit["result"] = ["", ""]
        total_limit.rename(columns={"index": "barcode"}, inplace=True)

        total_limit = total_limit.astype("str")
        total = total.astype("str")
        total_limit.loc[2, :] = total_limit.columns

        self.output = pd.concat([total_limit, total])
        self.output.to_csv(name, index=False, header=False)


if __name__ == "__main__":
    test = productTest("./work/log_merge_proj_data/Input/")
    test.dataMerge()
    test.saveOutput("./work/output2.csv")
