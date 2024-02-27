import argparse
from argparse import RawTextHelpFormatter

# create the top-level parser
parser = argparse.ArgumentParser()
parser.add_argument('--azure', help='foo help')
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "a" command
parser_a = subparsers.add_parser('azure_blob_read', help='a help')
parser_a.add_argument('--u',dest='arg_value', help='--a help')
parser_a.add_argument('--c',dest='arg_value', help='--a help')

# create the parser for the "b" command
parser_b = subparsers.add_parser('azure_vm_inventory_csv', help='b help')
parser_b.add_argument(dest='container', help='--b help')

args = parser.parse_args()
print(args)
if args == "":
    print("nop")
elif args.arg_value:
    print("Value: " + args.arg_value)
