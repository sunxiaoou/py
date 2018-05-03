#! /usr/bin/python3

import os
import shutil

from bs4 import BeautifulSoup


def get_title(html):
    try:
        soup = BeautifulSoup(open(html), 'lxml')
    except Exception as exception:
        return type(exception).__name__
    tag = soup.find("title")
    if tag is None:
        return 'null'
    return tag.getText()


def count_titles():
    titles = {}
    i = 0
    for folderName, subfolders, fileNames in os.walk(folder):
        for fileName in fileNames:
            ext = os.path.splitext(fileName)[1]
            if ext != '.htm' and ext != '.html':
                continue
            fn = folderName + '/' + fileName
            # print(fn)
            title = get_title(fn)

            print('{:06d}, '.format(i + 1) + fn + ', ' + title)
            i += 1
            if title not in titles.keys():
                titles[title] = 1
            else:
                titles[title] += 1

            if title == '简历':
                shutil.copy(fn, fd1)
            elif title == '智联简历':
                shutil.copy(fn, fd2)
            elif title == '简历管理_我的智联_智联招聘':
                shutil.copy(fn, fd3)
    print(titles)


# html = '/home/xixisun/suzy/resumes/0001/2/jm090122773r90250000000_2015-03-08_0.html'
# print(get_title(html))
folder = '/home/xixisun/suzy/resumes/0001'
fd1 = '/home/xixisun/suzy/resumes/html/jl'
fd2 = '/home/xixisun/suzy/resumes/html/zljl'
fd3 = '/home/xixisun/suzy/resumes/html/zlzp'
count_titles()
