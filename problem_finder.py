#!/usr/bin/python

import os
import re
import sys
#import numpy as np
from sets import Set

def init():
    """
    This function generally verifies that the program is called correctly.
    It verifies:
    * Proper number of arguments, and
    * That the date arguments can be split on "-" into three integers, and
    * That the start date occurs strictly before the end date.
    It does not verify:
    * That the commodity type given as the final argument makes sense.
    """

    # Make sure the program is being called correctly. If it isn't, print some
    # helpful information and exit.
    if len(sys.argv) is not 4:
        print "Usage: $" + sys.argv[0] + " word_list sample_exam output_file"
        sys.exit(-1)

    return {'word_list'  : sys.argv[1],
            'sample_exam': sys.argv[2],
            'output_file': sys.argv[3]}


def read_wordlist(filename):
    """
    Reads all the words from the wordlist into a set, and returns the set.
    """

    word_set = Set()

    if os.path.isfile(filename):
        with open(filename) as f:
            for line in f:
                # Split on whitespace
                word_set.union(line.split(' '))

    return word_set

def read_sample_exam(filename):
    """
    Reads the file into a string and returns that string.
    """
    if os.path.isfile(filename):
        with open(filename) as f:
            return f.read()

def parse_problems(sample_exam):
    """
    Segments the sample exam into a list of problems, and returns the list.

    A problem is a list of lines that starts on a
    ^[ ]*[0-9]+\. [A-Z].*$
    and ends on a newline just before the next occurrence of same,
    or the end of file.
    """

    # Let's start by seeing if we can print the beginning line of each problem
    #problem_pattern = r"^[ ]*[0-9]+\. [A-Z].*$(^.+$)+\n[ ]*[0-9]+\. [A-Z]"
    problem_pattern = r"^[ ]*[0-9]+\. [A-Z].*(\n.*)+?\n(?=^[ ]*[0-9]+\. [A-Z])"
    problem_regex   = re.compile(problem_pattern, re.MULTILINE)
    problems        = re.finditer(problem_regex, sample_exam)
    for problem_group in problems:
        print "Foo"
        print problem_group.group()
        print "Bar"
#    stop_pattern  = r"

#    for line in sample_exam_lines:
 #       problem_start = re.match(start_pattern, line)
  #      if problem_start:
   #         print problem_start.group()

def select(start, end, table):
    """
    Returns a list of prices corresponding to the given date range.
    This function also verifies that the given dates are within the bounds of
    the table.
    """

    # Make sure start and end dates are strictly on the table
    if start < (table[-1])[0]:
        print "Error: Start date before earliest datum."
        exit(-1)
    if end > (table[0])[0]:
        print "Error: End date after latest datum."
        exit(-1)

    # Grab the prices we're interested in
    selection = [x[1] for x in table if x[0] >= start and x[0] <= end]
    return selection

# Print the mean and variance of the price of a commodity over a given date
# range.
Parameters = init()
Words = read_wordlist(Parameters['word_list'])
Sample_Exam = read_sample_exam(Parameters['sample_exam'])
parse_problems(Sample_Exam)
"""
Selection = select(Parameters['start'], Parameters['end'], Table)

mean = np.mean(Selection)
variance = np.var(Selection)

print "%s %0.2f %0.2f" % (Parameters['ctype'], mean, variance)
"""
