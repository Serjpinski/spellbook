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
    args_len = len(args)

    if args_len == 0:
        print(get_usage())
    elif args[0] == "list":
        op_list(args[1:], True)
    elif args[0] == "listj":
        op_list(args[1:], False)
    elif args[0] == "add" and args_len > 1:
        op_add(args[1:])
    elif args[0] == "remove" and args_len > 1:
        op_remove(args[1:])
    else:
        print(get_usage())


# # # SPELL CRUD OPERATIONS # # #

def get_hierarchy(tree, name):

    if len(name) == 0:
        return [tree]

    if name[0] in tree["spells"]:
        return [tree] + get_hierarchy(tree["spells"][name[0]], name[1:])

    return [tree]


def op_list(name, compact):

    book = get_book()
    hierarchy = get_hierarchy(book, name)

    if len(hierarchy) == len(name) + 1:
        if compact:
            print_spell_compact(name, hierarchy[-1])
        else:
            print(json.dumps(hierarchy[-1], indent=4, sort_keys=True))
    else:
        print("Spell not found: {}".format(" ".join(name)))


def op_add(name):

    book = get_book()
    hierarchy = get_hierarchy(book, name)

    # Create missing spells
    while len(hierarchy) < len(name) + 1:
        spell = dict()
        spell["spells"] = dict()
        hierarchy[-1]["spells"][name[len(hierarchy) - 1]] = spell
        hierarchy.append(spell)

    spell = hierarchy[-1]

    if "command" not in spell:
        spell["command"] = input("Spell command: ")
    else:
        print("Current command: {}".format(spell["command"]))
        spell["command"] = input("New command: ")

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
        update_data_files(book)

    return book


def update_data_files(book):
    json_to_file(book, BOOK_FILE)
    string_to_file(get_aliases(book), ALIAS_FILE)


def get_usage():

    return ("Usage:\n"
            "list\t\t\tList all spells in the book (use listj for json output)\n"
            "list <spell>\t\tList <spell> and its children (use listj for json output)\n"
            "add <spell>\t\tAdd <spell> to the book\n"
            "remove <spell>\t\tRemove <spell> and its children from the book\n")


# # # ALIAS GENERATION # # #

def get_aliases(book):
    return "\n".join([get_root_alias(spell, book["spells"][spell]) for spell in book["spells"]])


def get_root_alias(name, spell):
    function_statement = "function {} () {{\n{}\n}}\n"
    return function_statement.format(name, get_alias([name], spell, 1))


# TODO support commands for non-leaf commands
def get_alias(name, spell, depth):

    test_statement = "[ ${} = \"{}\" ]"

    if len(spell["spells"]) > 0:
        return "\n".join([get_alias(name + [subspell], spell["spells"][subspell], depth + 1) for subspell in spell["spells"]])

    command_statement = "\t"

    for arg_index in range(1, len(name)):
        command_statement += test_statement.format(arg_index, name[arg_index]) + " && "

    return command_statement + get_resolve_statement(spell, depth)


# TODO support configuring delimiters
def get_resolve_statement(spell, depth):
    return "$(python3 " + BASE_DIR + "/resolve.py \"" + spell["command"] + "\" { } \"${@:" + str(depth) + "}\")"


# # # MISC # # #

def print_spell_compact(name, spell):

    if "command" in spell:
        print(" ".join(name) + " => " + ("" if spell["command"] is None else spell["command"]))
    for subname, subspell in sorted(spell["spells"].items()):
        print_spell_compact(name + [subname], subspell)


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
