# -*- encoding: utf-8 -*-
#!/usr/bin/env python

import json
import os
import sys
import sqlite3

from flask import Flask, request, render_template
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import create_engine, MetaData

app = Flask(__name__)
app.debug = True

if getattr(sys, 'frozen', False):
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
  'categoria-produto': Table('CATEGORIA PRODUTO', metadata, autoload=True),
  'cliente': Table('CLIENTE', metadata, autoload=True),
  'cobranca': Table('COBRANCA', metadata, autoload=True),
  'cor': Table('COR', metadata, autoload=True),
  'diagnostico': Table('DIAGNOSTICO', metadata, autoload=True),
  'distribuidor-produto': Table('DISTRIBUIDOR PRODUTO', metadata, autoload=True),
  'doenca': Table('DOENCA', metadata, autoload=True),
  'especie': Table('ESPECIE', metadata, autoload=True),
  'fabricante-produto': Table('FABRICANTE PRODUTO', metadata, autoload=True),
  'fabricante-vacina': Table('FABRICANTE VACINA', metadata, autoload=True),
  'lixo1': Table('lixo1', metadata, autoload=True),
  'movimento-produto': Table('MOVIMENTO PRODUTO', metadata, autoload=True),
  'ocorrencia': Table('OCORRENCIA', metadata, autoload=True),
  'produto': Table('PRODUTO', metadata, autoload=True),
  'produto1': Table('PRODUTO1', metadata, autoload=True),
  'propriedade-produto': Table('PROPRIEDADE PRODUTO', metadata, autoload=True),
  'raca': Table('RACA', metadata, autoload=True),
  'subdiagnostico': Table('SUBDIAGNOSTICO', metadata, autoload=True),
  'tipo-movimento-produto': Table('TIPO MOVIMENTO PRODUTO', metadata, autoload=True),
  'tipo-vacina': Table('TIPO VACINA', metadata, autoload=True),
  'vacina-aplicada': Table('VACINA APLICADA', metadata, autoload=True),
  'tipo-vacina-x-doenca': Table('TIPO VACINA x DOENCA', metadata, autoload=True),
  'unidade': Table('UNIDADE', metadata, autoload=True),
  'vacina-planejada': Table('VACINA PLANEJADA', metadata, autoload=True),
  'atendimento': Table('ATENDIMENTO', metadata, autoload=True),
  'paciente': Table('PACIENTE', metadata, autoload=True),
}

conn = engine.connect()

@app.route('/favicon.ico')
def nothing():
    return ''

@app.route('/<table_name>/<id>/', methods=['GET'])
@app.route('/<table_name>/', methods=['GET'])
def get(table_name, id=None):
    table = tables[table_name]
    offset = request.args.get('from', 0)
    limit = request.args.get('show', 20)

    try:
        pk = table.primary_key.columns.keys()[0]
    except IndexError:
        pk = None
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
    if not getattr(sys, 'frozen', False):
        app.run('0.0.0.0')
    else:
        import webbrowser
        import threading
        import random

        port = 5000 + random.randint(0, 999)
        url = 'http://127.0.0.1:%s' % port

        threading.Timer(1.45, lambda: webbrowser.open(url)).start()
        app.run(port=port, debug=False)
