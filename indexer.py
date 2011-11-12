# -*- coding: utf-8 -*-

import csv
import psycopg2
import codecs
from settings import *

conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (PG_DBNAME, PG_USER, PG_HOST, PG_PASSW))
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

with open('listebiblio.csv', 'rb') as f:
   reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
   for r in reader:
      try:
         name    = r[0]
         phone   = r[1]
         address = r[2]

         # Insert libraries
         try:
            cur.execute("INSERT INTO libraries (name, phone, address) VALUES (%s, %s, %s) RETURNING id", (name, phone, address))
         except Exception, e:
            cur.execute("SELECT id FROM libraries WHERE name=%s", (name,))
         library_id = cur.fetchone()[0]
         print "Library: %s" % library_id
      except Exception, e:
         pass


with open('saint-albert.csv', 'rb') as f:
   reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
   i = 0
   for r in reader:
      try:
         author  = r[0]
         title   = r[1]
         isbn    = r[2]
         editor  = r[3]
         type    = r[4]
         subject = r[5]
         doctype = r[6]

         # Insert authors
         #try:
         #   cur.execute("INSERT INTO authors (author) VALUES (%s) RETURNING id", (author,))
         #except:
         #   cur.execute("SELECT id FROM authors WHERE author=%s", (author,))
         #author_id = cur.fetchone()[0]

         ## Insert editors
         #try:
         #   cur.execute("INSERT INTO editors (name) VALUES (%s) RETURNING id", (editor,))
         #except:
         #   cur.execute("SELECT id FROM editors WHERE name=%s", (editor,))
         #editor_id = cur.fetchone()[0]

         # TODO : DO NOT HARDCODE THIS !
         author_id = 1
         editor_id = 1
         library_id = 8

         # Insert editors
         try:
            cur.execute("INSERT INTO documents (isbn, editor_id, doctype, type, author_id, title, subject) \
                         VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                         (isbn, editor_id, doctype, type, author_id, title, subject))
         except:
            cur.execute("SELECT id FROM documents WHERE isbn=%s", (isbn,))
         document = cur.fetchone()[0]

         print document_id

         i += 1
         if i > 10:
            break

      except Exception, e:
         print e
         pass

cur.close()
conn.close()
