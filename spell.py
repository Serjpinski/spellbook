import json
import os
import sys

BASE_DIR = os.path.dirname(__file__)
BOOK_FILE = os.path.join(BASE_DIR, "book.json")
ALIAS_FILE = os.path.join(BASE_DIR, "book.alias")


# TODO add spell modifiers: resolve values of a group of arguments in a spell, i.e.:
# TODO my > mysql -h {{host}} -u {{user}} -p{{pass}} -e {{command}}
# TODO modifier "local" > {"host": "localhost", "user": "localuser", "pass": "somepassword"}
# TODO modifier "prod" > {"host": "mysql-prod-ip", "user": "produser", "pass": "otherpassword"}
# TODO then you can: my --prod select 1

# TODO good example for usage;
# TODO shfor => for i in {{array}}; do {{command}}; done
# TODO array => a b c
# TODO command => echo $i
# TODO for i in a b c; do echo $i; done

# TODO use external bash file with functions to process arguments and/or resolve final command?

def main():

    args = sys.argv[1:]
    named_args, ordered_args = parse_args(args)

    if len(ordered_args) == 0:
        print(get_usage())
    elif ordered_args[0] == "list":
        op_list(ordered_args[1:])
    elif ordered_args[0] == "add" and len(ordered_args) > 1:
        op_add(ordered_args[1:], named_args)
    elif ordered_args[0] == "remove" and len(ordered_args) > 1:
        op_remove(ordered_args[1:])
    # TODO add import/export from/to json
    else:
        print(get_usage())
        exit(1)


# # # SPELL CRUD OPERATIONS # # #

def get_hierarchy(tree, name):

    if len(name) == 0:
        return [tree]

    if name[0] in tree["spells"]:
        return [tree] + get_hierarchy(tree["spells"][name[0]], name[1:])

    return [tree]


def op_list(name):

    book = get_book()
    hierarchy = get_hierarchy(book, name)

    if len(hierarchy) == len(name) + 1:
        print_spell(name, hierarchy[-1])
    else:
        print("Spell not found: {}".format(" ".join(name)))
        exit(1)


def op_add(name, args):

    command = args["c"] if "c" in args else None
    left_delimiter = args["ld"] if "ld" in args else None
    right_delimiter = args["rd"] if "rd" in args else None

    if command is None:
        print("Missing argument: -c <command>")
        exit(1)

    book = get_book()
    hierarchy = get_hierarchy(book, name)

    # Create missing spells
    while len(hierarchy) < len(name) + 1:
        spell = dict()
        spell["spells"] = dict()
        hierarchy[-1]["spells"][name[len(hierarchy) - 1]] = spell
        hierarchy.append(spell)

    spell = hierarchy[-1]
    
    spell["command"] = command

    if left_delimiter is not None:
        spell["left_delimiter"] = left_delimiter
    if right_delimiter is not None:
        spell["right_delimiter"] = right_delimiter

    update_data_files(book)


def op_remove(name):

    book = get_book()
    hierarchy = get_hierarchy(book, name)
    if len(hierarchy) < len(name):
        print("Parent not found: {}".format(" ".join(name[:-1])))
        exit(1)
    elif len(hierarchy) < len(name) + 1:
        print("Spell not found: {}".format(" ".join(name)))
        exit(1)
    else:
        hierarchy[-2]["spells"].pop(name[-1])
        update_data_files(book)


def get_book():

    book = file_to_json(BOOK_FILE)

    if book is None:
        book = dict()
        book["spells"] = dict()
        book["left_delimiter"] = "{"
        book["right_delimiter"] = "}"
        update_data_files(book)

    return book


def update_data_files(book):
    json_to_file(book, BOOK_FILE)
    string_to_file(get_aliases(book), ALIAS_FILE)


def get_usage():

    return ("Usage:\n"
            "list\t\t\tList all spells in the book\n"
            "list <spell>\t\tList <spell> and its children\n"
            "add <spell> -c <command> [-ld <left_delimiter>]  [-rd <right_delimiter>]\t\tAdd <spell> to the book\n"
            "remove <spell>\t\tRemove <spell> and its children from the book\n")


# # # ALIAS GENERATION # # #

def get_aliases(book):
    return "\n".join([
        get_root_alias(spell, book["spells"][spell], book["left_delimiter"], book["right_delimiter"])
        for spell in book["spells"]])


def get_root_alias(name, spell, left_delimiter, right_delimiter):
    function_statement = "function {} () {{\n{}\n}}\n"
    return function_statement.format(name, get_alias([name], spell, left_delimiter, right_delimiter, 1))


# TODO support commands for non-leaf spells
def get_alias(name, spell, left_delimiter, right_delimiter, depth):

    left_delimiter = spell["left_delimiter"] if "left_delimiter" in spell else left_delimiter
    right_delimiter = spell["right_delimiter"] if "right_delimiter" in spell else right_delimiter

    test_statement = "[ ${} = \"{}\" ]"

    if len(spell["spells"]) > 0:
        return "\n".join([
            get_alias(name + [subspell], spell["spells"][subspell], left_delimiter, right_delimiter, depth + 1)
            for subspell in spell["spells"]])

    command_statement = "\t"

    for arg_index in range(1, len(name)):
        command_statement += test_statement.format(arg_index, name[arg_index]) + " && "

    return command_statement + get_resolve_statement(spell["command"], left_delimiter, right_delimiter, depth)


def get_resolve_statement(command, left_delimiter, right_delimiter, depth):
    return "$(python3 " + BASE_DIR + "/resolve.py \"" + command + "\" \""\
           + left_delimiter + "\" \"" + right_delimiter + "\" \"${@:" + str(depth) + "}\")"


# # # MISC # # #

def parse_args(args):

    named_args = dict()
    ordered_args = list()

    arg_name = None

    for arg in args:
        if arg.startswith("-"):
            arg_name = arg[2:] if arg.startswith("--") else arg[1:]
        elif arg_name is not None:
            named_args[arg_name] = arg
            arg_name = None
        else:
            ordered_args.append(arg)

    return named_args, ordered_args


def print_spell(name, spell):

    if "command" in spell:
        print(" ".join(name) + " => " + ("" if spell["command"] is None else spell["command"]))
    for subname, subspell in sorted(spell["spells"].items()):
        print_spell(name + [subname], subspell)


def file_to_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.loads(f.read())
    return None


def json_to_file(j, path):
    string_to_file(json.dumps(j), path)


def string_to_file(string, path):
    with open(path, 'w') as f:
        f.write(string)


if __name__ == '__main__':
    main()
