# Declare utf-8 encoding
# -*- coding: utf-8 -*-

import os
import pyparsing as pp
import time

start_time = time.time()

# Set working directory
dump = "20161216"
datadir = "/Users/donaldposthuma/Documents/Klanten/ExperienceData/NationaleNederlanden/Letsel/0.Data/echo_dumps/" + dump
os.chdir(datadir)


# Location of raw data
inputpath = 'rawdata/'

# Create folder to store output of the importcheck
outputpath = "importcheck/"
if not os.path.exists(outputpath):
    os.makedirs(outputpath)

# Create folder to store validated data
validatedpath = "validateddata/"
if not os.path.exists(validatedpath):
    os.makedirs(validatedpath)

# Declare delimiter, quoter, content and field later used to construct the parser
delimiter = ';'
quote = '"'
content = quote + pp.Word(pp.printables + ' -’€éß', excludeChars=';"') + quote
# content = quote + pp.Word(pp.printables + ' ', excludeChars=';"') + quote
emptycontent = quote + quote
field = content | emptycontent


for file in os.listdir(inputpath):
    filename = os.path.splitext(file)[0]
    print file
    inputfile = file
    outputfile = 'IO_error_' + filename + '.txt'
    log = 'Import Validation Log ' + dump + '.txt'

    logfile = open(outputpath + log, 'w')

    with open(inputpath+inputfile, 'rb') as csvfile:

            # Construct parser by combining field and delimiters based on number of delimeters in header
            # Add LineEnd at the end of the parser
            firstline = csvfile.readline()
            count_delimiters = firstline.count(delimiter)
            count_quotes_header = firstline.count(quote)

            rowparse = field
            for x in range (0,count_delimiters):
                rowparse = rowparse + delimiter + field

            rowparse = rowparse + pp.LineEnd()
            # Loop trough lines to check whether they comply with parser
            reader = csvfile.readlines()
            outfile = open(outputpath + outputfile, 'w')
            outfile.write(firstline)
            lines_in_file = 0
            errors_in_file = 0
            for idx, line in enumerate(reader):
                count_quotes_line = line.count(quote)
                lines_in_file = lines_in_file + 1

                if count_quotes_header == count_quotes_line:
                    pass
                else:
                    errors_in_file = errors_in_file + 1
                    errorstring = str(idx + 2) + ': ' + line
                    #errorstring = line
                    outfile.write(errorstring)
                # try:
                #     rowparse.parseString(line)
                # except:
                #     errors_in_file = errors_in_file+1
                #     errorstring =  str(idx+2) + ': ' + line
                #     outfile.write(errorstring)

            print filename+': lines = '+str(lines_in_file)+', errors = '+str(errors_in_file) + ' (' + str(round(100*errors_in_file/(lines_in_file+0.00001), 1))+ '%)'
            logfile.close()

            outfile.close()
            print 'runtime: ' + str(time.time()-start_time)
            #MIf no errors then move file to validated path and delete output file
            if errors_in_file == 0:
                os.remove(outputpath + outputfile)
                os.rename(inputpath+inputfile, validatedpath+inputfile)

