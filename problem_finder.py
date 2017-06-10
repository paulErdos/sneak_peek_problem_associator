#!/usr/bin/python

import os
import re
import sys
import datetime
import numpy as np

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
        print "Usage: $./compute.py word_list input_file output_file"
        sys.exit(-1)

    # Check that arguments are formatted properly
    try:
        start_year, start_month, start_day = sys.argv[1].split('-')
        end_year, end_month, end_day = sys.argv[2].split('-')

        start =\
            datetime.date(int(start_year), int(start_month), int(start_day))
        end =\
             datetime.date(int(end_year), int(end_month), int(end_day))
    except:
        print "Error: Cannot make sense of date arguments!\n"
        print "The arguments in question:"
        print "Argument 1: " + sys.argv[1]
        print "Argument 2: " + sys.argv[2]
        print "\nQuitting!"
        exit(-1)

    # Verify that the dates are in order
    if not start < end:
        print "Error: Start date does not precede end date.\n"
        exit(-1)

    return {'start': start, 'end': end, 'ctype': sys.argv[3]}


def read_and_format(ctype):
    """
    This function takes a commodity name and returns its price history.
    The file corresponding to the commodity type is opened, and its contents
    are read in. Date information is converted to the python datetime.date
    type, while prices are converted to floats. Tuples of dates and prices are
    then stored in a list, which is returned.
    """

    table = []

    months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }

    # Select the specified data file
    filename = 'data_' + ctype + '.csv'
    if os.path.isfile(filename):
        with open(filename) as f:
            # Discard the header line
            f.readline()
            for line in f:
                # Remove the trailing newline character
                line = line.rstrip()
                date, price = line.split(',')

                # Convert the first column into date objects
                month, day, year = date.split(' ')
                month = months[month]
                date = datetime.date(int(year), month, int(day))

                # Reformat the price
                price = float(price)

                # Store the data in the table
                table.append((date, price))
    return table

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
Table = read_and_format(Parameters['ctype'])
Selection = select(Parameters['start'], Parameters['end'], Table)

mean = np.mean(Selection)
variance = np.var(Selection)

print "%s %0.2f %0.2f" % (Parameters['ctype'], mean, variance)
