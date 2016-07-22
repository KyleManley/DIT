import time
import getopt

import common.readwrite as io


def mid_month(infile, outfile, format):
    dates = io.pull(infile, str)

    month_days = [[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],  # Not leap year
                  [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],  # Is leap year
                  ]

    out = []
    for date in dates:
        t = time.strptime(format, date)
        year = t.tm_year
        leap = leap_year(year)
        month = t.tm_month
        mid_day = month_days[leap][month-1] / 2
        hour = mid_day % 1 * 24

        outputdate = (year, month, day, hour, 0, 0, 0, 0, -1)

        out.append(time.strftime('%Y-%m-%d %H:%M', outputdate))

    io.push(out, outfile)

def leap_year(year):
    if (year%4 == 0):
        if (year%100 == 0):
            if (year%400 == 0):
                return True
            return False
        return True
    return False


def parse_args(args):
    def help():
        print 'replace_ge.py -i <input file> -o <output file> -f <format>'
        print 'Makes a string of the center day of the month. See time.strftime for format specification'

    infile = None
    outfile = None
    format = None

    options = ('i:o:t:v:',
                ['input', 'output', 'format'])
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
            format = val

    if (any(val is None for val in [infile, outfile, format])):
        help()
        sys.exit(2)

    return infile, outfile, format
# def doy(month, day, leap, month_days):
    # count = 0
    # for i in range(month-1):
        # count += month_days[leap][month-1]
    # count += day
    # return count


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = parse_args(sys.argv[1:])


mid_month(*args)