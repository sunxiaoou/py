#! /usr/bin/python3

import os
import re
import shelve
import webbrowser
from datetime import datetime

from resume import Keys


class Reporter:
    base_folder = '/home/xixisun/suzy/shoulie/resumes'

    @staticmethod
    def unshelve(shelf_name):
        shelf = shelve.open(shelf_name)
        result = shelf['result']
        print(type(result))
        shelf.close()
        return result

    @staticmethod
    def name_html(name, file):
        html_type = re.compile(r'(\D+)\d+').search(file).group(1)
        full_file_name = os.path.join(Reporter.base_folder, html_type, file)
        return '<a href="file://{}"title="resume">{}</a><br>'.format(full_file_name, name)

    @staticmethod
    def gender_html(gender):
        if gender is None:
            return None
        return '{}<br>'.format(gender)

    @staticmethod
    def age_html(birth):
        if birth is None:
            return None
        today = datetime.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return '{}岁<br>'.format(age)

    @staticmethod
    def spots_html(spots):
        if spots is None:
            return None
        return '{}<br>'.format(','.join(spots))

    @staticmethod
    def education_html(education):
        if education is None:
            return None
        return '{}<br>'.format(['大专', '本科', '硕士', 'MBA', 'EMBA', '博士',  '博士后'][education - 1])

    @staticmethod
    def years_html(years):
        if years is None:
            return None
        return '{}年<br>'.format(years)

    @staticmethod
    def educations_html(educations):
        if educations is None:
            return None
        rank = educations.get(Keys.school_rank, 1)  # if None then 1
        text = ['', '211', '985'][rank - 1]
        if text:
            text = '<p>{}</p>'.format(rank)
        schools = educations.get(Keys.schools)
        majors = educations.get(Keys.majors)
        degrees = educations.get(Keys.degrees)
        for i in range(len(schools)):
            text += '{}|{}|{}<br>'.format(schools[i], majors[i], degrees[i])
        return text

    @staticmethod
    def experiences_html(experiences):
        if experiences is None:
            return None
        a = experiences[0]
        text = '{} | {} | {} | {}<br>'.format(a.get(Keys.start_date), a.get(Keys.end_date), a.get(Keys.company),
                                              a.get(Keys.company_desc))
        text += '{}<br>'.format(a.get(Keys.job_desc))
        return text if len(text) <= 100 else text[:150] + '...'

    @staticmethod
    def projects_html(projects):
        if projects is None:
            return None
        a = projects[0]
        text = '{} | {} | {}<br>'.format(a.get(Keys.start_date), a.get(Keys.end_date), a.get(Keys.project))
        text += '{}<br>'.format(a.get(Keys.project_desc))
        text += '{}<br>'.format(a.get(Keys.duty))
        return text if len(text) <= 100 else text[:150] + '...'

    @staticmethod
    def output(documents, file):
        head = '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <style type="text/css">td, th {{ border: 1px solid black; }}</style>
        <title>Found {}, show {}</title>
    </head>
    <body>
        <table>
            <tr>
                <th>基本信息</th>
                <th>教育经历</th>
                <th>工作经历</th>
                <th>项目经历</th>
            </tr>'''

        tr = '''
            <tr>
                <td>{}{}{}{}{}{}{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>'''

        tail = '''
        </table>
    </body>
</html>
'''

        html = open(file, 'w')
        num = len(documents)
        show_num = min(100, len(documents))
        html.write(head.format(num, show_num))

        for i in range(show_num):
            document = documents[i]
            no = '{:02d}<br>'.format(i)
            name = Reporter.name_html(document.get(Keys.name), document.get(Keys.file))
            gender = Reporter.gender_html(document.get(Keys.gender))
            age = Reporter.age_html(document.get(Keys.birth))
            spots = Reporter.spots_html(document.get(Keys.spots))
            education = Reporter.education_html(document.get(Keys.education))
            years = Reporter.years_html(document.get(Keys.years))
            educations = Reporter.educations_html(document.get(Keys.educations))
            experiences = Reporter.experiences_html(document.get(Keys.experiences))
            projects = Reporter.projects_html(document.get(Keys.projects))
            html.write(tr.format(no, name, gender, age, education, years, spots, educations, experiences, projects))

        html.write(tail)
        html.close()


if __name__ == "__main__":
    docs = Reporter.unshelve('result.dat')
    output = 'result.html'
    Reporter.output(docs, output)
    webbrowser.open('file://{}/{}'.format(os.getcwd(), output))
