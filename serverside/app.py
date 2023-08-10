from flask import (
    Flask,
    redirect,
    url_for,
    Response,
    Request,
    jsonify,
    send_file,
    request
)
from flask_cors import CORS

import sqlite3
from readInfo import Read
from relacao import Relacione
from setkey import setKey
from datetime import datetime
import os
import json

app = Flask(__name__)

# Configurando o App

CORS(app)
file = open("./files/config.json")
configs = json.load(file)
file.close()
UPLOAD_FILE   = configs["UPLOAD_FILE"]
DOMINIO       = configs["DOMINIO"]
AUTHORIZATION = configs["AUTHORIZATION"]

def noUser():
    response = jsonify("FORBIDDEN: você não tem permissão para acessar esta rota")
    response.status_code = 403
    return response

def Autorizado():
    if request.authorization is None: return False
    return request.authorization.token == AUTHORIZATION.split(" ")[1]

def security_name(path: str) -> str:
    name  = path.split("/")[-1]
    path1 = "/".join(path.split("/")[:-1])
    try:
        files = os.listdir(path1)
        if name in files:
            noExt = ".".join(name.split(".")[:-1])
            Ext   = name.split(".")[-1]
            if noExt.split("_")[-1].isnumeric() and (not noExt.isnumeric()):
                n = int(noExt.split("_")[-1]) + 1
                res = f"{path1}/{noExt}_{n}.{Ext}"
                if res in files:
                    return security_name(res)
                return res
            res = f"{path1}/{noExt}_1.{Ext}"
            if res in files:
                return security_name(res)
            return res
        return path
    except:
        return path

def setCab(response: Response) -> Response:
    
    response.access_control_allow_origin = 'http://localhost:8080'
    return response

@app.route("/api/info")
def info():
    response = jsonify(Read())
    response = setCab(response)
    return response

@app.route("/api/getfile/<file>")
def getFile(file):
    response = send_file(f"{UPLOAD_FILE}/{file}")
    response = setCab(response)
    return response

@app.route("/api/getpath/<file>")
def getpath(file):
    response = jsonify({"path": f"http://localhost:5000/api/getfile/{file}"})
    response = setCab(response)
    return response

