import re
import sys


# Gets a command, left/right delimiters for variables and a list of arguments.
# Returns the command with variables substituted with arguments.
# TODO migrate to bash?
def main():

    command = sys.argv[1]
    left_del = sys.argv[2]
    right_del = sys.argv[3]
    args = sys.argv[4:]

    named_args = dict()
    ordered_args = list()

    arg_name = None

    for arg in args:
        if arg.startswith("--"):
            arg_name = arg[2:]
        elif arg.startswith("-"):
            arg_name = arg[1:]
        elif arg_name is not None:
            named_args[arg_name] = arg
            arg_name = None
        else:
            ordered_args.append(arg)

    for arg_name in named_args:
        command = re.sub(re.escape(left_del) + arg_name + re.escape(right_del), named_args[arg_name], command)

    for arg in ordered_args:
        command = re.sub(re.escape(left_del) + "[a-zA-Z0-9_-]*" + re.escape(right_del), arg, command, count=1)

    print(command)


if __name__ == '__main__':
    main()
