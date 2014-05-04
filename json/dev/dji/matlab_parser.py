#! /usr/bin/python
import numbers
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def process(infile, outfile):
	data = open(infile, 'r')
	output = open(outfile, 'w')
	result = ""
	for line in data:
		line = str(line).strip()
		print line + "|"
		if (is_number(line)):
			#print line
			#raw_input()
			result = result + line + " "
	output.write(result+"\n")
	data.close()
	output.close()


process('matlab2.txt', 'matlab2_processed.txt')