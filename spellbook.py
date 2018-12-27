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

    if args[0] == "list":
        op_list(None if args_len == 1 else args[1])
    elif args[0] == "add":
        op_add(args[1], None if args_len == 2 else args[2], None)


def op_list(name):

    if name is None:
        book = file_to_json(BOOK_FILE)
        print(json.dumps(book["spells"], indent=4) if "spells" in book else "")
    else:
        print("Listing subspells for spell {}".format(name))


def op_add(name, description, command):

    book = file_to_json(BOOK_FILE)

    if "spells" not in book:
        book["spells"] = list()

    index = 0
    spell = dict()

    while index < len(book["spells"]) and name >= book["spells"][index]["name"]:
        if name == book["spells"][index]["name"]:
            spell = book["spells"][index]
        index += 1

    if "name" not in spell:
        spell["name"] = name
        book["spells"].insert(index, spell)
        print("Adding new spell {}".format(name))
    else:
        print("Updating spell {}".format(name))

    spell["description"] = description
    spell["command"] = command
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
