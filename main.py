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
imlec = db.cursor()

@app.route('/')
def index():
    return "Mobil Uygulama için servisler..."


@app.route('/api')
def Siranoalvegetir():
    imlec.execute("INSERT INTO Numbers VALUES('Bekliyor')")
    db.commit()
    imlec.execute('SELECT TOP(1)Id FROM Numbers order by Id desc')
    d = {"res": imlec.fetchone()}
    return jsonify(d)


@app.route('/api/deneme/<sirano>', methods=['PUT'])
def Islemisonlandir(sirano):
    imlec.execute("Update Numbers Set Islemdurumu = ('Tamamlandı') Where Id = ('"+sirano+"')")
    db.commit()
    return "islem tamamlandı"

@app.route('/api/islemal/<sirano>', methods=['PUT'])
def islemeal(sirano):
    #imlec.execute("SELECT MIN(Id) FROM Numbers where Islemdurumu=('Bekliyor')")
    imlec.execute("Update Numbers Set Islemdurumu = ('İşleniyor') Where Id = ('"+sirano+"')")
    db.commit()
    return "isleme alındı"


if __name__ == "__main__":
    app.run(debug=True)