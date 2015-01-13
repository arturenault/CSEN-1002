#!/usr/bin/env python
'''
style_checker.py - Checks python file for proper style as outlined for 
ENGI E1006, an introductory scientific computing class at Columbia
University.

Author: Alexander Roth
UNI:    air2112
Date:   2014-12-21
'''
import re
import os
import sys
import time

WS_OP_REGEX = re.compile('\\s[-+/%<=>*!]+\\s')
NO_WS_OP_REGEX = re.compile('[^\\s][-+/%<=>*!]+[^\\s]')
EXCESS_WS_OP_REGEX = re.compile('[\\s]{2,}[-+/%<=>*!]+[\\s]')
ANY_STRING_REGEX = re.compile('.+\n')
NEWLINE_REGEX = re.compile('^\n$')
COMMENT_REGEX = re.compile('^.*#\\s.+')


class Checker(object):

    # TODO: Refactor into Object Oriented Code. Would probably clean up
    # a lot of this code.
    def __init__(self, line_list):
        self.line_list = line_list
        self.errs = Report()
        self.msgs = Report()

    def addMsg(self, msg):
        pass


class Report(object):

    def __init__(self):
        self.msgs = []


def main(filename):
    '''The main method, runs all the necessary checks on a given python file.'''
    file_list = readlines(filename)
    errs = []
    msgs = []
    detect_header(file_list, errs, msgs)
    detect_imports(file_list, errs, msgs)
    detect_whitespace(file_list, errs, msgs)
    detect_docstrings(file_list, errs, msgs)
    detect_line_length(file_list, errs, msgs)
    detect_comments(file_list, errs, msgs)
    detect_indentation(file_list, errs, msgs)
    print_errors(errs)
    print_std(msgs)


def readlines(filename):
    '''Opens given file and reads it into a buffer.'''
    open_file = open(filename, 'r')
    file_list = open_file.readlines()
    open_file.close()
    return file_list


def detect_header(file_list, errs, msgs):
    '''Searches for a header in the file.

    Headers for 1006 usually consist of 5 to 10 lines of single line comments
    at the top of the file.

    Example: ##################################################
             # Author: Alexander Roth
             # UNI:    air2112
             # Date:   2015-01-12
             # 
             # Description: This program does blah blah blah.
             ##################################################

    All files from students must contain headers or else TA must take off
    for no header.
    '''
    header_end = 0

    # TODO: I can probably clean this up with a regex. Maybe something like
    # '^#+\n$' for the borders and '^#\\s.*\n$' for the information.
    for i in range(len(file_list)):
        if '#' not in file_list[i]:
            header_end = i + 1
            break

    # Typically if there is no header, the user will just start with code.
    if header_end == 1:
        err_no_header(errs)
    else:
        msg_header_len(msgs, header_end)


def err_no_header(errs):
    '''Appends header error message to error message list.'''
    errs.append('HEADER: No header detected')


def msg_header_len(msgs, index):
    '''Appends header note to standard message list.'''
    msgs.append('HEADER: Header length: %d lines' % index)


def detect_imports(file_list, errs, msgs):
    '''Detects import statement and locates them within file.


    It is good style to have all import statements at the top of a file,
    even if the function isn't needed till much later in the program. This 
    global import resolves any import issues that could occur if the import
    statement begins in a function.
    '''
    for i in range(len(file_list)):
        if 'import' in file_list[i]:

            if get_identation_difference(file_list[i]):
                err_import_in_func(errs, i)
            else:
                msg_import_location(msgs, i)

            # Typically import statements happen at the top of the file, usually
            # within the first 25 lines.
            if i > 25:
                err_import_not_top(errs, i)


def get_indentation_difference(line):
    '''Takes the given line and checks for indentation size by examining line
    length.
    '''
    origin_line = len(line)
    clean_line = len(line.lstrip())
    indent_diff = origin_line - clean_line
    return indent_diff


def err_import_in_func(errs, index):
    '''Appends import error message to error message list.'''
    errs.append('IMPORT: Import statement possibly inside '
                'function on line %d' % (index + 1))


def msg_import_location(msgs, index):
    '''Appends import note with line number to the standard message list.'''
    msgs.append('IMPORT: Import statement found on line %d' % (index + 1))


