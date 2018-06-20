from pyexcel_xls import save_data
from py_core import logger
import getpass, psycopg2, sys


# I want to...
# 1. Connect to a DB to get a list of DBs
# 2. Disconnect from that DB
# 3. Connect to each DB in the list
# 4. Run the view for the DB
# 5. Save that data to an XLS
# 6. Disconnect from the DB


def get_DB_list(dbname, user, password, host):
    # Connect to the source DB and create a cursor.
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cur = conn.cursor()
        SQL = "select datname from pg_catalog.pg_database;"
        cur.execute(SQL)
        data = cur.fetchall()
        cur.close()
        conn.close()
    except (psycopg2.OperationalError) as e:
        logger.log("Error: " + str(e), 0)
    except:
        logger.log(str(sys.exc_info()), 0)
    return data

def create_connection(dbname, user, password, host):
    # Connect to the source DB and create a cursor.
    try:
        logger.log("Connecting to " + dbname)
        conn = psycopg2.connect(dbname=str(dbname), user=user, password=password, host=host)
        cur = conn.cursor()

        SQL = '''select "column_name" from information_schema.columns where table_name = 'state_of_channel_activity';'''
        cur.execute(SQL)
        activity_headers = cur.fetchall()

        SQL = 'select * from state_of_channel_activity;'
        cur.execute(SQL)
        activity = cur.fetchall()
        #Prepend the headers to the top of the list
        activity.insert(0, activity_headers)
        activity_prep = {}
        activity_prep.update({"Sheet 1":activity})
        save_data("exports/" + dbname + "_activity.xls", activity_prep)

        SQL = '''select "column_name" from information_schema.columns where table_name = 'state_of_channel_campaign';'''
        cur.execute(SQL)
        campaign_headers = cur.fetchall()

        SQL = 'select * from state_of_channel_campaign;'
        cur.execute(SQL)
        campaign = cur.fetchall()
        #logger.log(campaign);
        campaign.insert(0, campaign_headers)
        campaign_prep = {}
        campaign_prep.update({"Sheet 1":campaign})
        save_data("exports/" + dbname + "_campaign.xls", campaign_prep)
	
        cur.close()
        conn.close()

    except (psycopg2.OperationalError) as e:
        logger.log("Error: " + str(e), 0)
    except:
        logger.log(str(sys.exc_info()), 0)


def input_stuff(message, default):
    # Used to make data input and defaults generic
    data = input(message)
    if len(data) is 0:
        data = default
        print(data)
    return data



try:
    #Request needed info from command line.
    host = input_stuff(
            "Source database host address (default is localhost):"
            ,"localhost")
    logger.log("Source host name %s" % host, 0)

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
    databases = get_DB_list(dbname, user, password, host)

    for database in databases:
        if database[0] not in ('postgres', 'template0', 'template1'):
            create_connection(database[0], user, password, host)
        else:
            continue

except (psycopg2.ProgrammingError) as e:
    logger.log("Warning: " + str(e), 0)
except (psycopg2.InternalError) as e:
    logger.log("Error: " + str(e), 0)
except:
    logger.log(sys.exc_info(), 0)
