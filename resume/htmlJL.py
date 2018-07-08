#! /usr/bin/python3

import re
import os
from datetime import datetime
from pprint import pprint
from abcParser import ABCParser
from resume import Person
from resume import Objective
from resume import Experience
from resume import Project
from resume import Education
from resume import Skills


class HtmlJL(ABCParser):

    def get_person(self):
        file = os.path.basename(self.html)

        try:
            text = self.soup.body.find(text=re.compile(r'姓名:.*'))
            name = re.compile(r'姓名:(.*)$').search(text).group(1)
            text = self.soup.body.find(text=re.compile(r'性别:.*'))
            gender = re.compile(r'性别:(.*)').search(text).group(1)
            text = self.soup.body.find(text=re.compile(r'出生日期:.*'))
            # birth = re.compile(r'出生日期:(.*)').search(text).group(1).strip()
            mo = re.compile(r'出生日期:\D*(\d{4})\D*(\d{1,2})\D*(\d{1,2})?\D*').search(text)    # ? to a optional group
            if mo.group(3) is None:
                birth = datetime(int(mo.group(1)), int(mo.group(2)), 15)
            else:
                birth = datetime(int(mo.group(1)), int(mo.group(2)), int(mo.group(3)))
            text = self.soup.body.find(text=re.compile(r'手机号码:.*'))
            phone = re.compile(r'手机号码:(.*)').search(text).group(1).strip()

            email = None
            text = self.soup.body.find(text=re.compile(r'Email:.*'))
            mo = re.compile(r'Email:(.*)').search(text)
            if mo is not None:
                email = mo.group(1).strip()

            text = self.soup.body.find(text=re.compile(r'学历:.*'))
            text = re.compile(r'学历:(.*)').search(text).group(1).strip()
            education = ['大专', '本科', '硕士', 'MBA', 'EMBA', '博士',  '博士后'].index(text.upper()) + 1

            text = self.soup.body.find(text=re.compile(r'工作经验:.*'))
            a = re.compile(r'\d{1,2}').findall(text)
            years = int(a[-1])          # -1 is last one
        except (TypeError, AttributeError) as err:
            raise err

        return Person(file, name, gender, birth, phone, email, education, years, self.get_objective())

    def get_objective(self):
        fields = industries = None
        salary = -1

        spots = []
        text = self.soup.body.find(text=re.compile(r'期望工作地点:.*'))
        if text is not None:
            text = re.compile(r'期望工作地点:(.*)$').search(text).group(1).strip()
            for spot in re.split('，|、', text):
                spots.append(spot)

        text = self.soup.body.find(text=re.compile(r'期望月薪\(税前\):.*'))
        if text is not None:
            salaries = re.compile(r'\d+').findall(text)
            if len(salaries) > 0:
                salary = int(salaries[-1])

        text = self.soup.body.find(text=re.compile(r'期望从事职业:.*'))
        if text is not None:
            text = re.compile(r'期望从事职业:(.*)$').search(text).group(1).strip()
            text = re.compile(r'\(.*\)').sub('', text)      # remove embedded ()
            fields = []
            for field in re.split('，|、', text):
                fields.append(field.upper())

        text = self.soup.body.find(text=re.compile(r'期望从事行业:.*'))
        if text is not None:
            text = re.compile(r'期望从事行业:(.*)$').search(text).group(1).strip()
            text = re.compile(r'\(.*\)').sub('', text)      # remove embedded ()
            industries = []
            for industry in re.split('，|、', text):
                industries.append(industry)

        return Objective(spots, salary, fields, industries)

    def get_experiences(self):
        text = self.soup.body.getText()
        mo = re.compile(r'工作经历(:|：)(.*)项目经验', re.DOTALL).search(text)
        if mo is None:
            return []
        text = mo.group(2)
        texts = re.compile(r'.*?离职理由:', re.DOTALL).findall(text)    # ? = non greedy
        experiences = []
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

    def get_projects(self):
        text = self.soup.body.getText()
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

    def get_educations(self):
        text = self.soup.body.getText()
        mo = re.compile(r'教育经历:(.*)语言水平', re.DOTALL).search(text)
        if mo is None:
            return []
        educations = []
        texts = mo.group(1).split('\n')
        for text in texts:
            if re.compile('^ *$').search(text) is not None:
                continue
            text.strip()
            date1 = date2 = school = major = degree = ''
            # print(":".join("{:02x}".format(ord(c)) for c in text))
            try:
                a = re.split('&nbsp|- ', text)
                date1 = a[0]
                date2 = a[1]
                school = a[2]
                major = a[4]
                degree = a[5]
            except IndexError:
                pass
            educations.append(Education(date1, date2, school, major, degree))
        return educations

    def get_skills(self):
        text = self.soup.body.getText()
        mo = re.compile(r'技能:(.*)', re.DOTALL).search(text)
        if mo is None:
            return None
        texts = mo.group(1).split('\n')
        level1 = []
        level2 = []
        level3 = []
        for text in texts:
            if re.compile('^ *$').search(text) is not None:
                continue
            a = [x.strip() for x in text.split('-') if x != '']
            try:
                b = re.split('&nbsp', a[1])
                if b[0] == '一般':
                    for skill in re.split('，|、', a[0]):
                        level1.append(skill.upper())
                elif b[0] == '熟练':
                    for skill in re.split('，|、', a[0]):
                        level2.append(skill.upper())
                elif b[0] == '精通':
                    for skill in re.split('，|、', a[0]):
                        level3.append(skill.upper())
            except IndexError:
                pass
        # Ignore level1
        if not level2 and not level3:
            return None
        return Skills(None, level2 if level2 else None, level3 if level3 else None)


def main():
    folder = '/home/xixisun/suzy/shoulie/resumes/jl'
    # file = '10022353-季文清.html'
    file = '10052356-安敬辉.html'
    # file = 'jm329830852r90250000000-朱昭卿.html'
    # file = 'jm615458412r90250000000-曾德阳.html'
    # file = 'jm375383835r90250000000-姜丽婷.html'
    parser = HtmlJL(folder + '/' + file)
    resume = parser.new_resume()
    pprint(resume.to_dictionary())
    # print(json.dumps(resume.to_dictionary()))

if __name__ == "__main__":
    main()
