import argparse
from argparse import RawTextHelpFormatter
from Parser_Helpers.module_selection_class import user_selection
import Parser_Helpers.modules as modules


def main():
    """ The message is splitted in two parts as a list in order to be able to chose one"""
    message = ["Module was not found. Maybe it is misspelled or I just didn't have time to develop it yet :)\n",
               "Allowed values for -m, --module\n\n",
               '------ AWS ------\n' + '\n'.join(modules.options_aws) \
               + "\n\n------ Azure ------\n" + '\n'.join(modules.options_azure) \
               + "\n\n------ GCP ------\n" + '\n'.join(modules.options_gcp)
               ]
    help_message = message[2]
    wrong_selection_message = message[0] + message[1] + message[2]

    """ Argument Parser """
    parser = argparse.ArgumentParser(description='Select the script to be run', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-m', '--module', dest="arg_value", metavar='', type=str, help=help_message)
    args = parser.parse_args()
    selection = user_selection(args.arg_value, wrong_selection_message)  # Add the value to the user class

    # Run Script based on the provided value
    if not args.arg_value:
        print(wrong_selection_message)
    elif "AWS_" in args.arg_value:
        selection.aws_selected()
    elif "Azure_" in args.arg_value:
        selection.azure_selected()
    elif "GCP_" in args.arg_value:
        selection.gcp_selected()
    else:
        print(wrong_selection_message)


main()
