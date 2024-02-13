import urllib.request
import os
def create_dir_if_not_exist(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
create_dir_if_not_exist("e2e-dataset")
url = "https://raw.githubusercontent.com/tuetschek/e2e-dataset/master/trainset.csv"
urllib.request.urlretrieve(url, "./e2e-dataset/trainset.csv")