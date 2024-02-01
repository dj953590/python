import configparser
configpath = '../cfg/rag.ini'

def loadconfig() -> configparser:
    config = configparser.ConfigParser()
    config.read(configpath)
    return config 