# -*- coding: utf-8 -*-

import csv
import psycopg2
import codecs
import utilities

from settings import *

from reader import UnicodeReader



def import_libraries(csv_filename, cur):
  with open(csv_filename, 'rb') as f:
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
  return

def import_documents(csv_filename, cur):
  
  with open(csv_filename, 'rb') as f:
    reader =  UnicodeReader(f, encoding='iso-8859-1')
    i = 0
    for r in reader:
      i += 1
      print i
      if i == 1:
        continue

      print "caliss"
      if i % 100 == 0:
        print "documednts : %s" % i
      

        
      author  = r[0]
      title   = r[1]
      isbn    = r[2]
      editor  = r[3]
      type    = r[4]
      subject = r[5]
      doctype = r[6]
      ena = ""
      
      print isbn
      if isbn == "":
        continue

      isbn = utilities.purge_isbn_field(isbn)
      print isbn

      # Insert authors
      try:
        cur.execute("INSERT INTO authors (author) VALUES (%s) RETURNING id", (author,))
      except Exception, e:
        # Already in the database ... we recover it with a "SELECT"
        cur.execute("SELECT id FROM authors WHERE author=%s", (author,))
      
      author_id = cur.fetchone()[0]
      
      # Insert editors
      try:
        cur.execute("INSERT INTO editors (name) VALUES (%s) RETURNING id", (editor,))
      except Exception, e:
        # Already in the database ... we recover it with a "SELECT"
        cur.execute("SELECT id FROM editors WHERE name=%s", (editor,))
      editor_id = cur.fetchone()[0]

      # TODO : DO NOT HARDCODE THIS !
      library_id = 8

      # Insert documents
      try:
        cur.execute("INSERT INTO documents (isbn, ena, editor_id, doctype, type, author_id, title, subject) \
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
          (isbn, ena, editor_id, doctype, type, author_id, title, subject))
      except Exception, e:
        #Already in the database ... we get the id matching the isbn
        cur.execute("SELECT id FROM documents WHERE isbn=%s", (isbn,))
      
      document = cur.fetchone()
      print document
      if document:
        document_id = document[0]

      #TODO : insert in libraries_documents


  return


conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (PG_DBNAME, PG_USER, PG_HOST, PG_PASSW))
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()


import_libraries('listebiblio.csv', cur)
import_documents('saint-albert.csv', cur) 



cur.close()
conn.close()