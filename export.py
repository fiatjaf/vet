# -*- encoding: utf-8 -*-

import StringIO
import datetime
import subprocess
import csv
import sqlite3

db = 'Paciente.mdb'

conn = sqlite3.connect('Paciente.db')
c = conn.cursor()

with open('Paciente.schema.sql') as f:
    schema = f.read()

for statement in schema.split('\n\n'):
    try:
        c.execute(statement)
    except Exception, e:
        print statement
        raise(e)

table_names = subprocess.Popen(["mdb-tables", "-1", db], stdout=subprocess.PIPE).communicate()[0]
tables = table_names.splitlines()
for table in tables:
    if table != '':
        data = subprocess.Popen(["mdb-export", db, table],
                                stdout=subprocess.PIPE).communicate()[0]
        filelike = StringIO.StringIO(data)
        rows = csv.reader(filelike, delimiter=',', quotechar='"')

        table = table.replace('Ç', 'C')

        cols = rows.next()
        for i, col in enumerate(cols):
            col = col.decode('utf-8').replace(u'ç', 'c').encode('utf-8')
            cols[i] = col

        for row in rows:
            vals = []
            for val in row:
                val = val.strip(' "')
                val = val.replace("'", "''")
                if len(val.split(' ')) == 2:
                    try:
                        val = datetime.datetime.strptime(val.split(' ')[0], '%m/%d/%y').isoformat().replace('T', ' ')
                    except ValueError, e:
                        pass
                val = unicode(val, 'utf-8')
                val = 'NULL' if not val else val if val.isdigit() else "'" + val + "'"
                vals.append(val) 

            try:
                vals = u", ".join(vals).encode('utf-8')
                sql = "INSERT INTO '{table}' ({cols}) VALUES ({vals})".format(
                    table=table,
                    cols=', '.join(cols),
                    vals=vals,
                )
                c.execute(sql)
            except sqlite3.OperationalError, e:
                print sql
                print e
                raise sqlite3.OperationalError

conn.commit()