@app.route("/api/getmusics")
def getmusics():
    conn = sqlite3.connect('./bd/young6ix.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM musicas order by data;")
    keys = ["id", "nome", "autores", "participantes", "views", "data", "ep", "album", "single"]
    response = jsonify([Relacione(setKey(item, keys), "musicas") for item in cursor.fetchall()])
    
    conn.close()
    response = setCab(response)
    return response

@app.route("/api/getgroup/<group>")
def getgruops(group):
    conn = sqlite3.connect('./bd/young6ix.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {group};")
    keys = ["id", "nome", "data"]
    response = jsonify([setKey(item, keys) for item in cursor.fetchall()])
    
    conn.close()
    response = setCab(response)
    return response

@app.route("/api/geteventus")
def geteventos():
    conn = sqlite3.connect('./bd/young6ix.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM eventos ORDER BY dataevent DESC;")
    keys = ["id", "titulo", "capa", "conteudo", "datapub", "dataevent"]
    response = jsonify([setKey(item, keys) for item in cursor.fetchall()])
    
    conn.close()
    response = setCab(response)
    return response

@app.route("/api/getcomentarios")
def getcomentarios():
    conn = sqlite3.connect('./bd/young6ix.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM comentarios ORDER BY id DESC;")
    keys = ["id", "conteudo", "entidadeid", "entidadename", "data"]
    response = jsonify([setKey(item, keys) for item in cursor.fetchall()])
    
    conn.close()
    response = setCab(response)
    return response

@app.route("/api/getusuarios")
def usuario():
    conn = sqlite3.connect('./bd/young6ix.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM usuario;")
    keys = ["id", "nome", "contacto", "capa", "senha"]
    response = jsonify([setKey(item, keys) for item in cursor.fetchall()])
    
    conn.close()
    response = setCab(response)
    return response

@app.route("/api/getimgs")
def getimgs():
    conn = sqlite3.connect('./bd/young6ix.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM img ORDER BY data;")
    keys = ["id", "path", "data", "titulo"]
    response = jsonify([setKey(item, keys) for item in cursor.fetchall()])
    
    conn.close()
    response = setCab(response)
    return response

@app.route("/api/login", methods = ["POST"])
def login():
    data = request.get_json(force = True)
    conn = sqlite3.connect('./bd/young6ix.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM usuario WHERE nome = '{data['nome']}' AND senha = '{data['senha']}';")
    keys = ["id", "nome", "contacto", "capa", "senha"]
    
    user = cursor.fetchone()
    response = None
    if user is None:
        response = jsonify(None)
    else:
        response = jsonify({
            "usuario"      : [setKey(item, keys) for item in [user]][0],
            "authorization": AUTHORIZATION
        })
    
    conn.close()
    response = setCab(response)
    return response

@app.route("/api/altertema", methods = ["POST"])
def altertema():
    if not Autorizado(): return noUser()
    
    tema = request.files["TEMA"]
    tema.save(UPLOAD_FILE+"/TEMA.jpg")

    return redirect(url_for("getpath", file = "TEMA.jpg"))

@app.route("/api/comentar/<entidaeName>/<entidadeId>", methods = ["POST"])
def comentar(entidaeName, entidadeId):
    data = request.get_json(force = True)
    conn = sqlite3.connect('./bd/young6ix.db')
    cursor = conn.cursor()

    conteudo = request.get_json(force = True)["conteudo"]
    
    data = datetime.now()
    data = f"{data.year}-{data.month}-{data.day}"

    cursor.execute("""
        INSERT INTO comentarios (conteudo, entidadeid, entidadename, data) 
        VALUES (?, ?, ?, ?)
    """,(conteudo, entidadeId, entidaeName, data))

    cursor.execute(f"SELECT *,MAX(id) FROM comentarios;")
    keys = ["id", "conteudo", "entidadeid", "entidadename", "data"]

    comentario = cursor.fetchone()
    response = jsonify([setKey(item, keys) for item in [comentario]][0])
    
    conn.commit()
    conn.close()
    
    response = setCab(response)
    return response

@app.route("/api/visualizar/<id_music>", methods = ["POST"])
def visualizar(id_music):
    conn = sqlite3.connect('./bd/young6ix.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT views FROM musicas WHERE id = {id_music}")
    musica = cursor.fetchone()
    musica = [setKey(item, ["views"]) for item in [musica]][0]

    cursor.execute(f"UPDATE musicas SET views = {musica['views'] + 1} WHERE id = {id_music}")
    
    conn.commit()
    conn.close()

    response = jsonify(musica['views'] + 1)
    response = setCab(response)

    return response

@app.route("/api/insert/<table>", methods = ["POST"])
@app.route("/api/insert/<table>/<id_entidade>", methods = ["PUT", "DELETE"])
def insert(table, id_entidade = None):
    if not Autorizado(): return noUser()
    
    if request.method == "DELETE" or request.method == "PUT":
        conn = sqlite3.connect('./bd/young6ix.db')
        cursor = conn.cursor()

        file = open("./bd/files.json")
        keys = json.load(file).get(table)
        file.close()
        
        if keys is not None:
            cursor.execute(f"SELECT {','.join(keys)} FROM {table} WHERE id = {id_entidade};")

            user = cursor.fetchone()
            user = [setKey(item, keys) for item in [user]][0]

            for key, value in user.items():
                if value is not None and\
                   ((request.files.get(key) is not None) or\
                    request.method == "DELETE"):
                      file = value.split("/")[-1]
                      exts = ["mp3", "m4p", "jpg", "png"]
                      for ext in exts:
                          EXT = "" if len(value.split("/")) > 1 else "."+ext
                          if os.path.exists(UPLOAD_FILE+"/"+file.replace(" ", "_")+EXT):
                              os.remove(UPLOAD_FILE+"/"+file.replace(" ", "_")+EXT)
                              break

        if request.method == "DELETE":
            cursor.execute(f"DELETE FROM {table} WHERE id = {id_entidade};")
            conn.commit()
            conn.close()

            response = jsonify(None)
            response = setCab(response)
            
            return response

    data = request.form
    camposno = ",".join([f"{campo}=?" for campo in data.keys()])
    campos   = ",".join([campo for campo in data.keys()])
    no       = ",".join(["?" for _ in data])
    values   = [
        None if value == "undefined" or value == "null" else
        1 if value == "true" else
        0 if value == "false" else
        value
        for value in data.values()
    ]
    
    if request.method == "POST":
        if not table == "usuario":
            date = datetime.now()
            date = f"{date.year}-{date.month}-{date.day}"

            campos += ",data"
            no     += ",?"
            values.append(date)

    files = request.files
    for key, file in files.items():
        path = security_name(UPLOAD_FILE+"/"+file.filename)
        name = path.split("/")[-1]
        file.save(path.replace(" ", "_"))
        
        camposno += f",{key}=?"
        campos   += f",{key}"
        no       += ",?"
        if table == "musicas":
            values.append(".".join(name.split(".")[:-1]))
        else:    
            values.append(DOMINIO+"/api/getfile/"+name)

    conn = sqlite3.connect('./bd/young6ix.db')
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute(f"INSERT INTO {table} ({campos}) VALUES ({no});", values)
        cursor.execute(f"SELECT *,MAX(id) FROM {table};")
    elif request.method == "PUT":
        cursor.execute(f"UPDATE {table} SET {camposno}  WHERE id = {id_entidade};", values)
        cursor.execute(f"SELECT * FROM {table} WHERE id = {id_entidade};")
    
    keys = {
        "albums" : ["id", "nome", "data"],
        "eps"    : ["id", "nome", "data"],
        "eventos": ["id", "titulo", "capa", "conteudo", "data", "dataevent"],
        "img"    : ["id", "path", "data", "titulo"],
        "musicas": ["id", "nome", "autores", "participantes", "views", "data", "ep", "album", "single"],
        "usuario" : ["id", "nome", "contacto", "senha"]
    }[table]

    entidade = cursor.fetchone()
    response = None
    if entidade is None:
        response = jsonify(None)
    else:
        response = jsonify([setKey(item, keys) for item in [entidade]][0])
    
    conn.commit()
    conn.close()
    
    response = setCab(response)
    return response
    
if __name__ == "__main__":
    app.run(debug = True)