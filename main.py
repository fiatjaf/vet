import json

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import create_engine, MetaData

app = Flask(__name__)
app.debug = True

engine = create_engine('sqlite:///Paciente.db', convert_unicode=True)
metadata = MetaData(bind=engine)

tables = {
  'cor': Table('COR', metadata, autoload=True),
  'paciente': Table('PACIENTE', metadata, autoload=True),
}

conn = engine.connect()

@app.route('/<table>/<id>/', methods=['POST'])
@app.route('/<table>/', methods=['POST'])
def p(table, id=None):
    table = tables[table]
    if not id:
        o = conn.execute(table.insert(), **request.form)
    else:
        o = conn.execute(table.update(), **request.form)
    return render_template('raw.html', data=o)

@app.route('/<table>/<id>/', methods=['GET'])
@app.route('/<table>/', methods=['GET'])
def g(table, id=None):
    table = tables[table]
    if id:
        pk = table.primary_key.columns.values()[0].description
        o = table.select(getattr(table.c, pk) == id).execute().first()
        return render_template('raw.html', data=o)
    else:
        r = table.select().limit(20).execute().fetchall()
        return render_template('raw.html', data=r)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
