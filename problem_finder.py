#!/usr/bin/python

import os
import re
import sys
#import numpy as np
from sets import Set
import textwrap

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

#    problems = []
#    for problem_group in problem_matches:
#        problems.append(problem_group.group(0))
#
    return [problem_group.group(0) for problem_group in problem_matches]
#    return problems

def match_problems_with_wordlist(problems, words):
    word_pattern = r"\w+"
    word_regex   = re.compile(word_pattern, re.MULTILINE)

    first_line_pattern = r"^.*"
    first_line_regex = re.compile(first_line_pattern)

    for problem in problems:
        # Form a set of all the words in the problem; convert to lowercase
        problem_word_matches = re.findall(word_regex, problem)
        lowered_matches = list(map(lambda x: x.lower(), problem_word_matches))
        lowered_problem_words = Set(lowered_matches)

        # Intersect the set of words in the problem with
        #           the set of words in the wordlist, and
        # print its size
        intersection = lowered_problem_words.intersection(words)
        intersection_string = ", ".join(list(intersection))
        intersection_string = textwrap.wrap(intersection_string, 80)
        intersection_string = "\n".join(intersection_string)

        # Define similarity as
        size_intersection = len(intersection)
        size_problem = len(lowered_problem_words)
        likeness = float(len(intersection))/float(len(lowered_problem_words))

        # For matches with likeness != 1, capitalize words in the problem that
        # are not in the wordset
#        for word in problem:
 #           if re.match(r"[a-zA-Z]+", word):
  #              word = word.upper()
#
#        problem_nonmatched_highlighted =\
#            [word.upper() for word in problem if re.match(r"[a-zA-Z]+", word)]

        # Get the words that are in the problem but are not in the wordlist
        difference = lowered_problem_words.difference(words)
        difference_string = ", ".join(list(difference))
        difference_string = textwrap.wrap(difference_string, 80)
        difference_string = "\n".join(difference_string)

        percentiles = map(lambda x: float(x)/10.0, range(0, 11, 1))
        for i in range(0, len(percentiles) - 1):
            if percentiles[i] <= likeness and likeness < percentiles[i + 1]:
                filename =\
                 "out" + re.sub(r"\.", "", str(percentiles[i + 1]))
                with open(filename, "a+") as o:
                    o.write("Likeness: {}\n".format(likeness))
                    o.write(sys.argv[2] + "\n")
                    o.write(problem + "\n")
                    o.write("Words from problem not in sneak peek:\n"
                             + difference_string + "\n\n")
                    o.write("Words from problem yes in sneak peek:\n"
                                 + intersection_string)
                    o.write("\n\n\n")
#        if 1.0 > likeness and likeness > 0.9:
#            if os.path.isfile(sys.argv[3]):
#                with open(sys.argv[3], "a+") as o:
#                    o.write("Likeness: {}".format(likeness))
#                    o.write("\n" + sys.argv[2])
#                    o.write("\n" + problem)
#                    o.write("\n")
#            print 'Likeness: {}'.format(likeness)
#            print sys.argv[2]
#            print problem
#            print difference
#            print intersection
#            print ""
#

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
