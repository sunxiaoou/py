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
    def age2str(birth):
        if birth is None:
            return None
        today = datetime.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return str(age) + '岁'

    @staticmethod
    def spots2str(spots):
        if spots is None:
            return None
        return ','.join(spots)

    @staticmethod
    def edu2str(education):
        if education is None:
            return None
        return ['大专', '本科', '硕士', 'MBA', 'EMBA', '博士',  '博士后'][education - 1]

    @staticmethod
    def years2str(years):
        if years is None:
            return None
        return str(years) + '年'

    @staticmethod
    def edus2str(educations):
        if educations is None:
            return None
        rank = educations.get(Keys.school_rank, 1)  # if None then 1
        text = ['', '211', '985'][rank - 1]  # if None then 1
        if text:
            text = '<p>{}</p>'.format(rank)
        schools = educations.get(Keys.schools)
        majors = educations.get(Keys.majors)
        degrees = educations.get(Keys.degrees)
        for i in range(len(schools)):
            text += '<p>{}|{}|{}</p>'.format(schools[i], majors[i], degrees[i])
        return text

    @staticmethod
    def output(documents):
        head ='''<!DOCTYPE html>
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
                <td>{} {} {} {} {} {}</td>
                <td>{}</td>
                <td>75</td>
                <td>1,204 ft</td>
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
            age = Reporter.age2str(document.get(Keys.birth))
            spots = Reporter.spots2str(document.get(Keys.spots))
            education = Reporter.edu2str(document.get(Keys.education))
            years = Reporter.years2str(document.get(Keys.years))
            educations = Reporter.edus2str(document.get(Keys.educations))

            html.write(tr.format(document.get(Keys.name), document.get(Keys.gender), age, education, years, spots,
                                 educations))

        html.write(tail)
        html.close()
        webbrowser.open(output_file)


if __name__ == "__main__":
    docs = Reporter.unshelve('result.dat')
    Reporter.output(docs)
