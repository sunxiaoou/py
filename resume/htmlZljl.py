#! /usr/bin/python3

import re
import os
from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint

from resume import Resume
from resume import Person
from resume import Objective
from resume import Experience
from resume import Project
from resume import Education


class HtmlZljl:
    soup = None

    @staticmethod
    def get_objective():
        elements = HtmlZljl.soup.select('.resume-preview-top')
        texts = elements[0].getText().strip().split('\n')
        items = []
        regex = re.compile(r'^$|[：]$')
        for text in texts:
            if regex.search(text) is None:
                items.append(text)

        spots = []
        for spot in re.split('，|、', items[0]):
            spots.append(spot)

        salary = -1
        try:
            salaries = re.compile(r'\d+').findall(items[1])
            salary = int(salaries[-1])
        except IndexError:
            pass

        fields = []
        try:
            for field in re.split('，|、', items[4]):
                fields.append(field.upper())
        except IndexError:
            pass

        industries = []
        try:
            for industry in re.split('，|、', items[5]):
                industries.append(industry)
        except IndexError:
            pass
        return Objective(spots, salary, fields, industries)

    @staticmethod
    def get_person(no):
        elements = HtmlZljl.soup.select('.resume-preview-main-title [class$=fc6699cc]')
        name = elements[0].getText()
        name = re.sub(r'[^\w]', '', name)          # remove special chars
        if not name or len(name) > 10:
            raise ValueError
        file = 'zljl_{:07d}_{}.html'.format(no, name)

        elements = HtmlZljl.soup.select('.summary-bottom')
        mo = re.compile(r'\D(\d{11})\D').search(elements[0].getText())
        phone = mo.group(1)

        try:
            elements = HtmlZljl.soup.select('.summary-bottom')
            regex = re.compile(r'''(
                    [a-zA-Z0-9._%+-]+      # username
                    @                      # @ symbol
                    [a-zA-Z0-9.-]+         # domain name
                    (\.[a-zA-Z]{2,4})      # dot-something
            )''', re.VERBOSE)
            email = regex.search(elements[0].getText()).group()
        except AttributeError:
            email = ''

        elements = HtmlZljl.soup.select('.summary-top')
        texts = elements[0].getText().split('\n')
        # print(":".join("{:02x}".format(ord(c)) for c in text))
        a = re.split(u'\xa0\xa0\xa0\xa0', texts[1])     # 4 non Break Spaces

        if a[0] != '男' and a[0] != '女':
            raise TypeError             # maybe english
        gender = a[0]

        mo = re.compile(r'(\d{4})年(\d{1,2})月').search(a[1])
        birth = datetime(int(mo.group(1)), int(mo.group(2)), 15)

        try:
            mo = re.compile(r'(\d{1,2})年工作经验').search(a[2])
            years = int(mo.group(1))
        except AttributeError:
            years = -1

        try:
            if years == -1:
                education = Education.educationList.index(a[2].upper()) + 1
            else:
                education = Education.educationList.index(a[3].upper()) + 1
        except (IndexError, ValueError):
            education = -1

        return Person(file, name, gender, birth, phone, email, education, years, HtmlZljl.get_objective())

    @staticmethod
    def get_experiences():
        tag = HtmlZljl.soup.find('h3', text='工作经历')
        if tag is None:
            return []
        tag = tag.find_parent()
        if not tag['class'][0].startswith('resume-preview-all'):
            return []

        experiences = []
        for h2 in tag.findAll('h2'):
            date1 = date2 = company = company_desc = job = job_desc = ''

            text = h2.getText().strip()
            a = re.split(u'\xa0\xa0| - ', text)
            try:
                date1 = a[0]
                date2 = a[1]
                company = a[2]
            except IndexError:
                pass

            sibling = h2.find_next_sibling()
            while sibling is not None and sibling.name != 'h2':
                if sibling.name == 'h5':
                    job = sibling.getText().strip()
                elif sibling['class'][0] == 'resume-preview-dl':
                    if sibling.string is not None:
                        company_desc = sibling.getText().strip()
                    else:
                        for td in sibling.findAll('td'):
                            if td.getText() != '工作描述：':
                                job_desc = td.getText().replace('\'', '’')
                sibling = sibling.find_next_sibling()
            experiences.append(Experience(date1, date2, company, company_desc, job, job_desc))
        return experiences

    @staticmethod
    def get_projects():
        tag = HtmlZljl.soup.find('h3', text='项目经历')
        if tag is None:
            return []
        tag = tag.find_parent()
        if not tag['class'][0].startswith('resume-preview-all'):
            return []

        projects = []
        for h2 in tag.findAll('h2'):
            date1 = date2 = name = description = duty = ''

            text = h2.getText().strip()
            a = re.split(u'\xa0\xa0| - ', text)
            try:
                date1 = a[0]
                date2 = a[1]
                name = a[2]
            except IndexError:
                pass

            sibling = h2.find_next_sibling()
            while sibling is not None and sibling.name != 'h2':
                tds = sibling.findAll('td')
                for i in range(len(tds)):
                    if tds[i].getText() == '责任描述：':
                        i += 1
                        duty = tds[i].getText().replace('\'', '’')
                    elif tds[i].getText() == '项目描述：':
                        i += 1
                        description = tds[i].getText().replace('\'', '’')
                sibling = sibling.find_next_sibling()

            projects.append(Project(date1, date2, name, description, duty))
        return projects

    @staticmethod
    def get_educations():
        tag = HtmlZljl.soup.find('h3', text='教育经历')
        if tag is None:
            return []
        tag = tag.find_parent()
        if not tag['class'][0].startswith('resume-preview-all'):
            return []

        educations = []
        for element in tag.findAll(class_='resume-preview-dl'):
            date1 = date2 = school = major = degree = ''
            text = element.getText().strip()
            a = re.split(u'\xa0\xa0| - ', text)
            try:
                date1 = a[0]
                date2 = a[1]
                school = a[2]
                major = a[3]
                degree = Education.educationList.index(a[4].upper()) + 1
            except (IndexError, ValueError):
                pass
            educations.append(Education(date1, date2, school, major, degree))
        return educations

    @staticmethod
    def get_skills():
        tag = HtmlZljl.soup.find('h3', text='专业技能')
        if tag is None:
            return []
        tag = tag.find_next_sibling()
        if not tag['class'][0].startswith('resume-preview-dl'):
            return []

        skills = []
        texts = tag.getText().split('\n')
        for text in texts:
            if re.compile('^ *$').search(text) is not None:
                continue
            a = re.split(r'：| \| ', text)
            try:
                if a[1] == '良好' or a[1] == '熟练' or a[1] == '精通':
                    for skill in re.compile(r'[\da-zA-Z/#]+').findall(a[0]):
                        skills.append(skill.upper())
            except IndexError:
                pass
        return list(set(skills))        # no duplicate

    @staticmethod
    def new_resume(html, no):
        HtmlZljl.soup = BeautifulSoup(open(html), 'lxml')
        return Resume(HtmlZljl.get_person(no), HtmlZljl.get_experiences(), HtmlZljl.get_projects(),
                      HtmlZljl.get_educations(), HtmlZljl.get_skills())


def main():
    folder = '/home/xixisun/suzy/shoulie/resumes/zljl'
    # file = '1001275097619586627470818947.html'
    # file = '10157404450912834562061694406.html'
    # file = '智联招聘_陶秀玲_法务部部长_中文_20130502_24441247.html'
    # file = '朱斌国简历_智联招聘.html'
    file = 'zljl0435506.html'
    # parser = HtmlParser(os.path.join(folder, file), 1)
    # resume = parser.new_resume()
    resume = HtmlZljl.new_resume(os.path.join(folder, file), 2)
    pprint(resume.to_dictionary())

if __name__ == "__main__":
    main()
