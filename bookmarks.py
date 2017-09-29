#!/bin/env python3

import sys
import os
from helpers import mbrofi

# user variables

# application variables
bookmark_directory = '~/bookmarks/'
BIND_NEW = 'alt-n'
BIND_DEL = 'alt-d'
script_id = 'bookmarks'
mbconfig = mbrofi.parse_config()
if script_id in mbconfig:
    lconf = mbconfig[script_id]
    bookmark_directory = lconf.get("bookmark_directory"
                                        , fallback='~/bookmarks/')
    BIND_NEW = lconf.get('bind_new', fallback='BIND_NEW')
    BIND_DEL = lconf.get('bind_del', fallback='BIND_DEL')
BOOKMARK_DIRECTORY = os.path.expanduser(bookmark_directory)

bindings = ["alt+h"]
bindings += [BIND_NEW]
bindings += [BIND_DEL]

BIND_HELPLIST = ["Show help menu."]
BIND_HELPLIST += ["Create new bookmark."]
BIND_HELPLIST += ["Bookmark bookmark."]

# launcher variables
msg = "Press Enter to open bookmark. "
msg += bindings[0] + " to show help."
#msg = "Help text. " + bindings[0] + " does something, " +  \
        #bindings[1]  + " does something else."
prompt = "bookmarks:"
answer=""
sel=""
filt=""
index=0

# run correct launcher with prompt and help message
launcher_args = {}
launcher_args['prompt'] = prompt
launcher_args['mesg'] = msg
launcher_args['filter'] = filt
launcher_args['bindings'] = bindings
launcher_args['index'] = index


def new_bookmark(name, url):
    if '/' in name:
        subdir = name.rsplit('/', 1)[0]
        if subdir:
            subpath = os.path.join(BOOKMARK_DIRECTORY, subdir)
            try:
                os.makedirs(subpath)
            except FileExistsError:
                pass
    book_path = os.path.join(BOOKMARK_DIRECTORY, name)
    if os.path.isfile(book_path):
        print("Bookmark '" + book_path + "' was found...ignoring 'add'")
        return(0)

    bookfile = open(book_path, 'w')
    bookfile.write(url.strip())
    bookfile.close()



def rofi_add_bookmark(book_name=None, book_url=None,  abort_key=None):
    add_args = {}
    add_args['prompt'] = "bookmark name:"
    add_args['mesg'] = "Write bookmark name."
    add_args['format'] = 'f'
    if abort_key is not None:
        print(abort_key)
        add_args['bindings'] = [abort_key]
    if book_name is None:
        answer, exit = mbrofi.rofi([''], add_args)
        if exit == 0 and answer is not None:
            book_name = answer.strip()
        elif exit == 1:
            sys.exit()
        else:
            return(0)
    if book_url is None:
        add_args['prompt'] = "bookmark url:"
        add_args['mesg'] = "Creating bookmark '" + book_name + "'. "
        add_args['mesg'] += "Write bookmark url."
        answer, exit = mbrofi.rofi([''], add_args)
        if exit == 0 and answer is not None:
            book_url = answer.strip()
        elif exit == 1:
            sys.exit()
        else:
            return(0)

    if book_name.strip() and book_url.strip():
        new_bookmark(book_name, book_url)

def del_bookmark(book_name):
    book_path = os.path.join(BOOKMARK_DIRECTORY, book_name)
    if os.path.isfile(book_path):
        os.remove(book_path)
    if '/' in book_name:
        book_sub = book_name.split('/')[:-1]
        if len(book_sub) > 0:
            for n in range(len(book_sub)):
                cs = ''.join(sd + '/' for sd in book_sub[:len(book_sub)-n])
                subpath = os.path.join(BOOKMARK_DIRECTORY, cs)
                if len(os.listdir(subpath)) < 1:
                    os.rmdir(subpath)




def edit_bookmark():
    pass


def open_bookmark(name):
    book_path = os.path.join(BOOKMARK_DIRECTORY, name)
    print('name: ' + name)
    print('path: ' + book_path)
    if not os.path.isfile(book_path):
        print("Bookmark '" + name + "' was not found...ignoring 'open'")
        return(False)

    bookfile = open(book_path, 'r')
    url = bookfile.readline()
    bookfile.close()
    print('url: ' + url)
    return(True)

def main(launcher_args):
    """Main function."""
    BFR = mbrofi.FileRepo(dirpath=BOOKMARK_DIRECTORY)
    BFR.scan_files(recursive=True)
    while True:
        answer, exit = mbrofi.rofi(BFR.filenames(), launcher_args)
        if exit == 1:
            return(0)
        index, filt, sel = answer.strip().split(';')
        print("index:", str(index))
        print("filter:", filt)
        print("selection:", sel)
        print("exit:", str(exit))
        print("------------------")

        launcher_args['filter'] = filt
        launcher_args['index'] = index
        if (exit == 0):
            # This is the case where enter is pressed
            if int(index) < 0:
                rofi_add_bookmark(book_name=filt.strip(), abort_key=BIND_NEW)
                launcher_args['filter'] = ''
                BFR.scan_files(recursive=True)
            else:
                open_bookmark(sel.strip())
                break
        elif exit == 10:
            helpmsg_list = BIND_HELPLIST
            mbrofi.rofi_help(bindings, helpmsg_list, prompt='bookmarks help:')
        elif exit == 11:
            if filt:
                rofi_add_bookmark(book_name=filt.strip(), abort_key=BIND_NEW)
                launcher_args['filter'] = ''
                BFR.scan_files(recursive=True)
            else:
                rofi_add_bookmark(abort_key=BIND_NEW)
                launcher_args['filter'] = ''
                BFR.scan_files(recursive=True)
        elif exit == 12:
            if int(index) < 0:
                print("No bookmark selected for deletion...ignoring")
                continue
            bookmark = sel.strip()
            ans = mbrofi.rofi_ask("Are you sure you want to delete bookmark '" +
                       bookmark + "'?", prompt='delete bookmark:',
                       abort_key=BIND_DEL)
            if ans:
                del_bookmark(bookmark)
                BFR.scan_files(recursive=True)
        else:
            break


if __name__ == '__main__':
    if not os.path.isdir(BOOKMARK_DIRECTORY):
        print("Bookmark directory does not exist at '" + BOOKMARK_DIRECTORY
                + "', creating it...")
        os.makedirs(BOOKMARK_DIRECTORY)
    main(launcher_args)
    #print('add')
    #print('---')
    #add_bookmark('hello', 'world')
    #print()
    #print('open')
    #print('----')
    #open_bookmark('hello')
