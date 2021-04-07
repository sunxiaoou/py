#! /usr/bin/python3

import shelve, pyperclip, sys

mcbShelf = shelve.open('mcb')

# Save clipboard content.
if len(sys.argv) == 3 and sys.argv[1].lower() == 'save':
    mcbShelf[sys.argv[2]] = pyperclip.paste()
elif len(sys.argv) == 2:
    # List keywords and load content.
    if sys.argv[1].lower() == 'list':
        pyperclip.copy(str(list(mcbShelf.keys())))
    elif sys.argv[1] in mcbShelf:
        pyperclip.copy(mcbShelf[sys.argv[1]])
else:
    print('Usage: ' + sys.argv[0] + ' save <keyword> - Saves clipboard to keyword.')
    print('       ' + sys.argv[0] + ' <keyword> - Loads clipboard to keyword.')
    print('       ' + sys.argv[0] + ' list - Loads all keywords to clipboard.')

mcbShelf.close()
