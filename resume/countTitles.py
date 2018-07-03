#! /usr/bin/python3
# or /opt/python/bin/python3

import re
import os
import shutil

from bs4 import BeautifulSoup


def get_title(html):
    try:
        soup = BeautifulSoup(open(html), 'lxml')
    except UnicodeDecodeError:
        # with open(html, 'rb') as html:
        #    soup = BeautifulSoup(html, 'lxml')
        return 'ude'
    except Exception as exception:
        return type(exception).__name__

    tag = soup.find("title")
    if tag is None:
        return 'none'
    text = tag.getText()
    if '举贤网-专注中高端人才职业机会' in text:
        return 'jxw'
    if re.search(r'\n\t.*\n', text, re.MULTILINE) is not None:
        return 'j51'
    return text


def count_titles():
    titles = {}
    i = 0
    for folderName, subfolders, fileNames in os.walk(orig):
        for fileName in fileNames:
            fn = folderName + '/' + fileName
            title = get_title(fn)
            print('{:07d}, '.format(i + 1) + fn + ', ' + title)
            i += 1

            print('{:06d}, '.format(i + 1) + fn + ', ' + title)
            i += 1
            if title not in titles.keys():
                titles[title] = 1
            else:
                titles[title] += 1

            try:
                if title == 'ude':
                    shutil.move(fn, ude)
                elif title == 'none':
                    shutil.move(fn, none)
                elif title == '简历':
                    shutil.move(fn, jl)
                elif title == '我的简历':
                    shutil.move(fn, wdjl)
                elif title == '智联简历':
                    shutil.move(fn, zljl)
                elif title == '简历管理_我的智联_智联招聘':
                    shutil.move(fn, zlzp)
                elif title == '尊敬的猎聘网用户':
                    shutil.move(fn, lpw)
                elif title == 'jxw':
                    shutil.move(fn, jxw)
                elif title == 'j51':
                    shutil.move(fn, j51)
                else:
                    shutil.move(fn, other)
            except shutil.Error:
                pass

    sort_titles = sorted(titles.items(), key=lambda kv: kv[1])      # sort by values
    print(sort_titles)


# html = '/home/xixisun/suzy/resumes/0001/2/jm090122773r90250000000_2015-03-08_0.html'
# print(get_title(html))

parent = '/home/xixisun/suzy/resumes/'
# parent = '/scratch/xixisun/shoulie/'

orig = parent + 'orig/'
new = parent + 'new/'

ude = new + 'ude'
if not os.path.exists(ude):
    os.makedirs(ude)

none = new + 'none'
if not os.path.exists(none):
    os.makedirs(none)

jl = new + 'jl'
if not os.path.exists(jl):
    os.makedirs(jl)

wdjl = new + 'wdjl'
if not os.path.exists(wdjl):
    os.makedirs(wdjl)

zljl = new + 'zljl'
if not os.path.exists(zljl):
    os.makedirs(zljl)

zlzp = new + 'zlzp'
if not os.path.exists(zlzp):
    os.makedirs(zlzp)

lpw = new + 'lpw'
if not os.path.exists(lpw):
    os.makedirs(lpw)

jxw = new + 'jxw'
if not os.path.exists(jxw):
    os.makedirs(jxw)

j51 = new + 'j51'
if not os.path.exists(j51):
    os.makedirs(j51)

other = new + 'other'
if not os.path.exists(other):
    os.makedirs(other)

count_titles()
