# -*- coding: utf-8 -*-

import re

def validate_char_isbn9(isbn):
  return (re.match("[0-9]{9}", isbn) != None)

def validate_char_isbn10(isbn):
  return (re.match("[0-9]{9}[1-9|x|X]", isbn) != None)

def build_isbn10(isbn9):
  if not validate_char_isbn9(isbn9):
    print "ERROR (build_isbn10): The argument must contains only numbers"
    return
  if len(isbn9) > 9 :
    isbn9 = isbn9[0:9]
  elif len(isbn9) < 9 :
    print "ERROR (build_isbn10): The argument must contains at least 9 characters."
    return

  a = 0
  for i in range(0,9):
    c = isbn9[i:i+1]
    if c == "x" or c == "X" :
      c = 10
    a = a + ((10 - i) * int(c))
  
  mod = a % 11
  checksum = 11 - mod
  if checksum == 10 :
    checksum = "X"
  return str(isbn9) + str(checksum) 

def validate_isbn10(isbn10):
  if not validate_char_isbn10(isbn10):
    print "ERROR (validate_isbn10): The argument must contains only numbers"
    return
  if len(isbn10) > 10 :
    isbn10 = isbn10[0:10]
  elif len(isbn10) < 10 :
    print "ERROR (validate_isbn10): The argument must contains at least 10 characters."
    return

  return (build_isbn10(isbn10) == isbn10)
 
def build_ena_from_isbn10(isbn):
  ena = "978" + isbn[0:9]
  check = 0
  for i in range(0, 11, 2):
    check += int(ena[i:i+1])
  for i in range(1, 12, 2):
    check += int(ena[i:i+1]) * 3

  mod = check % 10;
  return ena + str(10 - mod)

def purge_isbn_field(isbn):
  test = re.search('^([0-9-]+x?)', isbn, flags=re.IGNORECASE).group(1)
  return re.sub('-', '', test)
