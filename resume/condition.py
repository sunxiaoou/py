#! /usr/bin/python3

from datetime import datetime
from pprint import pprint
from resume import Keys


class Condition:
    spot = industry = field = company = skill = school = school_rank = major = None
    education1 = education2 = year1 = year2 = age1 = age2 = None

    @staticmethod
    def input_string(title):
        print('请输入' + title + ':')
        str = input()
        return str if str else None

    @staticmethod
    def input_number(title):
        while True:
            print('请输入' + title + ':')
            num = input()
            if not num:
                return None
            if num.isdecimal():
                return int(num)
            print('请输入数字')

    @staticmethod
    def input():
        Condition.spot = Condition.input_string('城市')
        Condition.industry = Condition.input_string('行业')
        Condition.field = Condition.input_string('职业')
        Condition.company = Condition.input_string('（前）雇主')
        Condition.skill = Condition.input_string('技能')
        if Condition.skill is not None:
            Condition.skill = Condition.skill.upper()
        Condition.school = Condition.input_string('学校')
        Condition.school_rank = Condition.input_number('毕业学校类别（1:一般 2:211 3:985）')
        Condition.major = Condition.input_string('专业')
        Condition.education1 = Condition.input_number('学历（1:大专 2:本科 3:硕士 4:MBA 5:EMBA 6:博士 7:博士后）以上（含）')
        Condition.education2 = Condition.input_number('学历（1:大专 2:本科 3:硕士 4:MBA 5:EMBA 6:博士 7:博士后）以下')
        Condition.year1 = Condition.input_number('工作经验_年以上（含）')
        Condition.year2 = Condition.input_number('工作经验_年以下')
        Condition.age1 = Condition.input_number('年龄_岁以上（含）')
        Condition.age2 = Condition.input_number('年龄_岁以下')

    @staticmethod
    def __str__():
        return Condition.spot + ', ' + Condition.industry + ', ' + Condition.field + ', ' + Condition.major + ', ' +\
               Condition.school_rank + '\n' + Condition.education1 + '-' + Condition.education2 + ', ' +\
               Condition.year1 + '-' + Condition.year2 + ', ' + Condition.age1 + '-' + Condition.age2

    @staticmethod
    def range_int(num1, num2):
        if num1 is None and num2 is None:
            return None

        if num1 is not None and num1 == num2:
            return num1

        conditions = {}
        if num1 is not None:
            conditions['$gte'] = num1
        if num2 is not None:
            conditions['$lt'] = num2
        return conditions

    @staticmethod
    def range_date(num1, num2):
        if num1 is None and num2 is None:
            return None

        today = datetime.today()
        if num1 is not None and num1 == num2:
            return datetime(today.year - num1, today.month, today.day)

        conditions = {}
        if num2 is not None:
            conditions['$gte'] = datetime(today.year - num2, today.month, today.day)
        if num1 is not None:
            conditions['$lt'] = datetime(today.year - num1, today.month, today.day)
        return conditions

    @staticmethod
    def create_conditions():
        Condition.input()

        conditions = {}
        if Condition.spot is not None:
            conditions[Keys.spots] = Condition.spot
        if Condition.industry is not None:
            conditions[Keys.industries] = {'$regex': Condition.industry}
        if Condition.field is not None:
            conditions[Keys.fields] = {'$regex': Condition.field}
        if Condition.company is not None:
            conditions[Keys.companies] = {'$regex': Condition.company}
        if Condition.skill is not None:
            """
            conditions['$or'] = [{Keys.skills + '.' + Keys.skill_level2: Condition.skill},
                                 {Keys.skills + '.' + Keys.skill_level3: Condition.skill}]
            """
            conditions[Keys.skills] = {'$regex': Condition.skill}
        if Condition.school is not None:
            conditions[Keys.educations + '.' + Keys.schools] = {'$regex': Condition.school}
        if Condition.school_rank is not None:
            conditions[Keys.educations + '.' + Keys.school_rank] = Condition.school_rank
        if Condition.major is not None:
            conditions[Keys.educations + '.' + Keys.majors] = {'$regex': Condition.major}

        c = Condition.range_int(Condition.education1, Condition.education2)
        if c is not None:
            conditions[Keys.education] = c

        c = Condition.range_int(Condition.year1, Condition.year2)
        if c is not None:
            conditions[Keys.years] = c

        c = Condition.range_date(Condition.age1, Condition.age2)
        if c is not None:
            conditions[Keys.birth] = c

        pprint(conditions)
        return conditions


if __name__ == "__main__":
    Condition.create_conditions()
