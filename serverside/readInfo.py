def Read():
    file = open("./files/infoDoGrupo.txt", "r", encoding = "utf-8")
    configs = file.read().split("\n")
    res = {}

    for config in configs:
        res[config.split("=")[0].strip()] = config.split("=")[1].strip()
    file.close()
    return res
