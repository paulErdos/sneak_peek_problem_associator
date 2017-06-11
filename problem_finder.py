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
        print "Usage: $"\
                + sys.argv[0]\
                + " word_list sample_exam sample_solutions"
        sys.exit(-1)

    return {'word_list'  : sys.argv[1],
            'sample_exam': sys.argv[2],
            'sample_solutions': sys.argv[3]}


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

def read_sample(filename):
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
    # So this means
    # Match the beginning of a line,
    # Then 0 or more spaces,
    # Then 1 or more numbers,
    # Then a dot,
    # Then a space,
    # Then a capital alpha character,
    # Then any number of any type of character aside from a newline,
    # Then one or more, but as few as possible, of:
    #     Newline, followed by 0 or more non-newlines,
    # But only match the above if the following lookahead assertion holds:
    # Only match above if the above is followed by
    # Either: 
    # 1. A newline,
    #    Then the beginning of a line,
    #    Then zero or more spaces,
    #    Then one or more digits,
    #    Then a dot,
    #    Then a space,
    #    Then one capital alpha character.
    # Or:
    # 2. Our end-of-file marker.
    problem_pattern =\
        r"^[ ]*[0-9]+\. [A-Z].*(\n.*)+?(?=\n^[ ]*[0-9]+\. [A-Z]|#####)"
    problem_regex   = re.compile(problem_pattern, re.MULTILINE)
    problem_matches = re.finditer(problem_regex, sample_exam)

#    print("number of problems: {}".format(len([problem_group.group(0) for problem_group in problem_matches])))

    return [problem_group.group(0) for problem_group in problem_matches]

def parse_solutions(sample_solutions):
    """
    Segments the solution file into a list of problems and returns that list.
    """

    # Python multiline regexing does not differentiate between the end of
    # a line and the end of the string. So add a sentinel value to the
    # end of the string.
    sample_solutions = sample_solutions + "#####"

    # Solutions start with a line that starts with
    # The beginning of a line,
    # Then
    # Either:
    # 1. "Question",
    #    Then any number of non-newlines.
    # Or:
    # 2. Any number of spaces,
    #    Then one or more digits,
    #    Then a dot,
    #    Then any number of non-newlines.
    # Then one or more, but as few as possible of:
    #     Newline, followed by any number of non-newlines,
    # But match the above only if followed by:
    # A newline,
    # Then a beginning of a line,
    # Then
    # Either:
    # 1. Either:
    #    1. "Question",
    #        Then any number of non-newlines.
    #    Or:
    #    2. Any number of spaces,
    #       Then one or more digits,
    #       Then a dot,
    #       Then any number of non-newlines.
    # Or:
    # 2: Our end-of-file marker.
    solution_pattern =\
          r"^((Question.*)|([ ]*[0-9]+\..*))"\
        + r"(\n.*)+?(?=\n^(((Question.*)|([ ]*[0-9]+\..*)))|#####)"
    solution_regex   = re.compile(solution_pattern, re.MULTILINE)
    solution_matches = re.finditer(solution_regex, sample_solutions)

#    print("number of solutions: {}".format(len([solution_group.group(0) for solution_group in solution_matches])))

    return [solution_group.group(0) for solution_group in solution_matches]

def match_problems_with_wordlist(problems, solutions, words):
    word_pattern = r"\w+"
    word_regex   = re.compile(word_pattern, re.MULTILINE)

    first_line_pattern = r"^.*"
    first_line_regex = re.compile(first_line_pattern)

    # Sanity check
    if len(problems) != len(solutions):
        print("Error! Unequal numbers of problems and solutions!")
        exit()

#    for problem in problems:
    for problem, solution in zip(problems, solutions):
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

        # Get the words that are in the problem but are not in the wordlist
        difference = lowered_problem_words.difference(words)
        difference_string = ", ".join(list(difference))
        difference_string = textwrap.wrap(difference_string, 80)
        difference_string = "\n".join(difference_string)

        percentiles = map(lambda x: float(x)/10.0, range(0, 12, 1))
        for i in range(0, len(percentiles) - 1):
            if percentiles[i] <= likeness and likeness < percentiles[i + 1]:
                problems_filename =\
                 "problems" + re.sub(r"\.", "", str(percentiles[i]))
                with open(problems_filename, "a+") as o:
                    o.write("Likeness: {}\n".format(likeness))
                    o.write(sys.argv[2] + "\n")
                    o.write(problem + "\n")
                    o.write("Words from problem not in sneak peek:\n"
                             + difference_string + "\n\n")
                    o.write("Words from problem yes in sneak peek:\n"
                                 + intersection_string)
                    o.write("\n\n\n")
                solutions_filename =\
                 "solutions" + re.sub(r"\.", "", str(percentiles[i]))
                with open(solutions_filename, "a+") as o:
                    o.write(solution + "\n\n")

Parameters = init()
Words = read_wordlist(Parameters['word_list'])
Sample_Exam = read_sample(Parameters['sample_exam'])
Sample_Solutions = read_sample(Parameters['sample_solutions'])
Problems = parse_problems(Sample_Exam)
Solutions = parse_solutions(Sample_Solutions)
match_problems_with_wordlist(Problems, Solutions, Words)
