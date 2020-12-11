#!/usr/bin/python

import random, sys
from argparse import ArgumentParser

class shuf:
    def __init__(self, args):
        self.input = []
        if (args.echo == '' and args.range == '0-0' and
            (args.file == '' or args.file[0] ==  '-')):
            self.input = sys.stdin.readlines()
        elif args.echo != '':
            for s in args.echo:
                self.input.append(s + "\n")
        elif args.range != '0-0':
            args.range = args.range.split('-')
            hi, lo = int(args.range[1]), int(args.range[0])
            self.input = [str(x) + '\n' for x in range(lo, hi + 1)]
        else:
        	try:
	            f = open(args.file[0], 'r')
	            self.input = f.readlines()
	            f.close()
	        except FileNotFoundError:
	        	sys.stdout.write("FILE NOT FOUND. PROGRAM TERMINATED.\n")
	        	return
        args.count = int(args.count)
        args.count = min(args.count, len(self.input)) if not args.repeat else args.count
        self.indices = []
        for i in range(len(self.input)):
            self.indices.append(i)
        random.shuffle(self.indices)
        self.count, self.repeat = args.count, args.repeat
        self.shuffle()

    def shuffle(self):
        if self.repeat:
            for i in range(self.count):
                sys.stdout.write(random.choice(self.input))
        else:
            for i in range(self.count):
                sys.stdout.write(self.input[self.indices[i]])

def main():
    parser = ArgumentParser(description="Shuffles some input.")
    parser.add_argument("-e", "--echo", action="store", dest="echo", nargs="*", default="",
                        help="Treat each command-line operand as an input line.")
    parser.add_argument("-i", "--input-range", action="store", dest="range", default="0-0",
                        help="Acts on unsigned decimal integer range lo...hi, one per line.")
    parser.add_argument("-n", "--head-count", action="store", dest="count", default=sys.maxsize,
                        help="Output at most count lines.")
    parser.add_argument("-r", "--repeat", action="store_true", dest="repeat",
                        help="Repeat output values, that is, select with replacement.")
    parser.add_argument("file", nargs="*", default="")
    args = parser.parse_args()

    try:
        generator = shuf(args)
    except IOError as err:
        parser.error('I/O error({0}): {1}'.format(err.errno, err.strerror))

if __name__ == "__main__":
    main()
