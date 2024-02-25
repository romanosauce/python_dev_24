import sys
import cowsay
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('message', nargs='?')
parser.add_argument('-e', default=cowsay.Option.eyes, dest='eyes')
parser.add_argument('-f', default='default', dest='cowfile')
parser.add_argument('-T', default=cowsay.Option.tongue, dest='tongue')
parser.add_argument('-W', type=int, default=40, dest='width')
parser.add_argument('-n', action='store_true', dest='wrap')
parser.add_argument('-l', action='store_true', dest='list')

group = parser.add_mutually_exclusive_group()
group.add_argument('-b', action='store_true')
group.add_argument('-g', action='store_true')
group.add_argument('-p', action='store_true')
group.add_argument('-s', action='store_true')
group.add_argument('-t', action='store_true')
group.add_argument('-w', action='store_true')
group.add_argument('-y', action='store_true')


args = parser.parse_args()


for preset in 'bgpstwy':
    if getattr(args, preset):
        break
    else:
        preset = None

if args.list:
    print(*cowsay.list_cows(), sep=' ')
    sys.exit(0)

if not args.message:
    args.message = ' '.join(sys.stdin.read().split())
else:
    args.message = ' '.join(args.message.split())

if args.cowfile in cowsay.list_cows():
    print(cowsay.cowsay(args.message, cow=args.cowfile, preset=preset,
                        eyes=args.eyes, tongue=args.tongue, width=args.width))
else:
    with open(args.cowfile, 'r') as f:
        print(cowsay.cowsay(args.message, preset=preset, eyes=args.eyes,
                            tongue=args.tongue, width=args.width,
                            cowfile=cowsay.read_dot_cow(f)))
