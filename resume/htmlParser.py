#! /usr/bin/python3

import re
import os
from abcParser import ABCParser
from resume import Person
from resume import Objective
from resume import Experience
from resume import Education


class HtmlParser(ABCParser):
    """
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(open(html), 'lxml')
    """

    def get_person(self):
        gender = birth = email = 'null'

        file = os.path.basename(self.html)

        # elements = self.soup.select('#userName')
        elements = self.soup.select('.resume-preview-main-title [class$=fc6699cc]')
        name = elements[0].getText().strip()

        elements = self.soup.select('.summary-top')
        mo = re.compile(r'男|女').search(elements[0].getText())
        if mo is not None:
            gender = mo.group()

        elements = self.soup.select('.summary-top')
        mo = re.compile(r'\d{4}年\d{1,2}月').search(elements[0].getText())
        if mo is not None:
            birth = mo.group()

        elements = self.soup.select('.summary-bottom')
        mo = re.compile(r'\D(\d{11})\D').search(elements[0].getText())
        if mo is not None:
            phone = mo.group(1)
        else:
            raise Exception('Cannot find phone')

        regex = re.compile(r'''(
                [a-zA-Z0-9._%+-]+      # username
                @                      # @ symbol
                [a-zA-Z0-9.-]+         # domain name
                (\.[a-zA-Z]{2,4})      # dot-something
        )''', re.VERBOSE)
        mo = regex.search(elements[0].getText())
        if mo is not None:
            email = mo.group()

        return Person(file, name, gender, birth, phone, email, self.get_objective())

    def get_objective(self):
        spot = field = industry = 'null'
        salary = '-1'
        elements = self.soup.select('.resume-preview-top')
        texts = elements[0].getText().strip().split('\n')
        items = []
        regex = re.compile(r'^$|[：]$')
        for text in texts:
            if regex.search(text) is None:
                items.append(text)
        try:
            spot = items[0]
            salaries = re.compile(r'\d+').findall(items[1])
            salary = salaries[len(salaries) - 1]
            field = items[4]
            industry = items[5]
        except IndexError:
            pass
        return Objective(spot, salary, field, industry)

    def get_experiences(self):
        experiences = []
        # tag = self.soup.find('div', class_='resume-preview-all workExperience')
        tag = self.soup.find('h3', text=re.compile(r'工作经历|项目经历'))
        if tag is None:
            return experiences
        tag = tag.find_parent()
        if not tag['class'][0].startswith('resume-preview-all'):
            return experiences

        for h2 in tag.findAll('h2'):
            text = h2.getText().strip()
            date1 = date2 = company = company_desc = job = job_desc = 'null'
            mo = re.compile(r'\d{4}\D\d{1,2}\D').search(text)
            if mo is not None:
                date1 = mo.group().strip()
                text = text.replace(date1, '')
            mo = re.compile(r'\d{4}\D\d{1,2}\D|至今').search(text)
            if mo is not None:
                date2 = mo.group().strip()
                text = text.replace(date2, '')
            # mo = re.compile(r'\S*(公司)\S*').search(text)
            mo = re.compile(r'[^-\s]+').search(text)
            if mo is not None:
                company = mo.group()
            sibling = h2.find_next_sibling()
            while sibling is not None and sibling.name != 'h2':
                if sibling.name == 'h5':
                    # jobs = '(生|员|工|师|代|理|总|监|书|顾|计)'
                    # mo = re.compile(r'\S*{0}\S*'.format(jobs)).search(sibling.getText())
                    # if mo is not None:
                    #    job = mo.group()
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

    def get_educations(self):
        educations = []
        element = self.soup.find('div', class_='resume-preview-dl educationContent')
        if element is None:
            element = self.soup.find('h3', text='教育经历')
            if element is None:
                return educations
            element = element.find_next_sibling()
        text = element.getText().strip()
        texts = text.split('\n')
        for text in texts:
            date1 = date2 = school = major = degree = 'null'
            mo = re.compile(r'(\d{4}\D\d{1,2}\D)').search(text)
            if mo is not None:
                date1 = mo.group().strip()
                text = text.replace(date1, '')
            mo = re.compile(r'(\d{4}\D\d{1,2}\D)').search(text)
            if mo is not None:
                date2 = mo.group().strip()
                text = text.replace(date2, '')
            mo = re.compile(r'\S*(大学|学院)').search(text)
            if mo is not None:
                school = mo.group()
                text = text.replace(school, '')
            majors = '(科学|语|数|理|化|光|机|电|计|通|仪|材料|应用|工程)'
            mo = re.compile(r'\S*{0}\S*'.format(majors)).search(text)
            if mo is not None:
                major = mo.group()
                text = text.replace(major, '')
            mo = re.compile(r'\S*(专|本|生|士)\S*').search(text)
            if mo is not None:
                degree = mo.group()
            educations.append(Education(date1, date2, school, major, degree))
        return educations

    """
    def new_resume(self):
        return Resume(self.get_person(), self.get_experiences(), self.get_educations())
    """
