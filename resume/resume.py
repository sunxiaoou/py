#! /usr/local/bin/python3

from schools import Schools


class Keys:
    spots = '期望工作地点'
    salary = '期望月薪'
    fields = '期望从事职业'
    industries = '期望从事行业'
    file = 'file'
    timestamp = 'timestamp'
    name = '姓名'
    gender = '性别'
    birth = '出生日期'
    phone = '手机号码'
    email = '电子邮箱'
    education = '学历'
    enrollment = '招生方式'
    year = '参加工作年份'
    companies = '雇主'
    educations = '教育经历'
    edu2 = '教育经历2'
    school = schools = '学校'
    major = majors = '专业'
    degree = degrees = '学位'
    school_rank = '学校类别'
    languages = '语言能力'
    skills = '技能'
    skill_level1 = '一般'
    skill_level2 = '熟练'
    skill_level3 = '精通'
    experiences = '工作经历'
    duration = '最长一次工作年限'
    start_date = '开始日期'
    end_date = '结束日期'
    company = '雇主'
    company_desc = '雇主描述'
    job = '岗位'
    job_desc = '岗位描述'
    projects = '项目经历'
    project = '项目'
    project_desc = '项目描述'
    duty = '责任描述'


class Objective:
    def __init__(self, spots, salary, fields, industries):
        self.spots = spots
        self.salary = salary
        self.fields = fields
        self.industries = industries

    def to_dictionary(self):
        objective = {}
        if self.spots:
            objective[Keys.spots] = self.spots
        if self.salary:
            objective[Keys.salary] = self.salary
        if self.fields:
            objective[Keys.fields] = self.fields
        if self.industries:
            objective[Keys.industries] = self.industries
        return objective


class Person:
    def __init__(self, file, timestamp, name, gender, birth, phone, email, education, enrollment, year, objective):
        self.file = file
        self.timestamp = timestamp
        self.name = name
        self.gender = gender
        self.birth = birth
        self.phone = phone
        self.email = email
        self.education = education
        self.enrollment = enrollment
        self.year = year
        self.objective = objective

    def to_dictionary(self):
        person = {Keys.file: self.file, Keys.timestamp: self.timestamp, Keys.name: self.name, Keys.gender: self.gender,
                  Keys.birth: self.birth, Keys.phone: self.phone}
        if self.email:
            person[Keys.email] = self.email
        if self.education:
            person[Keys.education] = self.education
        if self.enrollment:
            person[Keys.enrollment] = self.enrollment
        if self.year:
            person[Keys.year] = self.year
        return {**person, **self.objective.to_dictionary()}     # merge 2 dictionaries


class Experience:
    def __init__(self, start_date, end_date, company, company_desc, job, job_desc):
        self.start_date = start_date
        self.end_date = end_date
        self.company = company
        self.company_desc = company_desc
        self.job = job
        self.job_desc = job_desc

    def to_dictionary(self):
        return {Keys.start_date: self.start_date, Keys.end_date: self.end_date, Keys.company: self.company,
                Keys.company_desc: self.company_desc, Keys.job: self.job, Keys.job_desc: self.job_desc}


class Project:
    def __init__(self, start_date, end_date, name, description, duty):
        self.start_date = start_date
        self.end_date = end_date
        self.name = name
        self.description = description
        self.duty = duty

    def to_dictionary(self):
        return {Keys.start_date: self.start_date, Keys.end_date: self.end_date, Keys.project: self.name,
                Keys.project_desc: self.description, Keys.duty: self.duty}


class Education:
    educationList = ['大专', '本科', '硕士', 'MBA', 'EMBA', '博士',  '博士后']

    def __init__(self, start_date, end_date, school, major, degree):
        self.start_date = start_date
        self.end_date = end_date
        self.school = school
        self.major = major
        self.degree = degree

    def to_dictionary(self):
        return {Keys.start_date: self.start_date, Keys.end_date: self.end_date, Keys.school: self.school,
                Keys.major: self.major, Keys.degree: self.degree}


class Edu2:
    def __init__(self, educations):
        self.schools = []
        self.majors = []
        # self.degrees = []
        for education in educations:
            self.schools.append(education.school)
            self.majors.append(education.major)
            # self.degrees.append(education.degree)
        self.school_rank = 0
        for school in self.schools:
            rank = Schools.get_rank(school)
            if rank > self.school_rank:
                self.school_rank = rank

    def to_dictionary(self):
        return {Keys.schools: self.schools, Keys.majors: self.majors, Keys.school_rank: self.school_rank}

"""
class Skills:
    def __init__(self, level1, level2, level3):
        self.level1 = level1
        self.level2 = level2
        self.level3 = level3

    def __str__(self):
        return ' '.join(self.level1) + '\n' + ' '.join(self.level2) + '\n' + ' '.join(self.level3)

    def to_dictionary(self):
        skills = {}
        if self.level1 is not None:
            skills[Keys.skill_level1] = self.level1
        if self.level2 is not None:
            skills[Keys.skill_level2] = self.level2
        if self.level3 is not None:
            skills[Keys.skill_level3] = self.level3
        return skills
"""


class Resume:
    def __init__(self, person, experiences, projects, educations, languages, skills):
        self.person = person
        self.experiences = experiences
        self.projects = projects
        self.educations = educations
        self.languages = languages
        self.skills = skills

    def to_dictionary(self, list2str):
        if not self.person.year:
            end_years = []
            if self.educations:
                for education in self.educations:
                    end_years.append(education.end_date.year)
                self.person.year = max(end_years)
            else:
                self.person.year = self.person.timestamp.year

        if not self.person.education:
            degrees = []
            if self.educations:
                for education in self.educations:
                    degrees.append(education.degree)
                self.person.education = max(degrees)
            # else:
            #    self.person.education = 0

        resume = self.person.to_dictionary()

        if self.experiences:
            companies = []
            durations = []
            experiences = []
            for experience in self.experiences:
                companies.append(experience.company)
                if experience.end_date and experience.start_date:
                    durations.append(experience.end_date.year - experience.start_date.year)
                experiences.append(experience.to_dictionary())
            if companies:
                resume[Keys.companies] = companies
            if durations:
                resume[Keys.duration] = max(durations)
            if not list2str:
                resume[Keys.experiences] = experiences
            else:
                resume[Keys.experiences] = str(experiences)

        if self.projects:
            projects = []
            for project in self.projects:
                projects.append(project.to_dictionary())
            if not list2str:
                resume[Keys.projects] = projects
            else:
                resume[Keys.projects] = str(projects)

        if self.educations:
            educations = []
            for education in self.educations:
                educations.append(education.to_dictionary())
            if not list2str:
                resume[Keys.educations] = educations
            else:
                resume[Keys.educations] = str(educations)
            resume[Keys.edu2] = Edu2(self.educations).to_dictionary()

        if self.languages:
            resume[Keys.languages] = self.languages

        if self.skills:
            resume[Keys.skills] = self.skills
        return resume
