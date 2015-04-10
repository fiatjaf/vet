# -*- encoding: utf-8 -*-
#!/usr/bin/env python

import datetime
import json
import os
import sys
import sqlite3
import urllib
import urlparse

from flask import Flask, request, render_template, redirect
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import create_engine, MetaData
from utils import memoize

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

engine = create_engine(connstring, echo=False)
print engine
print engine.__dict__

metadata = MetaData(bind=engine)
conn = engine.connect()

tables = {
  'categoria-produto': {
    'table': Table('CATEGORIA PRODUTO', metadata, autoload=True),
    'name_column': 'NomeCategoria',
  },
  'clientes': {
    'table': Table('CLIENTE', metadata, autoload=True),
    'name_column': 'NomeCliente',
    'sort_column': 'NomeCliente',
  },
  'cobrancas': {
    'table': Table('COBRANCA', metadata, autoload=True),
    'name_column': 'data',
  },
  'cores': {
    'table': Table('COR', metadata, autoload=True),
    'name_column': 'NomeCor',
  },
  'diagnosticos': {
    'table': Table('DIAGNOSTICO', metadata, autoload=True),
    'name_column': 'DescricaoDiagnostico',
  },
  'distribuidor-produto': {
    'table': Table('DISTRIBUIDOR PRODUTO', metadata, autoload=True),
    'name_column': 'NomeDistribuidor',
  },
  'doencas': {
    'table': Table('DOENCA', metadata, autoload=True),
    'name_column': 'NomeDoenca',
  },
  'especies': {
    'table': Table('ESPECIE', metadata, autoload=True),
    'name_column': 'NomeEspecie',
  },
  'fabricante-produto': {
    'table': Table('FABRICANTE PRODUTO', metadata, autoload=True),
    'name_column': 'NomeFabricante',
  },
  'fabricante-vacina': {
    'table': Table('FABRICANTE VACINA', metadata, autoload=True),
    'name_column': 'NomeFabricante',
  },
  'lixo1': {
    'table': Table('lixo1', metadata, autoload=True),
    'name_column': 'MáxDeDataAtendimento',
  },
  'movimento-produto': {
    'table': Table('MOVIMENTO PRODUTO', metadata, autoload=True),
    'name_column': 'ValorMovimento',
  },
  'ocorrencias': {
    'table': Table('OCORRENCIA', metadata, autoload=True),
    'name_column': 'DescricaoOcorrencia',
  },
  'produtos': {
    'table': Table('PRODUTO', metadata, autoload=True),
    'name_column': 'NomeProduto',
  },
  'produto1': {
    'table': Table('PRODUTO1', metadata, autoload=True),
    'name_column': 'NomeProduto',
  },
  'propriedade-produto': {
    'table': Table('PROPRIEDADE PRODUTO', metadata, autoload=True),
    'name_column': 'DescricaoPropriedade',
  },
  'racas': {
    'table': Table('RACA', metadata, autoload=True),
    'name_column': 'NomeRaca',
  },
  'subdiagnosticos': {
    'table': Table('SUBDIAGNOSTICO', metadata, autoload=True),
    'name_column': 'DescricaoSubDiagnostico',
  },
  'tipo-movimento-produto': {
    'table': Table('TIPO MOVIMENTO PRODUTO', metadata, autoload=True),
    'name_column': 'DescricaoTipoMovimento',
  },
  'tipo-vacina': {
    'table': Table('TIPO VACINA', metadata, autoload=True),
    'name_column': 'DescricãoTipoVacina',
  },
  'vacinas-aplicadas': {
    'table': Table('VACINA APLICADA', metadata, autoload=True),
    'name_column': 'DataVacinacao',
    'sort_column': 'DataVacinacao DESC',
  },
  'tipo-vacina-x-doenca': {
    'table': Table('TIPO VACINA x DOENCA', metadata, autoload=True),
    'name_column': None,
  },
  'unidades': {
    'table': Table('UNIDADE', metadata, autoload=True),
    'name_column': 'NomeUnidade',
  },
  'vacinas-planejadas': {
    'table': Table('VACINA PLANEJADA', metadata, autoload=True),
    'name_column': 'DataVacinacao',
    'sort_column': 'DataVacinacao DESC',
  },
  'atendimentos': {
    'table': Table('ATENDIMENTO', metadata, autoload=True),
    'name_column': 'Historico',
    'sort_column': 'DataAtendimento DESC',
  },
  'pacientes': {
    'table': Table('PACIENTE', metadata, autoload=True),
    'name_column': 'NomePaciente',
    'sort_column': 'NomePaciente',
  },
}
tablenames = {}
keys_pointing_at = {}
for name, data in tables.items():
    tablenames[data['table']] = name

    try:
        data['primary_key'] = data['table'].primary_key.columns.keys()[0]
    except IndexError:
        data['primary_key'] = None

    data['foreign_keys'] = {}
    for k in data['table'].foreign_keys:
        data['foreign_keys'][k.parent.name] = {
            'table': k.column.table,
            'column': k.column.name
        }

        kpat = keys_pointing_at.get(k.column.table, {})
        kpat[k.parent.table] = k.parent
        keys_pointing_at[k.column.table] = kpat

