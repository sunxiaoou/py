#! /usr/bin/python3


class Objective:
    def __init__(self, spot, salary, fields, industries):
        self.spot = spot
        self.salary = salary
        self.fields = fields
        self.industries = industries

    def __str__(self):
        return self.spot + ', ' + self.salary + ', ' + self.fields + ', ' + self.industries

    def to_dictionary(self):
        return {'期望工作地点': self.spot, '期望月薪': self.salary, '期望从事职业': self.fields,
                '期望从事行业': self.industries}


class Person:
    def __init__(self, file, name, gender, birth, phone, email, education, years, objective):
        self.file = file
        self.name = name
        self.gender = gender
        self.birth = birth
        self.phone = phone
        self.email = email
        self.education = education
        self.years = years
        self.objective = objective

    def __str__(self):
        return self.file + '\n' +\
               self.name + ', ' + self.gender + ', ' + self.birth + ', ' + self.phone + ', ' + self.email + '\n' +\
               self.education + self.years + str(self.objective)

    def to_dictionary(self):
        person = {'file': self.file, '姓名': self.name, '性别': self.gender, '出生日期': self.birth,
                  '手机号码': self.phone, '电子邮箱': self.email, '学历': self.education, '工作经验': self.years}
        return {**person, **self.objective.to_dictionary()}     # merge 2 dictionaries


class Experience:
    def __init__(self, start_date, end_date, company, company_desc, job, job_desc):
        self.start_date = start_date
        self.end_date = end_date
        self.company = company
        self.company_desc = company_desc
        self.job = job
        self.job_desc = job_desc

    def __str__(self):
        return self.start_date + ', ' + self.end_date + ', ' + self.company + ', ' + self.company_desc + '\n' +\
               self.job + ', ' + self.job_desc

    def to_dictionary(self):
        return {'开始日期': self.start_date, '结束日期': self.end_date, '单位': self.company,
                '单位描述': self.company_desc, '岗位': self.job, '岗位描述': self.job_desc}


class Project:
    def __init__(self, start_date, end_date, name, description, duty):
        self.start_date = start_date
        self.end_date = end_date
        self.name = name
        self.description = description
        self.duty = duty

    def to_dictionary(self):
        return {'开始日期': self.start_date, '结束日期': self.end_date, '项目': self.name, '项目描述': self.description,
                '责任描述': self.duty}

    def __str__(self):
        return self.start_date + ', ' + self.end_date + ', ' + self.name + ', ' + self.description + '\n' + \
               self.duty


class Education:
    def __init__(self, start_date, end_date, school, major, degree):
        self.start_date = start_date
        self.end_date = end_date
        self.school = school
        self.major = major
        self.degree = degree

    def __str__(self):
        return self.start_date + ', ' + self.end_date + ', ' + self.school + ', ' + self.major + ', ' + self.degree

    def to_dictionary(self):
        return {'开始日期': self.start_date, '结束日期': self.end_date, '学校': self.school, '专业': self.major,
                '学位': self.degree}


class Skill:
    def __init__(self, name, grade, time):
        self.name = name
        self.grade = grade
        self.time = time

    def __str__(self):
        return self.name + ', ' + self.grade + ', ' + self.time

    def to_dictionary(self):
        return {'技能': self.name, '程度': self.grade, '使用时间': self.time}


class Resume:
    def __init__(self, person, experiences, projects, educations, skills):
        self.person = person
        self.experiences = experiences
        self.projects = projects
        self.educations = educations
        self.skills = skills

    def __str__(self):
        msg = 'Person:\n' + str(self.person) + '\n'
        msg += 'Experiences:\n'
        for experience in self.experiences:
            msg = msg + str(experience) + '\n'
        msg += 'Projects:\n'
        for project in self.projects:
            msg = msg + str(project) + '\n'
        msg += 'Educations:\n'
        for education in self.educations:
            msg = msg + str(education) + '\n'
        msg += 'Skills:\n'
        for skill in self.skills:
            msg = msg + str(skill) + '\n'
        return msg

    def to_dictionary(self):
        resume = self.person.to_dictionary()
        resume['工作经历'] = []
        for experience in self.experiences:
            resume['工作经历'].append(experience.to_dictionary())
        resume['项目经验'] = []
        for project in self.projects:
            resume['项目经验'].append(project.to_dictionary())
        resume['教育经历'] = []
        for education in self.educations:
            resume['教育经历'].append(education.to_dictionary())
        resume['技能'] = []
        for skill in self.skills:
            resume['技能'].append(skill.to_dictionary())
        return resume
