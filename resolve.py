import sys


# Gets a command, left/right delimiters for variables and a list of arguments.
# Returns the command with variables substituted with arguments.
def main():

    command = sys.argv[1]
    left_delimiter = sys.argv[2]
    right_delimiter = sys.argv[3]
    args = sys.argv[4:]
    print(command + left_delimiter + right_delimiter + args)
