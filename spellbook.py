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


### SPELL CRUD OPERATIONS ###

def op_list(name, compact):

    book = get_book()
    to_print = get_spell(book, name)
    if to_print is not None:
        if compact:
            print_spell_compact(name, to_print)
        else:
            print(json.dumps(to_print, indent=4, sort_keys=True))


def get_spell(book, name):

    if len(name) == 0:
        return book

    if name[0] in book["spells"]:
        return get_spell(book["spells"][name[0]], name[1:])

    return None


def op_add(name):

    book = get_book()
    parent = get_spell(book, name[:-1])

    if parent is None:
        print("Parent not found: {}".format(" ".join(name[:-1])))
        exit(1)

    leaf_name = name[-1]

    if leaf_name not in parent["spells"]:
        spell = dict()
        parent["spells"][leaf_name] = spell
        print("Adding new spell: {}".format(" ".join(name)))
        spell["command"] = input("Spell command: ")
    else:
        spell = parent["spells"][leaf_name]
        print("Updating spell: {}".format(" ".join(name)))
        print("Current command: {}".format(spell["command"]))
        spell["command"] = input("New command: ")

    spell["spells"] = dict()
    update_data_files(book)


def op_remove(name):

    book = get_book()
    parent = get_spell(book, name[:-1])
    if parent is None:
        print("Parent not found: {}".format(" ".join(name[:-1])))
        exit(1)
    elif name[-1] not in parent["spells"]:
        print("Spell not found: {}".format(" ".join(name)))
        exit(1)
    else:
        print("Removing spell: {}".format(" ".join(name)))
        parent["spells"].pop(name[-1])
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


### ALIAS GENERATION ###

def get_aliases(book):
    return "\n".join([get_root_alias(spell, book["spells"][spell]) for spell in book["spells"]])


def get_root_alias(name, spell):
    function_statement = "function {} () {{\n{}\n}}\n"
    return function_statement.format(name, get_alias([name], spell))


def get_alias(name, spell):

    test_statement = "[ ${} = \"{}\" ]"

    if len(spell["spells"]) > 0:
        return "\n".join([get_alias(name + [subspell], spell["spells"][subspell]) for subspell in spell["spells"]])

    command_statement = "\t"

    for arg_index in range(1, len(name)):
        command_statement += test_statement.format(arg_index, name[arg_index]) + " && "

    return command_statement + spell["command"]


### MISC ###

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
