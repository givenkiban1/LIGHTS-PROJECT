import sqlite3
database = "//home//pi//Documents//LIGHTS//db//sample.db"


sql_create_schedule_table = """CREATE TABLE IF NOT EXISTS Schedules (
                                EventID INTEGER PRIMARY KEY AUTOINCREMENT,
                                EventName text NOT NULL,
                                RingDuration INTEGER NOT NULL,
                                RingTime text NOT NULL,
                                EventDay text NOT NULL
                            );"""


def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file"""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Exception as e:
        print(e)
        
        


# create a database connection
conn = create_connection(database)

#conn = sqlite3.connect("/home/pi/Bell/sample.db")


if conn is not None:
    
    # create projects table
    create_table(conn, sql_create_schedule_table)
    # create tasks table
    #create_table(conn, sql_create_tasks_table)
    conn.commit()
    conn.close()
    print("done!")

else:

    print("Error! cannot create the database connection.")