def err_import_not_top(errs, index):
    '''Appends import error message about location of import statement to the
    error message list.
    '''
    errs.append('IMPORT: WARNING: Import statement found '
                'on line %d, not top of file.' % (index + 1))


def detect_whitespace(file_list, errs, msgs):
    '''Detects whitespace in between operators, inbetween logical blocks, and
    inbetween function definitions.
    '''
    detect_ws_in_op(file_list, errs, msgs)
    detect_nl_in_func(file_list, errs, msgs)
    detect_nls_between_func(file_list, errs, msgs)


def detect_ws_in_op(file_list, errs, msgs):
    '''Detects whitespace in between operators in a line of a function.

    In order to make code more readable, the programmer should include
    whitespace around binary operators.

    Example: Okay:  a + b 
             Okay:  test = tmp + foo + (2 * wow)
             Error: 1+2/5+temp
             Error: 1    +   2  /  3

    Note that it is ok to only leave whitespace on the side of parentheses and
    brackets that is not enclosing a varaible or constant.
    '''
    ws_total = 0
    no_ws_total = 0
    excess_ws_total = 0

    for i in range(len(file_list)):
        # Match whitespace based on different regular expressions
        ws_matches = re.findall(WS_OP_REGEX, file_list[i])
        no_ws_matches = re.findall(NO_WS_OP_REGEX, file_list[i])
        excess_ws_matches = re.findall(EXCESS_WS_OP_REGEX, file_list[i])

        if (len(no_ws_matches)):
            no_ws_total += len(no_ws_matches)

        if (len(excess_ws_matches)):
            excess_ws_total += len(excess_ws_matches)

        if (len(ws_matches)):
            ws_total += len(ws_matches)

    err_no_ws_op(errs, no_ws_total) if no_ws_total else False
    err_excess_ws_op(errs, excess_ws_total) if excess_ws_total else False
    msgs_good_ws_op(msgs, ws_total) if ws_total else False


def err_no_ws_op(errs, total):
    '''Appends whitespace error to error message list, contains the total number
    of whitepsace errors.
    '''
    errs.append('WHITESPACE: No whitespace found around '
                '%d operators in file' % (total))


def err_excess_ws_op(errs, total):
    '''Appends whitespace error to error message list, contains the total number
    of whitespace errors.
    '''
    errs.append('WHITESPACE: Excess whitespace found around '
                '%d operators in file' % (total))


def msgs_good_ws_op(msgs, total):
    '''Appends whitespace not to standard message list, contains total number of
    good whitespace found.
    '''
    msgs.append('WHITESPACE: Whitespace found around '
                '%d operators in file' % (total))


def detect_nl_in_func(file_list, errs, msgs):
    '''Detects newlines between logical block in function.

    Example: <code block 1 ...>

             <code block 2 ...>
           
    Note that there is one newline separating these logical blocks.
    '''

    # TODO: Have it operator function by function.
    count = 0
    for i in range(len(file_list)):
        if is_just_nl(file_list[i]) and in_between_block(file_list, i):
            count += 1

    if count == 0:
        err_no_nl_logic(errs)
    else:
        msg_nl_logic(msgs, count)


def is_just_nl(line):
    '''Matches newline to specified regular expression.'''
    return NEWLINE_REGEX.match(line)


def in_between_block(line_list, index):
    ''' Checks that the newline is found between two logical lines in a
    funciton.
    '''
    return (next_to_block(line_list[index - 1])
            and next_to_block(line_list[index + 1]))


def next_to_block(line):
    '''Matches a line containing any form of text that is not just a newline
    character.
    '''
    return ANY_STRING_REGEX.match(line)


def msg_nl_logic(msgs, total):
    '''Appends whitespace message with the total number of newlines found into
    the standard message list.
    '''
    msgs.append('WHITESPACE: Newlines possibly found '
                'inside %d function(s).' % (total))


def err_no_nl_logic(errs):
    '''Appends whitepsace error message that no newlines were found within
    function to the error message list.
    '''
    errs.append('WHITESPACE: No newlines found within functions')


