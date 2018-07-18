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


class HtmlJL:
    type = 'jl'
    soup = None

    @staticmethod
    def get_type():
        return HtmlJL.type

    @staticmethod
    def get_year():
        text = HtmlJL.soup.body.find(text=re.compile(r'更新日期:.*'))
        return int(re.compile(r'(\d{4})-').search(text).group(1))

    @staticmethod
    def get_objective():
        fields = industries = None
        salary = -1

        spots = []
        text = HtmlJL.soup.body.find(text=re.compile(r'期望工作地点:.*'))
        if text is not None:
            text = re.compile(r'期望工作地点:(.*)$').search(text).group(1).strip()
            for spot in re.split('，|、', text):
                spots.append(spot)

        text = HtmlJL.soup.body.find(text=re.compile(r'期望月薪\(税前\):.*'))
        if text is not None:
            salaries = re.compile(r'\d+').findall(text)
            if len(salaries) > 0:
                salary = int(salaries[-1])

        text = HtmlJL.soup.body.find(text=re.compile(r'期望从事职业:.*'))
        if text is not None:
            text = re.compile(r'期望从事职业:(.*)$').search(text).group(1).strip()
            text = re.compile(r'\(.*\)').sub('', text)      # remove embedded ()
            fields = []
            for field in re.split('，|、', text):
                fields.append(field.upper())

        text = HtmlJL.soup.body.find(text=re.compile(r'期望从事行业:.*'))
        if text is not None:
            text = re.compile(r'期望从事行业:(.*)$').search(text).group(1).strip()
            text = re.compile(r'\(.*\)').sub('', text)      # remove embedded ()
            industries = []
            for industry in re.split('，|、', text):
                industries.append(industry)

        return Objective(spots, salary, fields, industries)

    @staticmethod
    def get_person(no):
        text = HtmlJL.soup.body.find(text=re.compile(r'姓名:.*'))
        name = re.compile(r'姓名:(.*)$').search(text).group(1)
        name = re.sub(r'[^\w]', '', name)          # remove special chars
        file = '{}_{:07d}_{}.html'.format(HtmlJL.type, no, name)

        text = HtmlJL.soup.body.find(text=re.compile(r'性别:.*'))
        gender = re.compile(r'性别:(.*)').search(text).group(1)

        text = HtmlJL.soup.body.find(text=re.compile(r'出生日期:.*'))
        mo = re.compile(r'出生日期:\D*(\d{4})\D*(\d{1,2})\D*(\d{1,2})?\D*').search(text)    # ? to a optional group
        if mo.group(3) is None:
            birth = datetime(int(mo.group(1)), int(mo.group(2)), 15)
        else:
            birth = datetime(int(mo.group(1)), int(mo.group(2)), int(mo.group(3)))

        text = HtmlJL.soup.body.find(text=re.compile(r'手机号码:.*'))
        phone = re.compile(r'手机号码:(.*)').search(text).group(1).strip()

        email = None
        text = HtmlJL.soup.body.find(text=re.compile(r'Email:.*'))
        mo = re.compile(r'Email:(.*)').search(text)
        if mo is not None:
            email = mo.group(1).strip()

        try:
            text = HtmlJL.soup.body.find(text=re.compile(r'学历:.*'))
            text = re.compile(r'学历:(.*)').search(text).group(1).strip()
            education = Education.educationList.index(text.upper()) + 1
        except ValueError:
            education = -1

        try:
            text = HtmlJL.soup.body.find(text=re.compile(r'工作经验:.*'))
            a = re.compile(r'\d{1,2}').findall(text)
            delta = int(a[-1])          # -1 is last one
            year = HtmlJL.get_year() - delta
        except (AttributeError, IndexError):
            year = -1

        return Person(file, name, gender, birth, phone, email, education, year, HtmlJL.get_objective())

    @staticmethod
    def get_experiences():
        text = HtmlJL.soup.body.getText()
        mo = re.compile(r'工作经历(:|：)(.*)项目经验', re.DOTALL).search(text)
        if mo is None:
            return []
        text = mo.group(2)
        texts = re.compile(r'.*?离职理由:', re.DOTALL).findall(text)    # ? = non greedy
        experiences = []
        for text in texts:
            date1 = date2 = company = company_desc = job = job_desc = ''
            for item in text.split('\n'):
                if item == '' or '离职理由' in item:
                    continue
                if '工作内容:' not in item:
                    flds = [x.strip() for x in item.split('|') if x != '']
                    try:
                        date1 = flds[0]
                        date2 = flds[1]
                        company = flds[2]
                        company_desc = flds[3]
                        company_desc += ' {}'.format(flds[4])
                    except IndexError:
                        pass
                else:
                    job_desc = item[7:]
            experiences.append(Experience(date1, date2, company, company_desc, job, job_desc))
        return experiences

    @staticmethod
    def get_projects():
        text = HtmlJL.soup.body.getText()
        mo = re.compile(r'项目经验:(.*)教育经历', re.DOTALL).search(text)
        if mo is None:
            return []
        text = mo.group(1)
        texts = re.compile(r'  \d\d\d\d.*?(?=  \d\d\d\d)', re.DOTALL).findall(text)     # ? non greed, ?= non consuming
        projects = []
        for text in texts:
            date1 = date2 = name = 'null'
            mo = re.compile(r'  \d\d\d\d.*').search(text)
            if mo is None:
                continue
            item = mo.group()
            flds = [x.strip() for x in item.split('|') if x != '']
            try:
                date1 = flds[0]
                date2 = flds[1]
                name = flds[2]
            except IndexError:
                pass
            # print('date1({}) date2({}) project_name({})'.format(date1, date2, project_name))
            mo = re.compile(r'项目介绍:\n(.*?)$', re.DOTALL | re.MULTILINE).search(text)
            if mo is None:
                continue
            description = mo.group(1).strip()
            # print(project_desc)
            mo = re.compile(r'责任描述:\n(.*?)$', re.DOTALL | re.MULTILINE).search(text)
            if mo is None:
                continue
            duty = mo.group(1).strip()
            projects.append(Project(date1, date2, name, description, duty))
        return projects

    @staticmethod
    def get_educations():
        text = HtmlJL.soup.body.getText()
        mo = re.compile(r'教育经历:(.*)语言水平', re.DOTALL).search(text)
        if mo is None:
            raise ValueError    # no educations
        educations = []
        texts = mo.group(1).split('\n')
        for text in texts:
            if re.compile('^ *$').search(text) is not None:
                continue
            text.strip()
            date1 = date2 = school = major = ''
            degree = -1
            # print(":".join("{:02x}".format(ord(c)) for c in text))
            try:
                a = re.split('&nbsp|- ', text)
                date1 = int(re.compile(r'(\d{4})').search(a[0]).group(1))
                if a[1] == '至今':
                    date2 = HtmlJL.get_year()
                else:
                    date2 = int(re.compile(r'(\d{4})').search(a[1]).group(1))
                school = a[2]
                major = a[4]
                degree = Education.educationList.index(a[5].upper()) + 1
            except (AttributeError, IndexError, ValueError):
                pass
            educations.append(Education(date1, date2, school, major, degree))
        return educations

    @staticmethod
    def get_skills():
        text = HtmlJL.soup.body.getText()
        mo = re.compile(r'技能:(.*)', re.DOTALL).search(text)
        if mo is None:
            return []

        skills = []
        texts = mo.group(1).split('\n')
        for text in texts:
            if re.compile('^ *$').search(text) is not None:
                continue
            a = [x.strip() for x in text.split('-') if x != '']
            try:
                b = re.split('&nbsp', a[1])
                if b[0] == '良好' or b[0] == '熟练' or b[0] == '精通':
                    for skill in re.split('，|、', a[0]):
                        skills.append(skill.upper())
            except IndexError:
                pass
        return skills

    @staticmethod
    def new_resume(html, no):
        HtmlJL.soup = BeautifulSoup(open(html), 'lxml')

        person = HtmlJL.get_person(no)
        experiences = HtmlJL.get_experiences()
        projects = HtmlJL.get_projects()
        educations = HtmlJL.get_educations()
        skills = HtmlJL.get_skills()

        if person.year == -1:
            end_dates = []
            for education in educations:
                end_dates.append(education.end_date)
            person.year = max(end_dates)

        if person.education == -1:
            degrees = []
            for education in educations:
                degrees.append(education.degree)
            person.education = max(degrees)

        return Resume(person, experiences, projects, educations, skills)


def main():
    folder = '/home/xixisun/suzy/shoulie/resumes/jl'
    # file = 'jl_0085242_季文清.html'
    file = 'jl_0124952_安敬辉.html'
    # file = 'jl_0000123_郝锐强.html'
    resume = HtmlJL.new_resume(os.path.join(folder, file), 1)
    pprint(resume.to_dictionary())
    # print(json.dumps(resume.to_dictionary()))

if __name__ == "__main__":
    main()
