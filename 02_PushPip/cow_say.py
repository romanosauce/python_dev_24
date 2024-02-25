import cowsay
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('message', nargs='?', default='')

args = parser.parse_args()
print(cowsay.cowsay(args.message))
