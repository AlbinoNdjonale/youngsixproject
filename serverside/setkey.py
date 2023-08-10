def setKey(List: tuple, keys: list) -> dict:
    res = {}
    for key in range(len(keys)):
        res[keys[key]] = List[key]
    return res