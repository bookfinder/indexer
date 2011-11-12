import csv

with open('saint-albert.csv', 'rb') as f:
   reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
   i = 0
   for row in reader:
      author  = row[0]
      title   = row[1]
      isbn    = row[2]
      editor  = row[3]
      type    = row[4]
      subject = row[5]
      type2   = row[6]
      print type, type2, subject
      i += 1
      if i > 10:
         break
