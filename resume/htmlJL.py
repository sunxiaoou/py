#! /usr/bin/python3

import re
import os
from abcParser import ABCParser
from resume import Person
from resume import Objective
from resume import Experience
from resume import Education


class HtmlJL(ABCParser):

    """
    def __init__(self, html):
        super(HtmlJL, self).__init__(html)
        # text = self.soup.body.find(text=re.compile(r'工作经历(:|：).*', re.DOTALL))
        text = self.soup.body.getText()
        mo = re.compile(r'工作经历(:|：)(.*)项目经验', re.DOTALL).search(text)
        text = mo.group(2)
        texts = re.compile(r'.*离职理由', re.DOTALL).findall(text)
        for text in texts:
            # i = 0
            for item in text.split('\n'):
                if item != '' and '离职理由' not in item:
                    if '工作内容:' not in item:
                        flds = [x for x in item.split('|') if x != '']
                        print('{} {}'.format(flds, len(flds)))
                    else:
                        print(item[7:])
    """

    def get_person(self):
        file = os.path.basename(self.html)
        gender = birth = email = 'null'

        text = self.soup.body.find(text=re.compile(r'姓名:.*'))
        if text is not None:
            name = re.compile(r'姓名:(.*)$').search(text).group(1)
        else:
            raise Exception('Cannot find name')

        text = self.soup.body.find(text=re.compile(r'性别:.*'))
        if text is not None:
            mo = re.compile(r'性别:(.*)').search(text)
            gender = mo.group(1)

        text = self.soup.body.find(text=re.compile(r'出生日期:.*'))
        if text is not None:
            birth = re.compile(r'出生日期:(.*)').search(text).group(1).strip()

        text = self.soup.body.find(text=re.compile(r'手机号码:.*'))
        if text is not None:
            phone = re.compile(r'手机号码:(.*)').search(text).group(1).strip()
        else:
            raise Exception('Cannot find phone')

        text = self.soup.body.find(text=re.compile(r'Email:.*'))
        if text is not None:
            email = re.compile(r'Email:(.*)').search(text).group(1).strip()

        return Person(file, name, gender, birth, phone, email, self.get_objective())

    def get_objective(self):
        spot = field = industry = 'null'
        salary = '-1'

        text = self.soup.body.find(text=re.compile(r'期望工作地点:.*'))
        if text is not None:
            spot = re.compile(r'期望工作地点:(.*)$').search(text).group(1).strip()

        text = self.soup.body.find(text=re.compile(r'期望月薪\(税前\):.*'))
        if text is not None:
            salaries = re.compile(r'\d+').findall(text)
            salary = salaries[len(salaries) - 1]

        text = self.soup.body.find(text=re.compile(r'期望从事职业:.*'))
        if text is not None:
            field = re.compile(r'期望从事职业:(.*)$').search(text).group(1).strip()

        text = self.soup.body.find(text=re.compile(r'期望从事行业:.*'))
        if text is not None:
            industry = re.compile(r'期望从事行业:(.*)$').search(text).group(1).strip()

        return Objective(spot, salary, field, industry)

    def get_experiences(self):
        experiences = []
        text = self.soup.body.getText()
        mo = re.compile(r'工作经历(:|：)(.*)项目经验', re.DOTALL).search(text)
        text = mo.group(2)
        texts = re.compile(r'.*?离职理由:', re.DOTALL).findall(text)    # ? = non greedy
        for text in texts:
            date1 = date2 = company = company_desc = job = job_desc = 'null'
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

    def get_educations(self):
        educations = []
        text = self.soup.body.getText()
        mo = re.compile(r'教育经历:(.*)语言水平', re.DOTALL).search(text)
        texts = mo.group(1).split('\n')
        for text in texts:
            text.strip()
            if text == '' or text == ' ':
                continue
            # print(":".join("{:02x}".format(ord(c)) for c in text))
            date1 = date2 = school = major = degree = 'null'
            mo = re.compile(r'(\d{4}\D+\d{1,2})').search(text)
            if mo is not None:
                date1 = mo.group().strip()
                text = text.replace(date1, '')
            mo = re.compile(r'(\d{4}\D+\d{1,2})').search(text)
            if mo is not None:
                date2 = mo.group().strip()
                text = text.replace(date2, '')
            mo = re.compile(r'&nbsp(\S*(大学|学院))').search(text)
            if mo is not None:
                school = mo.group(1)
                text = text.replace(school, '')
            majors = '(科学|语|数|理|化|光|机|电|计|通|仪|材料|应用|工程)'
            mo = re.compile(r'(&nbsp)+(\S*{0}\S*)&nbsp'.format(majors)).search(text)
            if mo is not None:
                major = mo.group(2)
                text = text.replace(major, '')
            mo = re.compile(r'(&nbsp)+(\S*(专|本|生|士)\S*)').search(text)
            if mo is not None:
                degree = mo.group(2)
            educations.append(Education(date1, date2, school, major, degree))
        return educations


folder = '/home/xixisun/suzy/resumes/html/jl'
# file = '10022353-季文清.html'
file = '10052356-安敬辉.html'
parser = HtmlJL(folder + '/' + file)
print(parser.get_person())
for experience in parser.get_experiences():
    print(experience)
for education in parser.get_educations():
    print(education)
