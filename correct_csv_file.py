import sys

class ParseException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def main(argv):
    STATE_NULL = 'null'
    STATE_READ_HEADERS = 'read headers'
    STATE_FIELD = 'field'
    STATE_EXPECTING_NEW_FIELD = 'expecting new field'
    STATE_OPENING_NEW_FIELD = 'opening new field'
    STATE_EXPECTING_LINE_END = 'expecting line end'

    state = STATE_NULL
    field_count = 0
    num_fields = 1
    headers_read = False
    current_field = ''

    character_count = 0
    line_count = 1

    csv_filename = argv[1]
    file = open(csv_filename, 'r', encoding='UTF-8')

    output_filename = argv[2]
    output_file = open(output_filename, 'w', encoding = 'UTF-8')

    while True:
        char = file.read(1)
        character_count = character_count + 1
        if not char:
            # print('end of file')
            break
        else:
            if state == STATE_NULL:
               #  print('reading new line')
                if char == '"':
                    if headers_read:
                        # read content of first field
                        field_count = 1
                        state = STATE_FIELD
                    else:
                        print('line should contain headers')
                        output_file.write(char)
                        state = STATE_READ_HEADERS
                else:
                    # error: line has to start with a quote
                    raise ParseException('new line has to start with a quote, line '  + str(line_count) + ', character = ' + str(character_count))

            elif state == STATE_READ_HEADERS:
                output_file.write(char)
                if char == ';':
                    num_fields = num_fields + 1
                if char == '\n':
                    print(num_fields, ' header fields read')
                    line_count = line_count + 1
                    character_count = 0
                    headers_read = True
                    state = STATE_NULL

            elif state == STATE_FIELD:
                if char == '"':
                    if field_count < num_fields:
                        state = STATE_EXPECTING_NEW_FIELD
                    elif field_count == num_fields:
                        state = STATE_EXPECTING_LINE_END
                    else:
                        # error: more fields found than expected
                        raise ParseException('additional field found. ('  + str(field_count) + ' of '  + str(num_fields) + ' read), line '  + str(line_count) + ', character = ' + str(character_count))
                else:
                    # replace unwanted characters
                    if char == '\n':
                        print('replacing line break at line ', line_count)
                        line_count = line_count + 1
                        character_count = 0
                        char = ' '
                    # add to content of field
                    current_field = current_field + char

            elif state == STATE_EXPECTING_NEW_FIELD:
                if char == ';':
                    state = STATE_OPENING_NEW_FIELD
                else:
                    # instead of closing the last field, the last quote was an 'internal quote' and will be removed from the current field
                    if char == '\n':
                        # remove unwanted character
                        char = ' '
                        line_count = line_count + 1
                        character_count = 0
                        state = STATE_FIELD # and stay in last field
                    elif char == '"':
                        current_field = current_field[0:len(current_field)-1] # do not use current character if it is also a quote
                        state = STATE_EXPECTING_NEW_FIELD # and try whether the next one is a semicolon
                    else:
                        current_field = current_field[0:(len(current_field)-1)] + char
                        state = STATE_FIELD # and stay in last field
                    # # error: expecting a new field, but the next character is NOT a semicolon
                    # raise ParseException('expecting semicolon (field '  + str(field_count) + ' of '  + str(num_fields) + ' read), line '  + str(line_count) + ', character ' + str(character_count))

            elif state == STATE_OPENING_NEW_FIELD:
                if char == '"':
                    # end content of last field
                    output_file.write('"' + current_field + '";')
                    current_field = ''
                    field_count = field_count + 1
                    state = STATE_FIELD
                else:
                    # instead of closing the last field, the last quote was an 'internal quote' followed by a semicolon and will be removed from the current field
                    if char == '\n':
                        # remove unwanted character
                        char = ' '
                        line_count = line_count + 1
                        character_count = 0
                    current_field = current_field[0:len(current_field)-2] + ';' + char
                    state = STATE_FIELD # and stay in last field
                    # # error: expecting content of new field, but it is not quoted
                    # raise ParseException('expecting quote (field ' + str(field_count) + ' of ' + str(num_fields) + ' read), line ' + str(line_count) + ', character ' + str(character_count))

            elif state == STATE_EXPECTING_LINE_END:
                if char == '\n':
                    # end content of field
                    output_file.write('"' + current_field + '"\n')
                    current_field = ''
                    field_count = field_count + 1
                    # print('end of line read')
                    line_count = line_count + 1
                    state = STATE_NULL
                elif char == '"':
                    # leave current_field alone and do not add quote
                    state = STATE_EXPECTING_LINE_END # and try whether the next one is a semicolon
                else:
                    # instead of closing the last field, the last quote was an 'internal quote' and will be left out from the current field
                    current_field = current_field + char
                    state = STATE_FIELD # and stay in last field
                    # # error: expecting line end because all expected fields were read
                    # raise ParseException('expecting line end, found "' + char + '" (field ' + str(field_count) + ' of ' + str(num_fields) + ' read), line ' + str(line_count) + ', character ' + str(character_count))

if __name__ == '__main__':
    try:
        main(sys.argv)
    except ParseException as pe:
        print('ParseException: ', pe.value)