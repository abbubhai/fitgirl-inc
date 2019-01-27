import psycopg2
import re
from datetime import date, timedelta

#new_start_date = input("New start date (yyyy/mm/dd): ").split('/')
new_start_date = ['2019', '11', '11']
program = 'Fall 2019'
new_start_date = date(int(new_start_date[0]), int(new_start_date[1]), int(new_start_date[2]))
one_week = timedelta(days=7)
one_day = timedelta(days=1)

# Connect to an existing database
conn = psycopg2.connect("dbname=empoweru3 user=postgres password=instructor1a")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
myProgram = cur.execute("""
select path from wagtailcore_page
where title like %s;
""", (program, ))

program_page_id = cur.fetchone()
program_page_id = "%"+program_page_id[0]+"%"

myWeeks = cur.execute("""
select title, id, path from wagtailcore_page
where path like %s and title not like %s
""", (program_page_id, program, ))

for result in cur.fetchmany(500):
    m = re.search(('Week.*'), result[0])
    if (m):
        week_name = m.group(0)
        week_id = result[1]
        week_path = result[2] + '%'
        print(week_path)
        myPhys = cur.execute("""
                select id from wagtailcore_page
                where path like %s;
                """, (week_path,))
        result = cur.fetchmany()
        print(result)

        myPhysDates = cur.execute("""
                select start_date, end_date
                from week_physicalpostpage
                where page_ptr_id = %s""", (result[0],))
        result = cur.fetchmany()

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
