#! /usr/bin/python3

import sys
from datetime import datetime
from pprint import pprint
from resume import Keys


class Condition:
    file = 'file'
    name = 'name'
    spot = 'spot'
    industry = 'industry'
    field = 'field'
    age1 = 'age1'
    age2 = 'age2'
    skills = 'skills'

    education2 = 'education2'
    education1 = 'education1'
    school_rank = 'school_rank'
    school = 'school'
    major = 'major'

    year1 = 'year1'
    year2 = 'year2'
    duration1 = 'duration1'
    duration2 = 'duration2'
    company = 'company'
    experience_keys = 'experience_keys'
    ek_flag = 'ek_flag'
    project_keys = 'project_keys'
    pk_flag = 'pk_flag'

    @staticmethod
    def input_string(title):
        print('请输入' + title + ':')
        s = input()
        # return s if str else None
        return s

    @staticmethod
    def input_number(title):
        while True:
            print('请输入' + title + ':')
            num = input()
            if not num:
                return ''
            if num.isdecimal():
                return int(num)
            print('请输入数字')

    @staticmethod
    def interrupt():
        print('Input "y" to exit, any others to continue:')
        flag = input()
        if flag == 'y' or flag == 'Y':
            sys.exit(0)

    @staticmethod
    def input():
        entries = {}
        try:
            print('基本信息:')
            entries[Condition.name] = Condition.input_string('姓名')
            entries[Condition.spot] = Condition.input_string('期望地点')
            entries[Condition.industry] = Condition.input_string('期望行业(关键字)')
            entries[Condition.field] = Condition.input_string('期望职业(关键字)')
            entries[Condition.age1] = ''
            # Condition.input_number('年龄_岁及以上')
            entries[Condition.age2] = Condition.input_number('年龄_岁以下')
            skills = []
            for i in range(3):
                skill = Condition.input_string('技能-' + str(i + 1))
                if not skill:
                    break
                skills.append(skill)
            entries[Condition.skills] = ', '.join(skills)

            print('教育背景:')
            entries[Condition.school_rank] = Condition.input_number('学校类别(1:一般 2:211 3:985)及以上')
            entries[Condition.education1] =\
                Condition.input_number('学历(1:大专 2:本科 3:硕士 4:MBA 5:EMBA 6:博士 7:博士后)及以上')
            entries[Condition.education2] = ''
            # Condition.input_number('学历(1:大专 2:本科 3:硕士 4:MBA 5:EMBA 6:博士 7:博士后)以下')
            entries[Condition.school] = Condition.input_string('学校(关键字)')
            entries[Condition.major] = Condition.input_string('专业(关键字)')

            print('职业背景:')
            entries[Condition.year1] = Condition.input_number('工作经验_年及以上')
            entries[Condition.year2] = ''
            # Condition.input_number('工作经验_年以下')
            entries[Condition.company] = Condition.input_string('(前)雇主(关键字)')
            entries[Condition.experience_keys] = Condition.input_string('工作经历(关键字)')
            entries[Condition.project_keys] = Condition.input_string('项目经历(关键字)')
        except KeyboardInterrupt:
            Condition.interrupt()
        return entries

    """
    @staticmethod
    def __str__():
        return Condition.spot + ', ' + Condition.industry + ', ' + Condition.field + ', ' + Condition.major + ', ' +\
               Condition.school_rank + '\n' + Condition.education1 + '-' + Condition.education2 + ', ' +\
               Condition.year1 + '-' + Condition.year2 + ', ' + Condition.age1 + '-' + Condition.age2
    """

    @staticmethod
    def range_int(num1, num2):
        if not num1 and not num2:
            return ''

        if num1 and num1 == num2:
            return num1

        conditions = {}
        if num1:
            conditions['$gte'] = num1
        if num2:
            conditions['$lt'] = num2
        return conditions

    @staticmethod
    def range_year(num1, num2):
        if not num1 and not num2:
            return ''

        this_year = int(datetime.today().strftime('%Y'))
        if num1 and num1 == num2:
            return this_year - num1

        conditions = {}
        if num2:
            conditions['$gte'] = this_year - num2
        if num1:
            conditions['$lt'] = this_year - num1
        return conditions

    @staticmethod
    def range_date(num1, num2):
        if not num1 and not num2:
            return ''

        today = datetime.today()
        if num1 and num1 == num2:
            return datetime(today.year - num1, today.month, today.day)

        conditions = {}
        if num2:
            conditions['$gte'] = datetime(today.year - num2, today.month, today.day)    # >= birth equals <= age
        if num1:
            conditions['$lt'] = datetime(today.year - num1, today.month, today.day)     # < birth equals > age
        return conditions

    @staticmethod
    def create_conditions(entries):
        conditions = {}

        file = entries.get(Condition.file)
        if file:
            conditions[Keys.file] = file

        # basic information
        name = entries.get(Condition.name)
        if name:
            conditions[Keys.name] = name

        spot = entries.get(Condition.spot)
        if spot:
            conditions[Keys.spots] = spot

        industry = entries.get(Condition.industry)
        if industry:
            conditions[Keys.industries] = {'$regex': industry}

        field = entries.get(Condition.field)
        if field:
            conditions[Keys.fields] = {'$regex': field}

        c = Condition.range_date(entries.get(Condition.age1), entries.get(Condition.age2))
        if c:
            conditions[Keys.birth] = c

        skills = entries.get(Condition.skills)
        if skills:
            """
            conditions['$or'] = [{Keys.skills + '.' + Keys.skill_level2: Condition.skill},
                                 {Keys.skills + '.' + Keys.skill_level3: Condition.skill}]
            conditions[Keys.skills] = {'$regex': Condition.skill}
            """
            conditions[Keys.skills] = {'$all': [x.strip().upper() for x in skills.split(',')]}  # split and strip

        # education background
        c = Condition.range_int(entries.get(Condition.education1), entries.get(Condition.education2))
        if c:
            conditions[Keys.education] = c

        c = Condition.range_int(entries.get(Condition.school_rank), '')
        if c:
            conditions[Keys.edu2 + '.' + Keys.school_rank] = c

        school = entries.get(Condition.school)
        if school:
            conditions[Keys.edu2 + '.' + Keys.schools] = {'$regex': school}

        major = entries.get(Condition.major)
        if major:
            conditions[Keys.edu2 + '.' + Keys.majors] = {'$regex': major}

        # career background
        c = Condition.range_year(entries.get(Condition.year1), entries.get(Condition.year2))
        if c:
            conditions[Keys.year] = c

        c = Condition.range_int(entries.get(Condition.duration1), entries.get(Condition.duration2))
        if c:
            conditions[Keys.duration] = c

        company = entries.get(Condition.company)
        if company:
            conditions[Keys.companies] = {'$regex': company}

        and_list = []
        or_list = []

        experience_keys = entries.get(Condition.experience_keys)
        if experience_keys:
            ek_flag = entries.get(Condition.ek_flag)
            for key in experience_keys.split(','):
                if ek_flag == 'and':
                    and_list.append({Keys.experiences: {'$regex': key.strip()}})
                elif ek_flag == 'or':
                    or_list.append({Keys.experiences: {'$regex': key.strip()}})
                else:
                    raise ValueError

        project_keys = entries.get(Condition.project_keys)
        if project_keys:
            pk_flag = entries.get(Condition.pk_flag)
            for key in project_keys.split(','):
                if pk_flag == 'and':
                    and_list.append({Keys.projects: {'$regex': key.strip()}})
                elif pk_flag == 'or':
                    or_list.append({Keys.projects: {'$regex': key.strip()}})
                else:
                    raise ValueError

        if and_list:
            conditions['$and'] = and_list

        if or_list:
            conditions['$or'] = or_list

        pprint(conditions)
        return conditions


def main():
    entries = Condition.input()
    Condition.create_conditions(entries)


if __name__ == "__main__":
    main()
