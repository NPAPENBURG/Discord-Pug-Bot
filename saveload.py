import pickle


def loadMatchHistory():
    try:
        return pickle.load(open("data/matchHistory.p", "rb"))
    except FileNotFoundError:
        return []  # return blank history on new setup


def writeMatchHistory(variable):
    pickle.dump(variable, open("data/matchHistory.p", "wb"))


def loadMatchCount():
    try:
        return pickle.load(open("data/matchCount.p", "rb"))
    except FileNotFoundError:
        return 0  # return an empty match count if no file exists


def writeMatchCount(variable):
    pickle.dump(variable, open("data/matchCount.p", "wb"))


def loadPlayerPool():
    try:
        return pickle.load(open("data/playerPool.p", "rb"))
    except FileNotFoundError:
        return []  # return empty pool on first run


def writePlayerPool(variable):
    pickle.dump(variable, open("data/playerPool.p", "wb"))





