#! /usr/bin/python3

import shelve
import webbrowser
from datetime import datetime

from resume import Keys


class Reporter:

    @staticmethod
    def unshelve(shelf_name):
        shelf = shelve.open(shelf_name)
        result = shelf['result']
        print(type(result))
        shelf.close()
        return result

    @staticmethod
    def str2p(str):
        if str is None:
            return None
        return '<p>{}</p>'.format(str)

    @staticmethod
    def age2p(birth):
        if birth is None:
            return None
        today = datetime.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return '<p>{}岁</p>'.format(age)

    @staticmethod
    def spots2p(spots):
        if spots is None:
            return None
        return '<p>{}</p>'.format(','.join(spots))

    @staticmethod
    def education2p(education):
        if education is None:
            return None
        return '<p>{}</p>'.format(['大专', '本科', '硕士', 'MBA', 'EMBA', '博士',  '博士后'][education - 1])

    @staticmethod
    def years2p(years):
        if years is None:
            return None
        return '<p>{}年</p>'.format(years)

    @staticmethod
    def educations2p(educations):
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
            text += '<p>{}|{}|{}</p>'.format(schools[i], majors[i], degrees[i])
        return text

    @staticmethod
    def experiences2p(experiences):
        if experiences is None:
            return None
        a = experiences[0]
        text = '<p>{} | {} | {} | {}</p>'.format(a.get(Keys.start_date), a.get(Keys.end_date), a.get(Keys.company),
                                                 a.get(Keys.company_desc))
        text += '<p>{}</p>'.format(a.get(Keys.job_desc))
        return text if len(text) <= 100 else text[:100] + '...'

    @staticmethod
    def projects2p(projects):
        if projects is None:
            return None
        a = projects[0]
        text = '<p>{} | {} | {}</p>'.format(a.get(Keys.start_date), a.get(Keys.end_date), a.get(Keys.project))
        text += '<p>{}</p>'.format(a.get(Keys.project_desc))
        text += '<p>{}</p>'.format(a.get(Keys.duty))
        return text if len(text) <= 100 else text[:150] + '...'

    @staticmethod
    def output(documents):
        head = '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <style type="text/css">td, th { border: 1px solid black; }</style>
        <title>Testing Tony's Travels</title>
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
                <td>{}{}{}{}{}{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>'''

        tail = '''
        </table>
    </body>
</html>
'''

        output_file = 'result.html'
        html = open(output_file, 'w')
        html.write(head)

        for document in documents:
            name = Reporter.str2p(document.get(Keys.name))
            gender = Reporter.str2p(document.get(Keys.gender))
            age = Reporter.age2p(document.get(Keys.birth))
            spots = Reporter.spots2p(document.get(Keys.spots))
            education = Reporter.education2p(document.get(Keys.education))
            years = Reporter.years2p(document.get(Keys.years))
            educations = Reporter.educations2p(document.get(Keys.educations))
            experiences = Reporter.experiences2p(document.get(Keys.experiences))
            projects = Reporter.projects2p(document.get(Keys.projects))
            html.write(tr.format(name, gender, age, education, years, spots, educations, experiences, projects))

        html.write(tail)
        html.close()
        webbrowser.open(output_file)


if __name__ == "__main__":
    docs = Reporter.unshelve('result.dat')
    Reporter.output(docs)
