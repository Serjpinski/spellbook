import json
import os
import sys

BOOK_FILE = "book.json"
ALIAS_FILE = "book.alias"


# spell add goto
# spell goto add
#
# spell list
# spell goto list
def main():

    args = sys.argv[1:]
    args_len = len(args)

    if args_len == 0:
        print(get_usage())
    elif args[0] == "list":
        op_list(args[1:])
    elif args[0] == "add" and args_len > 1:
        op_add(args[1:])
    elif args[0] == "remove" and args_len > 1:
        op_remove(args[1:])
    else:
        print(get_usage())


def get_usage():

    return ("Usage:\n"
            "spellbook.py list [<spell>]\n"
            "spellbook.py add <spell>\n"
            "spellbook.py remove <spell>")


def op_list(name):

    book = get_book()
    to_print = get_spell(book, name)
    if to_print is not None:
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
        return

    leaf_name = name[-1]

    if leaf_name not in parent["spells"]:
        spell = dict()
        parent["spells"][leaf_name] = spell
        print("Adding new spell: {}".format(" ".join(name)))
    else:
        spell = parent["spells"][leaf_name]
        print("Updating spell: {}".format(" ".join(name)))

    spell["description"] = None
    spell["command"] = None
    spell["spells"] = dict()
    json_to_file(book, BOOK_FILE)


def op_remove(name):

    book = get_book()
    parent = get_spell(book, name[:-1])
    if parent is None:
        print("Parent not found: {}".format(" ".join(name[:-1])))
    elif name[-1] not in parent["spells"]:
        print("Spell not found: {}".format(" ".join(name)))
    else:
        print("Removing spell: {}".format(" ".join(name)))
        parent["spells"].pop(name[-1])
        json_to_file(book, BOOK_FILE)


def get_book():

    book = file_to_json(BOOK_FILE)

    if book is None:
        book = dict()
        book["spells"] = dict()
        json_to_file(book, BOOK_FILE)

    return book


def file_to_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.loads(f.read())
    return None


def json_to_file(j, path):
    with open(path, 'w') as f:
        f.write(json.dumps(j))


if __name__ == '__main__':
    main()
