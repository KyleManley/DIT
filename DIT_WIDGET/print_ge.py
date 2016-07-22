#! /usr/bin/python

import sys
import getopt

import printfamily.prints as p
# import common.parseargs as pa


def print_ge(infile, outfile, num):
    """Print all values greater than or equal to a threshold."""
    p.print_conditional(infile, outfile, num, lambda x, y: x >= y)


def parse_args(args):
    def help():
        print 'print_ge.py -i <input file> -o <output file> -t <threshold>'
        print 'Prints values greater than or equal to threshold'


    infile = None
    outfile = None
    threshold = None

    options = ('i:o:t:',
               ['input', 'output', 'threshold'])
    readoptions = zip(['-'+c for c in options[0] if c != ':'],
                      ['--'+o for o in options[1]])

    try:
        (vals, extras) = getopt.getopt(args, *options)
    except getopt.GetoptError as e:
        print str(e)
        help()
        sys.exit(2)

    for (option, val) in vals:
        if (option in readoptions[0]):
            infile = val
        elif (option in readoptions[1]):
            outfile = val
        elif (option in readoptions[2]):
            threshold = int(val)

    if (any(val is None for val in [infile, outfile, threshold])):
        help()
        sys.exit(2)

    return infile, outfile, threshold
#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = parse_args(sys.argv[1:])
# infile = args[0]
# outfile = args[1]
# threshold = args[2][0]

print_ge(*args)
