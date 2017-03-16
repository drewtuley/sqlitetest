import sqlite3
import os
import sys
from datetime import datetime
from random import randint

if __name__ == "__main__":
    insert_limit = 1e5
    if len(sys.argv) > 1:
        insert_limit = int(sys.argv[1])

    db_filename = "data/sqlite_test.db"
    schema_filename = "data/sqlite3_test.sql"

    db_exists = os.path.exists(db_filename)

    with sqlite3.connect(db_filename) as conn:
        if not db_exists:
            print('Creating test database')
            with open(schema_filename) as f:
                schema = f.read()
            conn.executescript(schema)

        conn.execute('DELETE FROM registration;')

        start = datetime.now()
        inserts = 0
        conflicts = 0
        upper = 256 ** 3
        while inserts < insert_limit:
            sql = 'insert into registration select \"{0}\",\"REG\",\"{1}\"'.format('{:06X}'.format(randint(1, upper)),
                                                                                   str(datetime.now()))
            try:
                # print(sql)
                conn.execute(sql)
                inserts += 1
            except sqlite3.IntegrityError:
                conflicts += 1
    try:
        print('Inserted {0} rows in {1} with {2} conflicts'.format(int(insert_limit), datetime.now() - start, conflicts))
        
        analysis_sql = 'select strftime(\'%s\',created), count(*) from registration group by strftime(\'%s\', created);'
        cursor = conn.cursor()
        cursor.execute(analysis_sql)
    
        time_base = -1
        print('time,rows')
        for row in cursor.fetchall():
            if time_base == -1:
                time_base = int(row[0])
            
            print('{0},{1}'.format(int(row[0])-time_base, row[1]))

    except NameError:
        print('False start')
