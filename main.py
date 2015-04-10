# -*- encoding: utf-8 -*-
#!/usr/bin/env python

import json
import os
import sys
import sqlite3

from flask import Flask, request, render_template
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

engine = create_engine(connstring, convert_unicode=True, echo=app.debug)
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
tablenames = {v['table']: k for k, v in tables.items()}

@app.template_filter('fk2name')
@memoize
def fk2name(id, table, column):
    tablecolumn = getattr(table.c, column)
    record = table.select(tablecolumn == id) \
                  .execute() \
                  .first()
    return row2name(record, table) or id

@app.template_filter('record2name')
def row2name(record, table):
    namecolumn = tables[tablenames[table]]['name_column']
    return getattr(record, namecolumn, None)

def list_foreign_key(table, column):
    query = table.select()
    if 'sort_column' in tables[tablenames[table]]:
        query = query.order_by(tables[tablenames[table]]['sort_column'])

    for record in query.execute():
        primary_key = table.primary_key.columns.keys()[0]
        id = getattr(record, primary_key)
        name = row2name(record, table)
        yield id, name

# jinja2 globals
@app.context_processor
def jinja2globals():
    return {
        'tables': tables,
        'tablenames': tablenames,
        'list_foreign_key': list_foreign_key,
    }

@app.route('/favicon.ico')
def nothing():
    return ''

@app.route('/<table_name>/<id>/', methods=['GET'])
@app.route('/<table_name>/', methods=['GET'])
def get(table_name, id=None):
    table = tables[table_name]['table']
    offset = int(request.args.get('from', 0))
    limit = int(request.args.get('show', 20))

    try:
        pk = table.primary_key.columns.keys()[0]
    except IndexError:
        pk = None
    fk = {k.parent.name:  {
            'table': k.column.table,
            'column': k.column.name
    } for k in table.foreign_keys}

    if id:
        o = table.select(getattr(table.c, pk) == id).execute().first()
        return render_template('entity.html',
                               columns=table.columns,
                               data=o,
                               table=table,
                               table_name=table_name,
                               primary_key=pk,
                               foreign_keys=fk)
    else:
        query = table.select()
        if 'sort_column' in tables[table_name]:
            print '\n\n', tables[table_name]['sort_column'], '\n\n\n'
            query = query.order_by(tables[table_name]['sort_column'])

        r = query.offset(offset).limit(limit).execute().fetchall()
        return render_template('entities.html',
                               limit=limit,
                               offset=offset,
                               columns=table.columns,
                               rows=r,
                               table=table,
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
