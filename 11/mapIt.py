#! /usr/bin/python3

# mapIt.py - Launches a map in the browser using an address from the
# command line or clipboard.

# Address format:
# House Number, Street Direction, Street Name, Street Suffix, City, State, Zip, Country
# 870 Valencia St, San Francisco, CA 94110
# Lianhua community, Lianhuachi West Rd Side Rd, Haidian, Beijing, China, 1000361

import webbrowser, sys, pyperclip

if len(sys.argv) > 1:
    # Get address from command line.
    address = ' '.join(sys.argv[1:])
else:
    # Get address from clipboard.
    address = pyperclip.paste()

webbrowser.open('https://www.google.com/maps/place/' + address)
