import argparse, time

# Parsing arguments
parser = argparse.ArgumentParser(description='Boh')

start = time.time()

parser.add_argument('file',
                    metavar='file',
                    type=str,
                    nargs='?',
                    help='file name',
                    default='file.pcapng')
parser.add_argument('-vars',
                    dest='vars',
                    metavar='vars',
                    type=str,
                    nargs='+',
                    action='store',
                    help='vars')
args = parser.parse_args()

print(args.file, args.vars)
if type(args.vars) is not None:
    print(len(args.vars))

print("Time:", time.time() - start)
