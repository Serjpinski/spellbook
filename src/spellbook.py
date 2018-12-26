import os
import sys


BASE_PATH = "."  # TODO handle data location better
BOOKS_PATH = os.path.join(BASE_PATH, "books")


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
        op_add(args[1], None if args_len == 2 else args[2])


def op_list(book):

    if book is None:
        print("Listing books")
        print("=============")
        books = file_to_dict(BOOKS_PATH)
        for book in books:
            print("{}\t{}".format(book, books[book]))
    else:
        print("Listing spells for book {}".format(book))


def op_add(book, description):

    print("Adding book {}".format(book))
    books = file_to_dict(BOOKS_PATH)
    books[book] = "" if description is None else description
    dict_to_file(books, BOOKS_PATH)


def file_to_dict(path):
    dictionary = dict()
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f.readlines():
                try:
                    kv = line.split("\t")
                    dictionary[kv[0]] = kv[1].replace("\n", "")
                except IndexError:
                    pass
    return dictionary


def dict_to_file(dictionary, path):
    with open(path, 'w') as f:
        f.write("\n".join([key + "\t" + dictionary[key] for key in dictionary]))


if __name__ == '__main__':
    main()
