import psycopg2
import re

# Connect to an existing database
conn = psycopg2.connect("dbname=empoweru3 user=postgres password=instructor1a")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
myProgram = cur.execute("""
select path from wagtailcore_page
where title like %s;
""", ('Spring 2019', ))

program_page_id = cur.fetchone()
program_page_id = "%"+program_page_id[0]+"%"

myWeeks = cur.execute("""
select title, path p from wagtailcore_page
where path like %s and title not like %s
""", (program_page_id, "Spring 2019", ))

for result in cur.fetchmany(500):
    if re.search('Week.*', result[0]):
        print(result)

cur.close()
conn.close()
