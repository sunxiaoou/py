#! /usr/local/bin/python3

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
    timestamp = None

    @staticmethod
    def get_type():
        return HtmlJxw.type

    @staticmethod
    def get_timestamp(file):
        return datetime.fromtimestamp(os.path.getmtime(file))

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

        salary = ''
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
        tag = tag.find_parent().find_next_sibling()
        if tag.name != 'table':
            return None

        tds = tag.findAll('td')
        name = re.compile(r'\w+').search(tds[1].getText()).group()
        if len(name) > 10:
            raise ValueError
        file = '{}_{:07d}_{}.html'.format(HtmlJxw.type, no, name)

        gender = re.compile(r'\w+').search(tds[3].getText()).group()
        if gender != '男' and gender != '女':
            raise TypeError

        try:
            email = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}').search(tds[5].getText()).group()
        except AttributeError:
            email = ''

        mo = re.compile(r'(\d{4})年(\d{1,2})月').search(tds[7].getText())
        birth = datetime(int(mo.group(1)), int(mo.group(2)), 15)

        phone = re.compile(r'\d{11}').search(tds[10].getText()).group()

        try:
            year = int(re.compile(r'\d{4}').search(tds[16].getText()).group())
        except AttributeError:
            year = ''

        try:
            mo = re.compile(r'\w+').search(tds[18].getText())
            education = Education.educationList.index(mo.group().upper()) + 1
            mo = re.compile(r'\w+').search(tds[18].find('span').getText())
            enrollment = mo.group()
        except (AttributeError, ValueError):
            education = enrollment = ''

        return Person(file, HtmlJxw.timestamp, name, gender, birth, phone, email, education, enrollment, year,
                      HtmlJxw.get_objective())

    @staticmethod
    def str2date(s):
        mo = re.compile(r'(\d{4}).+?(\d{1,2})|至今').search(s)
        if '至今' != mo.group() and int(mo.group(1)) < HtmlJxw.timestamp.year:
            return datetime(int(mo.group(1)), int(mo.group(2)), 15)
        return HtmlJxw.timestamp

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
                mo = re.compile(r'(\d{4}\.\d{2})-(\d{4}\.\d{2})?').search(date)     # ? optional match
                date1 = HtmlJxw.str2date(mo.group(1))
                if mo.group(2) is not None:
                    date2 = HtmlJxw.str2date(mo.group(2))
                else:
                    date2 = HtmlJxw.timestamp
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
                # mo = re.compile(r'(\d{4}\.\d{2})\D*-\D*(\d{4}\.\d{2})', re.DOTALL | re.MULTILINE).search(date)
                mo = re.compile(r'(\d{4}\.\d{2})\D*-\D*(\d{4}\.\d{2})?', re.DOTALL).search(date)
                date1 = HtmlJxw.str2date(mo.group(1))
                if mo.group(2) is not None:
                    date2 = HtmlJxw.str2date(mo.group(2))
                else:
                    date2 = HtmlJxw.timestamp
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
        tag = tag.find_parent().find_next_sibling()
        if tag.name != 'table':
            return []

        educations = []
        for tr in tag.findAll('tr'):
            tds = tr.findAll('td')
            try:
                # mo = re.compile(r'(\d{4}).*(\d{4})', re.DOTALL | re.MULTILINE).search(tds[1].getText())
                mo = re.compile(r'(\d{4}\.\d{2})\D*-\D*(\d{4}\.\d{2})?', re.DOTALL).search(tds[1].getText())
                date1 = HtmlJxw.str2date(mo.group(1))
                if mo.group(2) is not None:
                    date2 = HtmlJxw.str2date(mo.group(2))
                else:
                    date2 = HtmlJxw.timestamp
                school = re.compile(r'\w+').search(tds[2].getText()).group()
                major = re.compile(r'\w+').search(tds[4].getText()).group()
                mo = re.compile(r'\w+').search(tds[3].getText())
                degree = Education.educationList.index(mo.group().upper()) + 1
            except (AttributeError, ValueError):
                continue
            educations.append(Education(date1, date2, school, major, degree))
        return educations

    @staticmethod
    def get_languages():
        tag = HtmlJxw.soup.find('h3', text='语言能力')
        if tag is None:
            return ''
        tag = tag.find_parent()
        if tag['class'][0] != 'title_h3v6':
            return ''
        tag = tag.find_next_sibling()
        if tag.name != 'table':
            return ''

        string = ''
        tds = tag.findAll('td')
        for td in tds:
            mo = re.compile(r'[^\s\n]+', re.DOTALL).search(td.getText())
            if mo is not None:
                string += mo.group() + '\n'

        return string

    @staticmethod
    def get_skills():
        tag = HtmlJxw.soup.find('h3', text='自我评价')
        if tag is None:
            return ''
        tag = tag.find_parent()
        if tag['class'][0] != 'title_h3v6':
            return ''
        tag = tag.find_next_sibling()
        if tag.name != 'table':
            return ''

        skills = []
        for skill in re.compile(r'([a-zA-Z]+)([a-zA-Z\.\d/#]*)').findall(tag.getText()):
            skills.append(skill[0].upper())     # skill is a tuple

        return list(set(skills))        # no duplicate

    @staticmethod
    def new_resume(html, no):
        HtmlJxw.soup = BeautifulSoup(open(html), 'lxml')
        HtmlJxw.timestamp = HtmlJxw.get_timestamp(html)

        person = HtmlJxw.get_person(no)
        experiences = HtmlJxw.get_experiences()
        projects = HtmlJxw.get_projects()
        educations = HtmlJxw.get_educations()
        languages = HtmlJxw.get_languages()
        skills = HtmlJxw.get_skills()

        return Resume(person, experiences, projects, educations, languages, skills)


def main():
    folder = os.path.join('/home/xixisun/suzy/shoulie/resumes', HtmlJxw.type)
    # file = 'jxw_0000225_周书婷.html'
    # file = 'jxw_0052586_于小玉.html'
    # file = 'jxw_0076028_李兴琨.html'
    # file = 'jxw_0146878_洪聪贵.html'
    file = 'jxw_0139121_李永超.html'
    resume = HtmlJxw.new_resume(os.path.join(folder, file), 2)
    pprint(resume.to_dictionary(False))

if __name__ == "__main__":
    main()
