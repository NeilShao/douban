# -*- coding:utf-8 -*-
import sqlite3
import MySQLdb

conn = sqlite3.connect('../app.db')

movie_db = MySQLdb.connect("localhost", "root", "950520", "douban",charset="utf8")
cursor_movie = movie_db.cursor()

mysql = 'select id,title,comment from movie'
cursor_movie.execute(mysql)
movies = cursor_movie.fetchall()
for movie in movies:
    movie_name = movie[1].split(' ')[0]
    comments = movie[2].split('\n')
    comments = [comment for comment in comments if not comment.strip(' ') == '']

    for comment in comments:
        sqlite = "INSERT INTO Comment (movie_id,movie_name,body)  \
                 VALUES ('%s','%s','%s');" %(movie[0],movie_name,comment)
        print sqlite

        try:
            conn.execute(sqlite)
            conn.commit()
        except:
            conn.rollback()
    print str(movie[0]) + ' done'
conn.close()

'''

conn.execute("DELETE from Comment where ID>13;")
conn.commit()
cursor = conn.execute("select * from Comment;")
for row in cursor:
   for c in row:
       print c

   print '\n'
'''