@app.template_filter('fk2name')
@memoize
def fk2name(id, table, column):
    tablecolumn = getattr(table.c, column)
    record = table.select(tablecolumn == int(id)) \
                  .execute() \
                  .first()
    return record2name(record, table) or id

@app.template_filter('record2id')
def record2id(record, table):
    primary_key = tables[tablenames[table]]['primary_key']
    return getattr(record, primary_key, None)

@app.template_filter('record2name')
def record2name(record, table):
    namecolumn = tables[tablenames[table]]['name_column']
    return getattr(record, namecolumn, None)

@app.template_filter('select')
@memoize
def select(table, where=None):
    tabledata = tables[tablenames[table]]

    query = table.select(where)
    if 'sort_column' in tabledata:
        query = query.order_by(tabledata['sort_column'])

    return tuple(query.execute())

@app.template_filter('get_from')
def get_from(id, table):
    primary_key = tables[tablenames[table]]['primary_key']
    return table.select(getattr(table.c, primary_key) == id).execute().first()

@app.template_filter('add_query_params')
def add_query_params(url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)

# jinja2 globals
@app.context_processor
def jinja2globals():
    return {
        'tables': tables,
        'tablenames': tablenames,
        'keys_pointing_at': keys_pointing_at,
    }

@app.route('/favicon.ico')
def nothing():
    return ''

@app.route('/<table_name>/', methods=['GET'])
def entities(table_name):
    tabledata = tables[table_name]
    table = tabledata['table']
    offset = int(request.args.get('from', 0))
    limit = int(request.args.get('show', 20))

    query = table.select()
    if 'sort_column' in tabledata:
        query = query.order_by(tabledata['sort_column'])

    r = query.offset(offset).limit(limit).execute().fetchall()
    return render_template('entities.html',
                           limit=limit,
                           offset=offset,
                           columns=table.columns,
                           rows=r,
                           table=table,
                           table_name=table_name,
                           primary_key=tabledata['primary_key'],
                           foreign_keys=tabledata['foreign_keys'])

@app.route('/<table_name>/<id>/', methods=['POST', 'GET'])
def post(table_name, id):
    tabledata = tables[table_name]
    table = tabledata['table']

    if request.method == 'GET':
        o = table.select(getattr(table.c, tabledata['primary_key']) == int(id)).execute().first()
        return render_template('entity.html',
                               columns=table.columns,
                               data=o,
                               table=table,
                               table_name=table_name,
                               primary_key=tabledata['primary_key'],
                               foreign_keys=tabledata['foreign_keys'])

    elif request.method == 'POST':
        update_data = {}
        for k, value in request.form.items():
            type = getattr(table.c, k).type.python_type
            if type is datetime.date:
                type = lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date()
            elif type is str:
                type = unicode

            update_data[k] = type(value)

        from pprint import pprint as pp
        pp(update_data)

        table.update() \
             .where(getattr(table.c, tabledata['primary_key']) == int(id)) \
             .values(update_data) \
             .execute()

        return redirect(request.url)

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
