import json
import sqlite3
from setkey import setKey

def Relacione(Tupla: dict, NomeDaTabela: list[str]) -> dict:
    with open("./files/relacoes.json", "r", encoding = "utf-8") as file:
        configs = json.load(file)
        for config in configs:
            if config["nome"] == NomeDaTabela:
                conn = sqlite3.connect('./bd/young6ix.db')
                cursor = conn.cursor()
                for relacao in config["relações"]:
                    if Tupla[relacao[0]] is None:
                        continue
                    cursor.execute(f"""SELECT * FROM {relacao[2]}
                        WHERE {relacao[1]} = {Tupla[relacao[0]]};""")
                    
                    Tupla[relacao[0]] = setKey(
                        cursor.fetchone(),
                        ["id", "nome", "data"])
                conn.close()
        return Tupla