def detect_nls_between_func(file_list, errs, msgs):
    '''Detects that there are 2 new lines inbetween function definitions.

    Example: def foo():
                 pass


             def bar():
                 pass

    PEP8 dictates that there must be 2 newlines between function definitions.
    '''
    # TODO: Detect multiple numbers of newlines between functions, not just 2.
    count = 0
    for i in range(len(file_list)):
        if (is_just_nl(file_list[i]) and
                is_just_nl(file_list[i - 1]) and
                is_func(file_list[i + 1])):
            count += 1

    if count == 0:
        err_no_nls_func(errs)
    else:
        msg_nls_func(msgs, count)


def is_func(line):
    '''Checks that the current line contains a function definition.'''
    return 'def' in line


def msg_nls_func(msgs, total):
    '''Appends whitespace message along with total number to the standard
    message list.
    '''
    msgs.append('WHITESPACE: Newlines possibly found '
                'between %d function(s)' % (total))


def err_no_nls_func(errs):
    '''Appends whitespace error to the error message list.'''
    errs.append('WHITESPACE: No newlines found between functions')


def detect_docstrings(file_list, errs, msgs):
    # TODO: Detect docstrings within functions.
    pass


def detect_line_length(file_list, errs, msgs):
    '''Checks that lines are under 79 characters in length.'''
    count = 0
    for line in file_list:
        if len(line) > 79:
            count += 1

    if count:
        err_over_79_chars(errs, count)
    else:
        msg_no_79_chars(msgs)


def err_over_79_chars(errs, total):
    '''Appends error message that line is too long to error list.'''
    errs.append('LINE LENGTH: %d line(s) over 79 chars in length' % (total))


def msg_no_79_chars(msgs):
    '''Appends line length message when lines are under 79 chars.'''
    msgs.append('LINE LENGTH: No lines over 79 chars in length')


def detect_comments(file_list, errs, msgs):
    '''Detects number of comments within the file.
    
    It is good style to sparingly include comments when the code cannot be
    easily described through the code itself.
    '''
    count = 0
    for line in file_list:
        if COMMENT_REGEX.match(line):
            count += 1

    if count:
        msg_comments(msgs, count)
    else:
        err_no_comments(errs)


def msg_comments(msgs, count):
    '''Appends the number of comments detect in program to standard message
    list.
    '''
    msgs.append('COMMENTS: %d comments detected in program' % count)


def err_no_comments(errs):
    '''Appends no comment error to error list.'''
    errs.append('COMMENTS: No comments detected in program')


def detect_indentation(file_list, errs, msgs):
    '''Detects indentation within the program. Checks that it is a multiple of
    4.

    It is good style to use an indentation size of 4, and only whitespace, not
    tabs.
    '''
    # TODO: Detect tabs mixed with whitespace.
    # TODO: Detect if an individual (unnested) indent is more than 4 chars.
    incorrect_count = 0
    for line in file_list:
        if not is_just_nl(line):
            indent_diff = get_indentation_difference(line)

            if indent_diff and indent_diff % 4:
                incorrect_count += 1

    if incorrect_count:
        err_incorrect_indentation(errs, incorrect_count)
    else:
        msg_correct_indentation(msgs)


def err_incorrect_indentation(errs, total):
    '''Appends indentation error to error list.'''
    errs.append('INDENTATION: Inconsistent indentation found '
                '%d times throughout file' % (total))


def msg_correct_indentation(msgs):
    '''Appends indentation note to the standard message list.'''
    msgs.append('INDENTATION: Consistent indentation throughout file')


def detect_variables(file_list, errs, msgs):
    # TODO: Detect intuitive variables
    pass


def detect_global_vars(file_list, errs, msgs):
    # TODO: Detect global varaibles
    pass


def print_errors(errs):
    '''Prints all errors within the error list.'''
    print_headers('ERRORS')

    if errs:
        print_message_list(errs)
    else:
        print 'No errors to report\n'


def print_std(msgs):
    '''Prints all messages in the standard message list.'''
    print_headers('STATS')

    if msgs:
        print_message_list(msgs)


def print_headers(section):
    '''Displays the section header.'''
    print section
    print '-' * 70


def print_message_list(msg_list):
    '''Prints the message list.'''
    for i in msg_list:
        print i
    print ''


def print_arguments(program):
    '''Prints arugments to show to the user if they don't know the commands.'''
    print 'python %s <file>' % program


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print_arguments(sys.argv[0])
