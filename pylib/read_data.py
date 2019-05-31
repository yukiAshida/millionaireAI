import glob
import pickle

data_dir = "..\\data\\"

# 解析方法によって、今後書き換える必要がありそう

# pickleファイルからデータを取り出す
def open_pickle(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    return data



# ログを読み込むためのイテレータクラス
class ReadLogIterator():
    def __init__(self,month,day,ex_id,year = 2019):
        month_10 = month//10
        month_01 = month%10
        day_10 = day//10
        day_01 = day%10
        tmp_pickle_file_name = data_dir + "match_log\\{}_{}{}_{}{}_{}\\*.pickle".format(year,month_10,month_01,day_10,day_01,ex_id)
        self.pickle_file_name = glob.glob(tmp_pickle_file_name)
        self.data_len = len(self.pickle_file_name)
        self.index = 0

    def __iter__(self):
        # __next__()はselfが実装してるのでそのままselfを返す
        return self

    def __next__(self):  # Python2だと next(self) で定義
        if self.index == self.data_len:
            raise StopIteration()
        file_name = self.pickle_file_name[self.index]
        data = open_pickle(file_name)
        self.index += 1
        return data


if __name__ == "__main__":

    month = 5
    day = 31
    
    read_log_iter = ReadLogIterator(month,day,0)
    for data in read_log_iter:
        print(data["rank"])

    # year = 2019
    # month_10 = month//10
    # month_01 = month%10
    # day_10 = day//10
    # day_01 = day%10
    # file_name = data_dir + "match_log\\{}_{}{}_{}{}".format(year,month_10,month_01,day_10,day_01)
    # print(glob.glob(file_name))




