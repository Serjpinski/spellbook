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
    else:
        print(get_usage())


def get_usage():

    return ("Usage:\n"
            "spellbook.py list [<spell>]\n"
            "spellbook.py add <spell>")


def op_list(name):

    book = file_to_json(BOOK_FILE)
    to_print = get_spell(book, name)
    if to_print is not None:
        print(json.dumps(to_print, indent=4))


def get_spell(book, name):

    if len(name) == 0:
        return book

    if "spells" in book:
        for spell in book["spells"]:
            if spell["name"] == name[0]:
                return get_spell(spell, name[1:])

    return None


def op_add(name):

    book = file_to_json(BOOK_FILE)
    parent = get_spell(book, name[:-1])

    if parent is None:
        print("Parent not found: {}".format(" ".join(name[:-1])))
        return

    leaf_name = name[-1]

    if "spells" not in parent:
        parent["spells"] = list()

    index = 0
    spell = dict()

    while index < len(parent["spells"]) and leaf_name >= parent["spells"][index]["name"]:
        if leaf_name == parent["spells"][index]["name"]:
            spell = parent["spells"][index]
        index += 1

    if "name" not in spell:
        spell["name"] = leaf_name
        parent["spells"].insert(index, spell)
        print("Adding new spell: {}".format(" ".join(name)))
    else:
        print("Updating spell: {}".format(" ".join(name)))

    spell["description"] = None
    spell["command"] = None
    json_to_file(book, BOOK_FILE)


def file_to_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.loads(f.read())
    return dict()


def json_to_file(j, path):
    with open(path, 'w') as f:
        f.write(json.dumps(j))


if __name__ == '__main__':
    main()
