# Declare utf-8 encoding
# -*- coding: utf-8 -*-

import os
import pyparsing as pp

# Set working directory
dump = "TEST IMPORT"
datadir = "/Users/donaldposthuma/Documents/Klanten/ExperienceData/NationaleNederlanden/Letsel/0.Data/echo_dumps/" + dump
os.chdir(datadir)


# Location of raw data
inputpath = 'rawdata/'

# Create folder to store output of the importcheck
outputpath = "importcheck/"
if not os.path.exists(outputpath):
    os.makedirs(outputpath)

# Declare delimiter, quoter, content and field later used to construct the parser
delimiter = ';'
quote = '"'
content = quote + pp.Word(pp.printables + ' ’', excludeChars=';"') + quote
emptycontent = quote + quote
field = content | emptycontent


for file in os.listdir(inputpath):
    filename = os.path.splitext(file)[0]
    inputfile = file
    outputfile = 'IO_error_' + filename + '.txt'

    with open(inputpath+inputfile, 'rb') as csvfile:

            # Construct parser by combining field and delimiters based on number of delimeters in header
            # Add LineEnd at the end of the parser
            firstline = csvfile.readline()
            count_delimiters = firstline.count(delimiter)

            rowparse = field
            for x in range (0,count_delimiters):
                rowparse = rowparse + delimiter + field

            rowparse = rowparse + pp.LineEnd()

            # Loop trough lines to check whether they comply with parser
            reader = csvfile.readlines()
            outfile = open(outputpath + outputfile, 'w')
            for idx, line in enumerate(reader):
                try:
                    rowparse.parseString(line)
                except:
                    print idx
                    errorstring =  str(idx+2) + ': ' + line
                    outfile.write(errorstring)

            outfile.close()

            # Delete output files which contain no errors
            if os.stat(outputpath+outputfile).st_size == 0:
                os.remove(outputpath+outputfile)

