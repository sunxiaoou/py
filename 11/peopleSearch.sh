#!/bin/sh

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --remote-debugging-port=9014 --user-data-dir=/tmp/chrome \
    https://people.oracle.com/apex/f?p=8000:1:101705649184588::::P1_SEARCH:
