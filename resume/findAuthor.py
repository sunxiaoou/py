#! /usr/bin/python3
import re
import bs4
import sys


def get_preview_list():
    elems = soup.select('.resume-preview-list')
    return elems


def get_summary_top():
    # elems = soup.select('.summary-top span')
    elems = soup.select('.summary-top')
    return elems[0].getText().split()


def get_summary_bottom():
    # elems = soup.select('.summary-top span')
    elems = soup.select('.summary-bottom')
    return elems[0].getText().split()


def get_preview_all():
    elems = soup.select('.resume-preview-all')
    return elems


def get_name():
    elems = soup.select('#userName')
    return elems[0].getText().strip()


def get_gender():
    elems = soup.select('.summary-top')
    male = re.compile('男')
    female = re.compile('女')
    if male.search(elems[0].getText()) is not None:
        return '男'
    if female.search(elems[0].getText()) is not None:
        return '女'
    return None


def get_date_of_birth():
    elems = soup.select('.summary-top')
    dob = re.compile(r'\d{4}年\d{1,2}月')
    mo = dob.search(elems[0].getText())
    if mo is None:
        return ''
    return mo.group()


def get_school():
    elems = soup.select("[class$=educationContent]")
    if len(elems) == 0:
        return ''
    school = re.compile(r'\S*{0}'.format('(大学|学院)'))
    mo = school.search(elems[0].getText())
    if mo is None:
        return ''
    return mo.group()


# def get_major():


def get_education():
    # elems = soup.select("[class$=educationContent]")
    # if len(elems) == 0:
    elem = soup.find('div', class_='resume-preview-dl educationContent')
    if elem is None:
        print(2)
        elem = soup.find('h3', text='教育经历').find_next_sibling()
    return elem.getText().strip()


def get_experience():
    # elems = soup.select("[class$=workExperience]")
    # elems = soup.select('[class$=workExperience] h2')
    elem = soup.find('div', class_='resume-preview-all workExperience')
    if elem is None:
        print(2)
        elem = soup.find('h3', text='工作经历').find_parent()
    elems = elem.findAll('h2')
    return elems[0].getText().strip()


def get_table():
    elems = soup.select('.resume-preview-top')
    return elems[0].getText().strip()


# html = open('../html/jm089618041r90250000000_2015-08-24_0.html')
html = open('/home/xixisun/suzy/resumes/0001/2/jm089638951r90250000000_2015-01-28_0.html')
# html = open('/home/xixisun/suzy/resumes/0001/2/jm090122773r90250000000_2015-03-08_0.html')

soup = bs4.BeautifulSoup(html.read(), "lxml")

# for tag in get_preview_list():
#    print(tag.getText().strip())


# name = get_name()

# summaryTop = get_summary_top()
# summaryBottom = get_summary_bottom()
# phone = getPhone()
# education = getEducation()


# print("name: " + get_name())
# print("gender: " + get_gender())
# print("dayOfBirth: " + get_date_of_birth())
# print("school: " + get_school())

# print("Summary top:")
# print(get_summary_top())
# print("Summary bottom:")
# print(get_summary_bottom())

print("Education: ")
print(get_education())

print("Experience: ")
print(get_experience())

# print('CREATE TABLE {} ({} {}, {} {}, {} {}, {} {}, {} {})'.
#      format('person', 'name', 'TEXT', 'gender', 'TEXT', 'birth', 'TEXT', 'phone', 'INTEGER', 'email', 'TEXT'))

print('CREATE TABLE person (name TEXT, gender TEXT, birth TEXT, email TEXT, phone INTEGER PRIMARY KEY)')
print('CREATE TABLE objective (spot TEXT, salary INTEGER, field TEXT, industry TEXT, phone INTEGER, '
      'FOREIGN KEY(phone) REFERENCES person(phone))')
print('CREATE TABLE experience (start_date TEXT, end_date TEXT, company TEXT, job TEXT, phone INTEGER, '
      'FOREIGN KEY(phone) REFERENCES person(phone))')
print('CREATE TABLE education (start_date TEXT, end_date TEXT, school TEXT, major TEXT, degree TEXT, phone INTEGER, '
      'FOREIGN KEY(phone) REFERENCES person(phone))')


sys.exit(1)

# print(get_table())
text = get_table()
print(text + '\n')

items = []
regex = re.compile(r'^$|[：]$')
texts = str(text).split('\n')
for text in texts:
    if regex.search(text) is None:
        items.append(text)

del items[2], items[2]
print(items)

# print("Preview all:")
# for tag in get_preview_all():
#    print(tag.getText().strip())
#    print()

print()
# print(soup.get_text().strip())
