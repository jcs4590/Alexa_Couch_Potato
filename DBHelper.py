import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse("postgres://sqbzklbkfhnxko:lHJ-WM97Vwt3ym9sM4Nvcs9BOH@ec2-107-22-184-127.compute-1.amazonaws.com:5432/d861dkoeg9qld0")

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

#
cur = conn.cursor()
#
#
# cur.callproc("AddProgram", [None, None, 3, 4, 5, 6, 5, "dddd",None, "sssaaaaa", 5, 1,6,4,7, 6, unicode("vgg"),33333])
# cur.close()
# conn.commit()
# conn.close()

# def insert_into

# cur.execute('SELECT * from GetPrograms()')
# ver = cur.fetchone()
# print ver[0]