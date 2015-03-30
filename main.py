#!/usr/bin/env python

import json

from flask import Flask, request, render_template
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

@app.route('/favicon.ico')
def nothing():
    return ''

@app.route('/<table_name>/<id>/', methods=['POST'])
@app.route('/<table_name>/', methods=['POST'])
def p(table_name, id=None):
    table = tables[table_name]
    if not id:
        o = conn.execute(table.insert(), **request.form)
    else:
        o = conn.execute(table.update(), **request.form)
    return render_template('raw.html', data=o)

@app.route('/<table_name>/<id>/', methods=['GET'])
@app.route('/<table_name>/', methods=['GET'])
def g(table_name, id=None):
    table = tables[table_name]
    if id:
        pk = table.primary_key.columns.values()[0].description
        o = table.select(getattr(table.c, pk) == id).execute().first()
        return render_template('entity.html', entity=o)
    else:
        r = table.select().limit(20).execute().fetchall()
        return render_template('entities.html',
                               rows=r,
                               name=table_name.replace('-', ' '))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.run(host='0.0.0.0')
    else:
        import webbrowser
        import threading
        import random

        port = 5000 + random.randint(0, 999)
        url = 'http://127.0.0.1:%s' % port

        threading.Timer(1.25, lambda: webbrowser.open(url)).start()
        app.run(port=port, debug=False)
