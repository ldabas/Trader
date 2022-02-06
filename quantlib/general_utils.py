from msilib.schema import File
import pickle

def save_file(path,object):
    try:
        with open(path, "wb") as fp:
            pickle.dump(object, fp)

    except Exception as err:
        print("pickle error: ", str(err))


def load_file(path):
    try:
        with open(path, "rb") as fp:
            file = pickle.load(fp)

        return file

    except Exception as err:
        print("Load Error ", err)