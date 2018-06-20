from pyexcel_xls import save_data
from py_core import logger
import getpass, psycopg2

def create_connection(dbname, user, password, host):
    # Connect to the source DB and create a cursor.
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        source_cur = conn.cursor()
    except (psycopg2.OperationalError) as e:
        logger.log("Error: " + str(e))
        sys.exit(2)
    except:
        logger.log("Unhandled exception:\n" + str(sys.exc_info()))
        sys.exit(2)
    return conn

def input_stuff(message, default):
    # Used to make data input and defaults generic
    data = input(message)
    if len(data) is 0:
        data = default
        print(data)
    return data


#Request needed info from command line.
source_host = input_stuff(
        "Source database host address (default is localhost):"
        ,"localhost")
logger.log("Source host name %s" % source_host, 0)

dbname = input_stuff(
        "Database name (Name of database on host):"
        ,"pyjunk")
logger.log("Database name %s" % dbname, 0)

user = input_stuff(
        "Database role (username - leave blank if same as your current user):"
        ,getpass.getuser())
logger.log("Username %s" % user, 0)

#Obviously, don't log the role password in the log
password = input("Role password:")


#Create the DB connection and cursor.
source_conn = create_connection(dbname, user, password, source_host)
source_cur = source_conn.cursor()

try:
    SQL = 'select * from myusers;'
    # If the name is an instance number, that must be converted into an int to
    # get the SQL command to view the text as a role name.
    source_cur.execute(SQL)
    data = source_cur.fetchall()
except (psycopg2.ProgrammingError) as e:
    logger.log("Warning: " + str(e))
except (psycopg2.InternalError) as e:
    logger.log("Error: " + str(e))
except:
    logger.log("Unhandled exception\n%s" % sys.exc_info())
    sys.exit(2)

print(data)
row = []

for item in data:
    print(item)
    print(item[0])
    row.append(item[0])

print(row)


data = {}
print(data)
data.update({"Sheet 1":[row, row]})
save_data("mytmp.xls",data)
