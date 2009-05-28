import json
import sys
try:
	f = open(sys.argv[1], "r")
except IndexError:
	sys.exit("Please supply a file name")
except IOError:
	sys.exit("Invalid file name")
unique = {}
keyparts = sys.argv[2].split(":")
while True:
	line = f.readline()
	if not line:
		break
	data = json.read(line)
	for keypart in keyparts:
		data = data[keypart]
	try:
		unique[data] = None
	except KeyError:
		pass
	except IndexError:
		sys.exit("Please supply an attribute name")
f.close()
for x in unique.keys():
	print x
