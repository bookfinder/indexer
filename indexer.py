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
         print "CAISS"

         # Insert libraries
         try:
            cur.execute("INSERT INTO libraries (name, phone, address) VALUES (%s, %s, %s) RETURNING id", (name, phone, address))
         except Exception, e:
            print e
            cur.execute("SELECT id FROM librairies WHERE name=%s", (name,))
         library_id = cur.fetchone()[0]
         print "Library: %s" % library_id
      except:
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
         try:
            cur.execute("INSERT INTO authors (author) VALUES (%s) RETURNING id", (author,))
         except:
            cur.execute("SELECT id FROM authors WHERE author=%s", (author,))
         author_id = cur.fetchone()[0]

         # Insert editors
         try:
            cur.execute("INSERT INTO editors (name) VALUES (%s) RETURNING id", (editor,))
         except:
            cur.execute("SELECT id FROM editor WHERE name=%s", (editor,))
         editor_id = cur.fetchone()[0]

         print author_id

         i += 1
         if i > 10:
            break

      except:
         pass

cur.close()
conn.close()
