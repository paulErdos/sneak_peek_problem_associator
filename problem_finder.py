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
                # Remove newline
                line = line.rstrip()
                # Split on whitespace
                word_set = word_set.union(Set(line.split(' ')))

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

    # Python multiline regexing does not differentiate between the end of
    # a line and the end of the string. So add a sentinel value to the
    # end of the string.
    sample_exam = sample_exam + "#####"

    # Let's start by seeing if we can print the beginning line of each problem
    #problem_pattern = r"^[ ]*[0-9]+\. [A-Z].*$(^.+$)+\n[ ]*[0-9]+\. [A-Z]"
    problem_pattern =\
        r"^[ ]*[0-9]+\. [A-Z].*(\n.*)+?(?=\n^[ ]*[0-9]+\. [A-Z]|#####)"
    problem_regex   = re.compile(problem_pattern, re.MULTILINE)
    problem_matches = re.finditer(problem_regex, sample_exam)

    problems = []
    for problem_group in problem_matches:
#        print "foo"
        problems.append(problem_group.group(0))
 #       print "bar"
  #      print problems[-1]
  #      print "baz"

    return problems

def match_problems_with_wordlist(problems, words):
    word_pattern = r"\w+"
    word_regex   = re.compile(word_pattern, re.MULTILINE)

    first_line_pattern = r"^.*"
    first_line_regex = re.compile(first_line_pattern)

    for problem in problems:
        # Print a newline to separate, and print the first line of the problem
#        print "\n"
        first_line_matches = re.search(first_line_regex, problem)
#        print first_line_matches.group(0)

        # Form a set of all the words in the problem; convert to lowercase
        word_matches = re.findall(word_regex, problem)
        lowered_matches = list(map(lambda x: x.lower(), word_matches))
        lowered_set = Set(lowered_matches)

        # Print the size of the set of words in the problem
        size_problem = len(lowered_set)
#        print len(lowered_set)

        # Intersect the set of words in the problem with
        #           the set of words in the wordlist, and
        # print its size
        intersection = lowered_set.intersection(words)
        size_intersection = len(intersection)

        likeness = float(size_intersection)/float(size_problem)

        if 1.0 > likeness and likeness > 0.9:
#            if intersection == lowered_set:
 #               print "Intersection == lowered_set!"
            if os.path.isfile(sys.argv[3]):
                with open(sys.argv[3], "a+") as o:
                    o.write("Likeness: {}".format(likeness))
                    o.write("\n" + sys.argv[2])
                    o.write("\n" + problem)
                    o.write("\n")
            print 'Likeness: {}'.format(likeness)
            print sys.argv[2]
            print problem
            print ""
#        print "bar"
#        print len(intersection)

        # Sort the intersection alphabetically and print it
 #       print sorted(list(lowered_set.intersection(words)))

Parameters = init()
Words = read_wordlist(Parameters['word_list'])
Sample_Exam = read_sample_exam(Parameters['sample_exam'])
Problems = parse_problems(Sample_Exam)
match_problems_with_wordlist(Problems, Words)
"""
Selection = select(Parameters['start'], Parameters['end'], Table)

mean = np.mean(Selection)
variance = np.var(Selection)

print "%s %0.2f %0.2f" % (Parameters['ctype'], mean, variance)
"""
