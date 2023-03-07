import psycopg2

from dotenv import dotenv_values

config = dotenv_values(".env")

async def createNewShotEntry(name, limits, reso, maxStability):
    name = '\'' + name + '\''
    cur = conn.cursor()
    query = """INSERT INTO public.shot (name, limits, reso, max_stability) VALUES (%s, %s, %s, %d)""" % (name, "ARRAY " + str(limits), "ARRAY " + str(reso), maxStability)
    cur.execute( query )
    conn.commit()

async def updateStabilitiesById(id, stabilities):
    cur = conn.cursor()
    query="""UPDATE public.shot SET stabilities = %s WHERE id = %d""" % ( 'ARRAY ' + str(stabilities), id )
    cur.execute( query )
    conn.commit()

async def fetchShotById(id):
    cur = conn.cursor()
    query="""SELECT limits, reso FROM public.shot WHERE id = %d""" % ( id )
    cur.execute( query )
    rows = cur.fetchall()
    return { "id": id, "limits": rows[0][0], "reso": rows[0][1] }

async def fetchStabilitiesById(id):
    cur = conn.cursor()
    query="""SELECT stabilities, max_stability FROM public.shot WHERE id = %d""" % ( id )
    cur.execute( query )
    rows = cur.fetchall()
    #print(rows[0][1])
    return { "id": id, "stabilities": rows[0][0], "max_stability": rows[0][1] }
    

# terminal command to start db
# psql -h localhost -p 5432 -U postgres -f db.sql

conn = psycopg2.connect(database = config["DB_NAME"], user = config["DB_USER"],
                        password = config["DB_PASS"], host = config["DB_HOST"], 
                        port = config["DB_PORT"])

print("Connection Successful to PostgreSQL")

#createNewShot('testName', [-9.6, 9.6, -5.4, 5.4], [1920, 1080], 500)



#updateStabilitiesById( 1, an array )