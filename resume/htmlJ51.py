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
        tag = HtmlJ51.soup.find('h3', text='工作经历')
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
        tag = HtmlJ51.soup.find('h3', text='项目经验')
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
        tag = HtmlJ51.soup.find('h3', text='教育经历')
        if tag is None:
            return []
        tag = tag.find_parent().find_next_sibling()
        if tag.name != 'table':
            return []

        educations = []
        for tr in tag.findAll('tr'):
            tds = tr.findAll('td')
            try:
                mo = re.compile(r'(\d{4}).*(\d{4})', re.DOTALL | re.MULTILINE).search(tds[1].getText())
                date1 = int(mo.group(1))
                date2 = int(mo.group(2))
                school = re.compile(r'\w+').search(tds[2].getText()).group()
                major = re.compile(r'\w+').search(tds[4].getText()).group()
                mo = re.compile(r'\w+').search(tds[3].getText())
                degree = Education.educationList.index(mo.group().upper()) + 1
            except (AttributeError, ValueError):
                continue
            educations.append(Education(date1, date2, school, major, degree))
        return educations

    @staticmethod
    def get_skills():
        tag = HtmlJ51.soup.find('h3', text='自我评价')
        if tag is None:
            return None
        tag = tag.find_parent()
        if tag['class'][0] != 'title_h3v6':
            return None
        tag = tag.find_next_sibling()
        if tag.name != 'table':
            return []

        skills = []
        for skill in re.compile(r'([a-zA-Z]+)([a-zA-Z\.\d/#]*)').findall(tag.getText()):
            skills.append(skill[0].upper())     # skill is a tuple

        return list(set(skills))        # no duplicate

    @staticmethod
    def new_resume(html, no):
        HtmlJ51.soup = BeautifulSoup(open(html), 'lxml')

        person = HtmlJ51.get_person(no)
        experiences = []
        projects = []
        educations = []
        skills = []

        """
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
        """

        return Resume(person, experiences, projects, educations, skills)


def main():
    folder = os.path.join('/home/xixisun/suzy/shoulie/resumes', HtmlJ51.type)
    file = '16486510.html'
    resume = HtmlJ51.new_resume(os.path.join(folder, file), 4)
    pprint(resume.to_dictionary())

if __name__ == "__main__":
    main()
