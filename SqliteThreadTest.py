import os
import sys
import sqlite3

import threading
from datetime import datetime
from random import randint


def insertor(instance, dbname, lock):
    with sqlite3.connect(dbname) as connection:
        print('instance {0} connected to {1}'.format(instance, dbname))
        start = datetime.now()
        inserts = 0
        conflicts = 0
        retry_count = 0
        upper = 256 ** 3
        retry = False
        while inserts < insert_limit:
            if not retry:
                sql = 'insert into registration select \"{0}\",\"REG\",\"{1}\"'.format(
                    '{:06X}'.format(randint(1, upper)),
                    str(datetime.now()))
            try:
                #print('{0} sql= {1}'.format(instance,sql))
                connection.execute(sql)
                inserts += 1
                retry = False
            except sqlite3.OperationalError as ex:
                retry = True
                print('{0} operror {1}'.format(instance, ex))

                retry_count += 1
            except sqlite3.IntegrityError:
                conflicts += 1
    try:
        print(
            'Inserted {0} rows in {1} with {2} conflicts and {3} retries'.format(int(insert_limit),
                                                                                 datetime.now() - start, conflicts,
                                                                                 retry_count))
    except NameError:
        print('False start')


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
        conn.execute('vacuum;')

        lock = threading.Lock

        t1 = threading.Thread(target=insertor, args=('1', db_filename, lock))
        t2 = threading.Thread(target=insertor, args=('2', db_filename, lock))

        t1.start()
        t2.start()

        print('Thread launcher finished')
        t1.join()
        t2.join()
        print('All threads complete')

        analysis_sql = 'select strftime(\'%s\',created), count(*) from registration group by strftime(\'%s\', created);'
        cursor = conn.cursor()
        cursor.execute(analysis_sql)

        time_base = -1
        print('time,rows')
        for row in cursor.fetchall():
            if time_base == -1:
                time_base = int(row[0])

            print('{0},{1}'.format(int(row[0]) - time_base, row[1]))
