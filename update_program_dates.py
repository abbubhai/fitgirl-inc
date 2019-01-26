import psycopg2
import re
from datetime import date, timedelta

today = date.today()
print(today)

one_week = timedelta(days=7)
one_day = timedelta(days=1)
print(today + one_week)
print(today + one_day)


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
select title, id, path from wagtailcore_page
where path like %s and title not like %s
""", (program_page_id, "Spring 2019", ))

for result in cur.fetchmany(500):
    m = re.search(('Week.*'), result[0])
    if (m):
        week_name = m.group(0)
        week_id = result[1]
        myWeek = cur.execute("""
        select start_date, end_date from week_weekpage
        where page_ptr_id = %s
        """, (week_id,))
        result = cur.fetchone()
        TIME_FORMAT = "%b %d"
        print("Start date for %s: %s" %(week_name, result[0].strftime(TIME_FORMAT)))
        print("End date for %s: %s" %(week_name, result[1].strftime(TIME_FORMAT)))

cur.close()
conn.close()
