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


class HtmlJxw:
    type = 'jxw'
    soup = None

    @staticmethod
    def get_type():
        return HtmlJxw.type

    @staticmethod
    def get_objective():
        tag = HtmlJxw.soup.find('h3', text='求职意向')
        if tag is None:
            return None
        tag = tag.find_parent()
        if tag['class'][0] != 'title_h3v6':
            return None

        texts = tag.find_next_sibling().getText().split('\n')
        items = []
        regex = re.compile(r'^\s*$')       # delete lines of empty
        for text in texts:
            if regex.search(text) is None:
                items.append(text.strip())

        industries = []
        try:
            i = items.index('期望行业：')
            for industry in re.split(',|·', items[i + 1]):
                industries.append(industry)
        except (IndexError, ValueError):
            pass

        fields = []
        try:
            i = items.index('期望职位：')
            for field in re.split(',|·', items[i + 1]):
                fields.append(field.upper())
        except (IndexError, ValueError):
            pass

        spots = []
        try:
            i = items.index('期望地点：')
            for spot in re.split(',|·', items[i + 1]):
                spots.append(spot)
        except (IndexError, ValueError):
            pass

        salary = -1
        try:
            i = items.index('期望月薪：')
            salaries = re.compile(r'\d+').findall(items[i + 1])
            salary = int(salaries[-1])
        except (IndexError, ValueError):
            pass

        return Objective(spots, salary, fields, industries)

    @staticmethod
    def get_person(no):
        tag = HtmlJxw.soup.find('h3', text=re.compile('个人信息'))
        if tag is None:
            return None
        tag = tag.find_parent()
        if tag['class'][0] != 'title_h3v6':
            return None

        texts = tag.find_next_sibling().getText().split('\n')
        items = []
        regex = re.compile(r'^\s*$|[：]$')       # delete lines of empty or title
        for text in texts:
            if regex.search(text) is None:
                items.append(text.strip())

        name = re.sub(r'[^\w]', '', items[0])          # remove special chars
        if not name or len(name) > 10:
            raise ValueError
        file = '{}_{:07d}_{}.html'.format(HtmlJxw.type, no, name)

        if items[1] != '男' and items[1] != '女':
            raise TypeError             # maybe english
        gender = items[1]

        try:
            regex = re.compile(r'''(
                    [a-zA-Z0-9._%+-]+      # username
                    @                      # @ symbol
                    [a-zA-Z0-9.-]+         # domain name
                    (\.[a-zA-Z]{2,4})      # dot-something
            )''', re.VERBOSE)
            email = regex.search(items[2]).group()
        except AttributeError:
            email = ''

        mo = re.compile(r'(\d{4})年(\d{1,2})月').search(items[3])
        birth = datetime(int(mo.group(1)), int(mo.group(2)), 15)

        mo = re.compile(r'\d{11}').search(items[4])
        phone = mo.group()

        try:
            mo = re.compile(r'(\d{4})').search(items[7])
            years = int(datetime.today().strftime('%Y')) - int(mo.group(1))
        except AttributeError:
            years = -1

        try:
            education = Education.educationList.index(items[8].upper()) + 1
        except (IndexError, ValueError):
            education = -1
        return Person(file, name, gender, birth, phone, email, education, years, HtmlJxw.get_objective())

    @staticmethod
    def get_experiences():
        tag = HtmlJxw.soup.find('h3', text='工作经历')
        if tag is None:
            return []
        tag = tag.find_parent()
        if tag['class'][0] != 'title_h3v6':
            return []

        experiences = []
        div = tag.find_next_sibling()
        while div is not None and div['class'][0] == 'gongzuojl':
            date1 = date2 = company = company_desc = job = job_desc = ''
            try:
                date = div.find('div', class_='gztime fl').getText()
                mo = re.compile(r'(\d{4}\.\d{2})-(\d{4}\.\d{2})').search(date)
                date1 = mo.group(1)
                date2 = mo.group(2)
            except AttributeError:
                pass

            try:
                company = div.find('div', class_='gzcomp_title').getText()
                mo = re.compile(r'(\w+)').search(company)
                company = mo.group(1)
            except AttributeError:
                pass

            try:
                for tr in div.find('table').findAll('tr'):
                    if company_desc:
                        company_desc += ', '
                    company_desc += re.sub(r'[\s]', '', tr.getText())
            except AttributeError:
                pass

            try:
                job = div.find('div', class_='wid594 fl').getText()
                mo = re.compile(r'(\w+)').search(job)
                job = mo.group(1)
            except AttributeError:
                pass

            try:
                for tr in div.find('div', class_='wid594 fl').find_parent().find('table').findAll('tr'):
                    if job_desc:
                        job_desc += ', '
                    job_desc += re.sub(r'[\s]', '', tr.getText())
            except AttributeError:
                pass

            experiences.append(Experience(date1, date2, company, company_desc, job, job_desc))
            div = div.find_next_sibling()
            if div.get('class') is None:
                div = div.find_next_sibling()

        experiences.reverse()
        return experiences

    @staticmethod
    def get_projects():
        tag = HtmlJxw.soup.find('h3', text='项目经验')
        if tag is None:
            return []
        tag = tag.find_parent()
        if tag['class'][0] != 'title_h3v6':
            return []

        projects = []
        div = tag.find_next_sibling()
        while div is not None and div['class'][0] == 'gongzuojl':
            date1 = date2 = name = description = duty = ''
            try:
                date = div.find('div', class_='gztime fl').getText()
                mo = re.compile(r'(\d{4}\.\d{2})\D*-\D*(\d{4}\.\d{2})', re.DOTALL | re.MULTILINE).search(date)
                date1 = mo.group(1)
                date2 = mo.group(2)
            except AttributeError:
                pass

            try:
                t = div.find('div', class_='gzcomp_title')
                name = t.getText()
                description = t.find_parent().find('td', text=re.compile('项目描述')).find_next_sibling().getText()
                description = re.sub(r'[\n]', '', description).strip()
            except AttributeError:
                pass

            projects.append(Project(date1, date2, name, description, duty))
            div = div.find_next_sibling()
            if div.get('class') is None:
                div = div.find_next_sibling()

        return projects

    @staticmethod
    def get_educations():
        tag = HtmlJxw.soup.find('h3', text='教育经历')
        if tag is None:
            return []
        tag = tag.find_parent()
        if tag['class'][0] != 'title_h3v6':
            return []
        tag = tag.find_next_sibling()
        if tag.name != 'table':
            return []

        educations = []
        for tr in tag.findAll('tr'):
            date1 = date2 = school = major = degree = ''
            texts = tr.getText().split('\n')
            a = []
            regex = re.compile(r'^\s*$')       # delete lines of empty
            for text in texts:
                if regex.search(text) is None:
                    a.append(text.strip())
            try:
                date1 = a[0]
                date2 = a[1]
                school = a[2]
                degree = Education.educationList.index(a[3].upper()) + 1
                major = a[4]
            except (IndexError, ValueError):
                pass

            educations.append(Education(date1, date2, school, major, degree))
        return educations

    @staticmethod
    def get_skills():
        """
        tag = HtmlJxw.soup.find('h3', text='专业技能')
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
        """
        return []

    @staticmethod
    def new_resume(html, no):
        HtmlJxw.soup = BeautifulSoup(open(html), 'lxml')
        return Resume(HtmlJxw.get_person(no), HtmlJxw.get_experiences(), HtmlJxw.get_projects(),
                      HtmlJxw.get_educations(), HtmlJxw.get_skills())


def main():
    folder = os.path.join('/home/xixisun/suzy/shoulie/resumes', HtmlJxw.type)
    # file = '000258b20ff44361831ab87ad389cc16.html'
    file = '74e547d642454e8f92022b72a5300741.html'
    resume = HtmlJxw.new_resume(os.path.join(folder, file), 2)
    pprint(resume.to_dictionary())

if __name__ == "__main__":
    main()
