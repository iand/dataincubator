# Reads the LibraryThing XML dump and creates a gdbm database for ISBN->Work lookup

import re
import gdbm
lookup = gdbm.open('thingisbn_lookup.db', 'c');

f = open("thingISBN.xml", "r")
for line in f:
  
  m = re.match('<work workcode="([^"]+)"><isbn>(.+)</isbn></work>', line)
  if m is not None:
    isbns = m.group(2).replace(' uncertain="true"', '').split("</isbn><isbn>")
    for isbn in isbns: 
      lookup[isbn] = str(m.group(1))
    
f.close()
