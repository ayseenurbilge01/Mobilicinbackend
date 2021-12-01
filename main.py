import base64
import datetime

from bson import ObjectId
from flask import Flask, jsonify, render_template, request, redirect, session
import json
import pypyodbc

class ObjectIdEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(ObjectIdEncoder, self).default(obj)

app = Flask(__name__)
app.secret_key = 'bizim cok zor gizli sozcugumuz'
app.json_encoder = ObjectIdEncoder

db = pypyodbc.connect(
        'Driver={SQL Server};'
        'Server=LAPTOP-EEFUFS2L\SQLEXPRESS;'
        'Database=DbQ-Matic;'
        'Trusted_Connection=True;'
    )

@app.route('/api')
def Siranoalvegetir():
    imlec = db.cursor()
    imlec.execute("INSERT INTO Numbers VALUES('Bekliyor')")
    db.commit()
    d=imlec.execute('SELECT TOP(1)Id FROM Numbers order by Id desc').fetchone()
    return {"res": d}

@app.route('/api/giriskontrol/<Id>/<Password>')
def giriskontrol(Id,Password):
    imlec = db.cursor()
    p=imlec.execute("SELECT Password FROM Users WHERE Id="+Id).fetchone()
    if p:
        d=imlec.execute("SELECT Id FROM Users WHERE Password='"+Password+"' and Id='"+Id+"'").fetchone()
        if d:
            return {"res": d}
        else:
            return "Yanlış Şifre"
    else:
        return "Yanlış Kullanıcı Adı"

@app.route('/api/islemisonlandir')
def Islemisonlandir():
    imlec = db.cursor()
    imlec.execute("SELECT MIN(Id) FROM Numbers where Islemdurumu=('İşleniyor')").fetchone()
    imlec.execute("Update Numbers Set Islemdurumu = ('Tamamlandı') Where Id = (SELECT MIN(Id) FROM Numbers where Islemdurumu=('İşleniyor'))")
    db.commit()
    return "islem tamamlandı"

@app.route('/api/islemal')
def islemal():
    imlec = db.cursor()
    imlec.execute("SELECT MIN(Id) FROM Numbers where Islemdurumu=('Bekliyor')").fetchone()
    imlec.execute("Update Numbers Set Islemdurumu = ('İşleniyor') Where Id = (SELECT MIN(Id) FROM Numbers where Islemdurumu=('Bekliyor'))")
    db.commit()
    return "isleme alındı"

@app.route('/api/islemdekinigoster')
def islemdekinigoster():
    imlec = db.cursor()
    d=imlec.execute("SELECT MIN(Id) FROM Numbers where Islemdurumu=('İşleniyor')").fetchone()
    return jsonify(d)

@app.route('/api/gunsonu')
def gunsonu():
    imlec = db.cursor()
    d=imlec.execute("SELECT COUNT(Id) FROM Numbers WHERE Islemdurumu = ('Tamamlandı')").fetchone()
    imlec.execute("TRUNCATE TABLE Numbers")
    db.commit()
    return jsonify(d)

@app.route('/api/bekleyensayisigoster')
def bekleyensayisigoster():
    imlec = db.cursor()
    d = imlec.execute("Select count(Id) from Numbers where Islemdurumu=('Bekliyor') and Id<(SELECT TOP(1)Id FROM Numbers order by Id desc)").fetchone()
    return {"res":d}

if __name__ == "__main__":
    app.run(debug=True)