import base64
import datetime
import time

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

@app.route('/api', methods = ['POST'])
def Siranoalvegetir():
    id = request.form['Id']
    imlec = db.cursor()
    imlec.execute("INSERT INTO Numbers VALUES('Bekliyor','"+id+"')")
    db.commit()
    d=imlec.execute("SELECT TOP(1)Id FROM Numbers WHERE Studentnumber= '"+id+"' order by Id desc").fetchone()
    return {"res": d}

@app.route('/api/giriskontrol', methods = ['POST'])
def giriskontrol():
    id = request.form['Id']
    imlec = db.cursor()
    p=imlec.execute("SELECT Id FROM Users WHERE Id='"+id+"'").fetchone()
    if p:
        return "true"
    else:
        return "Yanlış Kullanıcı Adı veya Şifre"

@app.route('/api/kayit' , methods = ['POST'])
def kayit():
    id = request.form['Id']
    imlec = db.cursor()
    imlec.execute("INSERT INTO Users(Id) VALUES('"+id+"')")
    db.commit()
    return "true"


#@app.route('/api/bildirimonkisi', methods = ['POST'])
#def Bildirimonkisi():
#    id = request.form['Id']
#    imlec = db.cursor()
#    imlec.execute("Select count(Id) from Numbers where Transactionstatus=('Bekliyor') and Id<(SELECT TOP(1)Id FROM Numbers WHERE Studentnumber= '" + id + "' order by Id desc)").fetchone()
#    return "true"

@app.route('/api/islemisonlandir')
def Islemisonlandir():
    imlec = db.cursor()
    imlec.execute("SELECT MIN(Id) FROM Numbers where Transactionstatus=('İşleniyor')").fetchone()
    imlec.execute("Update Numbers Set Transactionstatus = ('Tamamlandı') Where Id = (SELECT MIN(Id) FROM Numbers where Transactionstatus=('İşleniyor'))")
    db.commit()
    return "islem tamamlandı"

@app.route('/api/islemal')
def islemal():
    imlec = db.cursor()
    imlec.execute("SELECT MIN(Id) FROM Numbers where Islemdurumu=('Bekliyor')").fetchone()
    imlec.execute("Update Numbers Set Transactionstatus = ('İşleniyor') Where Id = (SELECT MIN(Id) FROM Numbers where Transactionstatus=('Bekliyor'))")
    db.commit()
    return "isleme alındı"

@app.route('/api/islemdekinigoster')
def islemdekinigoster():
    imlec = db.cursor()
    d=imlec.execute("SELECT MIN(Id) FROM Numbers where Transactionstatus=('İşleniyor')").fetchone()
    return jsonify(d)

@app.route('/api/gunsonu')
def gunsonu():
    imlec = db.cursor()
    d=imlec.execute("SELECT COUNT(Id) FROM Numbers WHERE Transactionstatus = ('Tamamlandı')").fetchone()
    imlec.execute("TRUNCATE TABLE Numbers")
    db.commit()
    return jsonify(d)

@app.route('/api/bekleyensayisigoster', methods = ['POST'])
def bekleyensayisigoster():
    id = request.form['Id']
    imlec = db.cursor()
    d = imlec.execute("Select count(Id) from Numbers where Transactionstatus=('Bekliyor') and Id<(SELECT TOP(1)Id FROM Numbers WHERE Studentnumber= '"+id+"' order by Id desc)").fetchone()
    return {"res":d}

if __name__ == "__main__":
    app.run(debug=True)