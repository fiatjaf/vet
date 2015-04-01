#!/usr/bin/env python

import json
import os
import sys

from flask import Flask, request, render_template
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import create_engine, MetaData

app = Flask(__name__)
app.debug = True

print getattr(sys, 'frozen')
if getattr(sys, 'frozen'):
    print sys.executable
    here = sys.executable
else:
    here = os.path.realpath(__file__)
db = os.path.join(os.path.dirname(here), 'Paciente.db')

print db
print open(db)
connstring = 'sqlite:///' + db
print connstring

engine = create_engine(connstring, convert_unicode=True)
print engine
print engine.__dict__

metadata = MetaData(bind=engine)

tables = {
  'cores': Table('COR', metadata, autoload=True),
  'pacientes': Table('PACIENTE', metadata, autoload=True),
  'clientes': Table('CLIENTE', metadata, autoload=True),
  'atendimentos': Table('ATENDIMENTO', metadata, autoload=True),
  'vacinas-aplicadas': Table('VACINA APLICADA', metadata, autoload=True),
  'vacinas-agendadas': Table('VACINA PLANEJADA', metadata, autoload=True)
}

conn = engine.connect()

@app.route('/favicon.ico')
def nothing():
    return ''

@app.route('/<table_name>/<id>/', methods=['POST'])
@app.route('/<table_name>/', methods=['POST'])
def post(table_name, id=None):
    table = tables[table_name]
    if not id:
        o = conn.execute(table.insert(), **request.form)
    else:
        o = conn.execute(table.update(), **request.form)
    return render_template('raw.html', data=o)

@app.route('/<table_name>/<id>/', methods=['GET'])
@app.route('/<table_name>/', methods=['GET'])
def get(table_name, id=None):
    table = tables[table_name]
    offset = request.args.get('from', 0)
    limit = request.args.get('show', 20)

    pk = table.primary_key.columns.keys()[0]
    fk = {}
    if id:
        o = table.select(getattr(table.c, pk) == id).execute().first()
        return render_template('entity.html',
                               columns=table.columns.keys(),
                               data=o,
                               table_name=table_name,
                               primary_key=pk,
                               foreign_keys=fk)
    else:
        r = table.select().offset(offset).limit(limit).execute().fetchall()
        return render_template('entities.html',
                               columns=table.columns.keys(),
                               rows=r,
                               table_name=table_name,
                               primary_key=pk,
                               foreign_keys=fk)

@app.route('/')
def index():
    return render_template('list.html', list=tables, name="Tabelas")

if __name__ == '__main__':
    import webbrowser
    import threading
    import random

    port = 5000 + random.randint(0, 999)
    url = 'http://127.0.0.1:%s' % port

    threading.Timer(1.45, lambda: webbrowser.open(url)).start()
    app.run(port=port, debug=False)
