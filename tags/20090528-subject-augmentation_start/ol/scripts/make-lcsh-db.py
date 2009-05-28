# Reads the lcsh NTriples dump and creates a gdbm database for prefLabel->URI lookup

import re
import gdbm
lookup = gdbm.open('lcsh_lookup.db', 'c');

# labels-sorted.nt is a grep on ntriples dump for prefLabel that is then sorted (sort is not really needed)
f = open("labels-sorted.nt", "r")
for line in f:
  m = re.match('^<([^>]+)>\s+<[^>]+>\s+"([^"]+)"', line)
  if m is not None:
    lookup[m.group(2)] = m.group(1)
    
f.close()
