import re
import sys

from spell import parse_args


# Gets a command, left/right delimiters for variables and a list of arguments.
# Returns the command with variables substituted with arguments.
# TODO migrate to bash?
def main():

    command = sys.argv[1]
    left_del = sys.argv[2]
    right_del = sys.argv[3]
    args = sys.argv[4:]

    named_args, ordered_args = parse_args(args)

    for arg_name in named_args:
        command = re.sub(re.escape(left_del) + arg_name + re.escape(right_del), named_args[arg_name], command)

    for arg in ordered_args:
        command = re.sub(re.escape(left_del) + "[a-zA-Z0-9_-]*" + re.escape(right_del), arg, command, count=1)

    print(command)


if __name__ == '__main__':
    main()
