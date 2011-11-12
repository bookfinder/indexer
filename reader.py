import csv, codecs, cStringIO, pickle
class UnicodeReader:
   """
   A CSV reader which will iterate over lines in the CSV file "f",
   which is encoded in the given encoding.
   """

   def __init__(self, f, dialect=csv.excel, encoding="utf-8", reader='csv', **kwds):
       if reader == 'excel':
           self.reader = ExcelReader(f)
           self.reader_type = 'excel'
       else:
           self.reader_type = 'csv'

           input_file = f
           input_file.seek(0)
           dialect.delimiter = ','
           f = UnicodeReader.UTF8Recoder(input_file, encoding)
           comma_reader = csv.reader(f, dialect=dialect, **kwds)
           comma_len = len(comma_reader.next())

           input_file.seek(0)
           f = UnicodeReader.UTF8Recoder(input_file, encoding)
           dialect.delimiter = ';'
           semicolon_reader = csv.reader(f, dialect=dialect, **kwds)
           semicolon_len = len(semicolon_reader.next())

           input_file.seek(0)
           f = UnicodeReader.UTF8Recoder(input_file, encoding)
           if comma_len >= semicolon_len:
               dialect.delimiter = ','
               self.reader = csv.reader(f, dialect=dialect, **kwds)
           else:
               dialect.delimiter = ';'
               self.reader = csv.reader(f, dialect=dialect, **kwds)

   def next(self):
       try:
           row = self.reader.next()
       except StopIteration:
           raise StopIteration

       if self.reader_type == 'csv':
           return [unicode(s, "utf-8") for s in row]
       else:
           return row

   def __iter__(self):
       return self

   class UTF8Recoder:
       """
       Iterator that reads an encoded stream and reencodes the input to UTF-8
       """
       def __init__(self, f, encoding):
           self.reader = codecs.getreader(encoding)(f)

       def __iter__(self):
           return self

       def next(self):
           return self.reader.next().encode("utf-8")
