import os, sys
f = open("jsondump.json", "r")
o = open("output10k.json", "w")
i = 0
while True:
	line = f.readline()
	if not line:
		break
	i += 1
	if (i % 10000) == 1:
		o.write(line)
	if (i % 100000) == 1:
		sys.stdout.write(".")
		sys.stdout.flush()
o.close()
f.close()
