#! /usr/bin/python3


class Condition:
    spot = industry = field = skill = major = None
    school_rank = education1 = education2 = year1 = year2 = age1 = age2 = None

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
                return num
            print('请输入数字')

    @staticmethod
    def input():
        Condition.spot = Condition.input_string('城市')
        Condition.industry = Condition.input_string('行业')
        Condition.field = Condition.input_string('职业')
        Condition.skill = Condition.input_string('技能')
        Condition.major = Condition.input_string('专业')
        Condition.school_rank = Condition.input_number('毕业学校类别（1:一般 2:211 3:985）')
        Condition.education1 = Condition.input_number('学历下限（含）（1:大专 2:本科 3:硕士 4:MBA 5:EMBA 6:博士 7:博士后）')
        Condition.education2 = Condition.input_number('学历上限（1:大专 2:本科 3:硕士 4:MBA 5:EMBA 6:博士 7:博士后）')
        Condition.year1 = Condition.input_number('工作经验下限（含）（年）')
        Condition.year2 = Condition.input_number('工作经验上限（年）')
        Condition.age1 = Condition.input_number('年龄下限（含）（岁）')
        Condition.age2 = Condition.input_number('年龄上限（岁）')

    @staticmethod
    def __str__():
        return Condition.spot + ', ' + Condition.industry + ', ' + Condition.field + ', ' + Condition.major + ', ' +\
               Condition.school_rank + '\n' + Condition.education1 + '-' + Condition.education2 + ', ' +\
               Condition.year1 + '-' + Condition.year2 + ', ' + Condition.age1 + '-' + Condition.age2

if __name__ == "__main__":
    Condition.input()
    print(Condition.__str__())
