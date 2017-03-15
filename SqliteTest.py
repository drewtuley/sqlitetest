import sqlite3
import os
from datetime import datetime
from random import randint

if __name__ == "__main__":
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
        while inserts < 1e5:
            sql = 'insert into registration select \"{0}\",\"REG\",\"{1}\"'.format('{:06X}'.format(randint(1, upper)),
                                                                                   str(datetime.now()))
            try:
                # print(sql)
                conn.execute(sql)
                inserts += 1
            except sqlite3.IntegrityError:
                conflicts += 1
    try:
        print('Runtime = {0} with {1} conflicts'.format(datetime.now() - start, conflicts))
    except NameError:
        print('False start')
