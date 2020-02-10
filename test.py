import sys, argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Fast Static File HTTP Server')

parser.add_argument('--host', default='localhost')
parser.add_argument('--port', default=8080, type=int)
parser.add_argument(
    '--version',
    action='version',
    version='%(prog)s ' + (Path(__file__).parent / 'VERSION.txt').read_text()
)

print(parser.parse_args(sys.argv[1:]))
