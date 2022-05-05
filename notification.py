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

@app.route('/apii/bekleyensayisigoster', methods = ['POST'])
def bekleyensayisigoster():
    id = request.form['Id']
    imlec = db.cursor()
    d = imlec.execute("Select count(Id) from Numbers where (Transactionstatus=('Bekliyor') or Transactionstatus=('İşleniyor')) and Id<(SELECT TOP(1)Id FROM Numbers WHERE Studentnumber= '"+id+"' order by Id desc)").fetchone()
    print(jsonify(d))
    return jsonify(d)


if __name__ == "__main__":
    app.run(debug=True,port=5001)