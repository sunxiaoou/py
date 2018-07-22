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


class HtmlJ51:
    type = 'j51'
    soup = None
    skills = []

    @staticmethod
    def get_type():
        return HtmlJ51.type

    @staticmethod
    def get_year():
        tag = HtmlJ51.soup.body.find(id='lblResumeUpdateTime')
        return int(re.compile(r'\d{4}').search(tag.getText()).group())

    @staticmethod
    def get_objective():
        tag = HtmlJ51.soup.find('td', text='求职意向').find_next('table')
        if tag is None:
            return None

        tds = tag.findAll('td')

        industries = []
        try:
            for industry in re.split('，', tds[2].find('span').getText()):
                industries.append(industry)
        except (IndexError, ValueError):
            pass

        fields = []
        try:
            for field in re.split('，', tds[5].find('span').getText()):
                fields.append(field.upper())
        except (IndexError, ValueError):
            pass

        spots = []
        try:
            for spot in re.split('，', tds[3].find('span').getText()):
                spots.append(spot)
        except (IndexError, ValueError):
            pass

        salary = -1
        try:
            salaries = re.compile(r'\d+').findall(tds[4].find('span').getText())
            salary = int(salaries[-1])
        except (IndexError, ValueError):
            pass

        return Objective(spots, salary, fields, industries)

    @staticmethod
    def get_person(no):
        tag = HtmlJ51.soup.find(id='spanProcessStatusHead').find_next_sibling()
        if tag is None:
            return None

        name = re.compile(r'\w+').search(tag.getText()).group()
        if len(name) > 10:
            raise ValueError
        file = '{}_{:07d}_{}.html'.format(HtmlJ51.type, no, name)

        tag = tag.find_parent().find_parent().find_next_sibling()
        if tag is None or tag.name != 'tr':
            return None

        tds = tag.findAll('td')
        mo = re.compile(r'(\d{1,2})年工作经验.*(男|女).*(\d{4})年(\d{1,2})月', re.DOTALL).search(tds[1].getText())
        try:
            year = HtmlJ51.get_year() - int(mo.group(1))
        except AttributeError:
            year = -1
        gender = mo.group(2)
        birth = datetime(int(mo.group(3)), int(mo.group(4)), 15)
        phone = re.compile(r'\d{11}').search(tds[8].getText()).group()

        try:
            email = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}').search(tds[10].getText()).group()
        except AttributeError:
            email = ''

        try:
            tag = HtmlJ51.soup.find(text='最高学历').find_next('td').find_next('td')
            education = Education.educationList.index(tag.getText().upper()) + 1
        except (AttributeError, ValueError):
            education = -1

        return Person(file, name, gender, birth, phone, email, education, year, HtmlJ51.get_objective())

    @staticmethod
    def get_experiences():
        tag = HtmlJ51.soup.find('td', text='工作经验').find_next('table')
        if tag is None:
            return []

        tds = tag.findAll('td')

        experiences = []
        j = 0
        date1 = date2 = company = company_desc = job = job_desc = ''
        for i in range(len(tds)):
            if j == 0:
                mo = re.compile(r'(\d{4}.*/\d{1,2}).*(\d{4}.*/\d{1,2}|至今)：(\w+)', re.DOTALL).\
                    search(tds[i].getText())
                date1 = mo.group(1)
                date1 = re.sub(r'[\s\n]', '', date1)
                date2 = mo.group(2)
                if date2 != '至今':
                    date2 = re.sub(r'[\s\n]', '', date2)
                company = mo.group(3)
            elif j == 2:
                company_desc = tds[i].getText()
            elif j == 4:
                job = tds[i].getText()
            elif j == 5:
                job_desc = tds[i].getText()
                experiences.append(Experience(date1, date2, company, company_desc, job, job_desc))
                date1 = date2 = company = company_desc = job = job_desc = ''
            elif j > 5:
                if not tds[i].getText():
                    j = -1      # to zero
            j += 1

        return experiences

    @staticmethod
    def get_projects():
        tag = HtmlJ51.soup.find('td', text='项目经验').find_next('table')
        if tag is None:
            return []

        tds = tag.findAll('td')

        projects = []
        j = 0
        date1 = date2 = name = description = duty = ''
        for i in range(len(tds)):
            if j == 0:
                mo = re.compile(r'(\d{4}.*/\d{1,2}).*(\d{4}.*/\d{1,2}|至今)：\W*(\w+)', re.DOTALL). \
                    search(tds[i].getText())
                date1 = mo.group(1)
                date1 = re.sub(r'[\s\n]', '', date1)
                date2 = mo.group(2)
                if date2 != '至今':
                    date2 = re.sub(r'[\s\n]', '', date2)
                name = mo.group(3)
            elif j == 1:
                if tds[i].getText() == '项目描述：':
                    j += 2
            elif j == 2:
                HtmlJ51.skills.append(tds[i].getText())
            elif j == 4:
                description = tds[i].getText()
            elif j == 6:
                duty = tds[i].getText()
                projects.append(Project(date1, date2, name, description, duty))
                date1 = date2 = name = description = duty = ''
            elif j > 6:
                if not tds[i].getText():
                    j = -1      # to zero
            j += 1

        return projects

    @staticmethod
    def get_educations():
        tag = HtmlJ51.soup.find('td', text='教育经历').find_next('table')
        if tag is None:
            return []

        tds = tag.findAll('td')

        educations = []
        j = 0
        date1 = date2 = school = major = degree = ''
        for i in range(len(tds)):
            if j == 0:
                mo = re.compile(r'(\d{4}.*/\d{1,2}).*(\d{4}.*/\d{1,2}|至今)', re.DOTALL).search(tds[i].getText())
                date1 = mo.group(1)
                date1 = re.sub(r'[\s\n]', '', date1)
                date2 = mo.group(2)
                if date2 != '至今':
                    date2 = re.sub(r'[\s\n]', '', date2)
            elif j == 1:
                school = tds[i].getText()
            elif j == 2:
                major = tds[i].getText()
            elif j == 3:
                degree = tds[i].getText()
                educations.append(Education(date1, date2, school, major, degree))
                date1 = date2 = school = major = degree = ''
            elif j > 3:
                if not tds[i].getText():
                    j = -1      # to zero
            j += 1

        return educations

    @staticmethod
    def get_skills():
        skills = []
        for skill in HtmlJ51.skills:
            skills += re.split(r',', skill.upper())     # merge 2 lists

        return list(set(skills))        # no duplicate

    @staticmethod
    def new_resume(html, no):
        HtmlJ51.soup = BeautifulSoup(open(html), 'lxml')

        person = HtmlJ51.get_person(no)
        experiences = HtmlJ51.get_experiences()
        projects = HtmlJ51.get_projects()
        educations = HtmlJ51.get_educations()
        skills = HtmlJ51.get_skills()

        if person.year == -1:
            end_dates = []
            if educations:
                for education in educations:
                    end_dates.append(education.end_date)
                person.year = max(end_dates)
            else:
                person.year = 2015

        if person.education == -1:
            degrees = []
            if educations:
                for education in educations:
                    degrees.append(education.degree)
                person.education = max(degrees)
            else:
                person.education = 0

        return Resume(person, experiences, projects, educations, skills)


def main():
    folder = os.path.join('/home/xixisun/suzy/shoulie/resumes', HtmlJ51.type)
    file = '16486510.html'
    resume = HtmlJ51.new_resume(os.path.join(folder, file), 4)
    pprint(resume.to_dictionary(False))

if __name__ == "__main__":
    main()
