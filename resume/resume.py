#! /usr/bin/python3


class Objective:
    def __init__(self, spot, salary, field, industry):
        self.spot = spot
        self.salary = salary
        self.field = field
        self.industry = industry

    def __str__(self):
        return self.spot + ', ' + self.salary + ', ' + self.field + ', ' + self.industry


class Person:
    def __init__(self, file, name, gender, birth, phone, email, objective):
        self.file = file
        self.name = name
        self.gender = gender
        self.birth = birth
        self.phone = phone
        self.email = email
        self.objective = objective

    def __str__(self):
        return self.file + '\n' +\
               self.name + ', ' + self.gender + ', ' + self.birth + ', ' + self.phone + ', ' + self.email + '\n' +\
               str(self.objective)

    def insert_cmd(self):
        return 'INSERT OR IGNORE INTO person (file, name, gender, birth, email, phone, spot, salary, field, industry) '\
               + "VALUES ('{}', '{}', '{}', '{}', '{}', {}, '{}', {}, '{}', '{}')".\
                    format(self.file, self.name, self.gender, self.birth, self.email, self.phone,
                           self.objective.spot, self.objective.salary, self.objective.field, self.objective.industry)


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

    def insert_cmd(self, phone):
        return 'INSERT OR IGNORE INTO experience (start_date, end_date, company, company_desc, job, job_desc, phone) '\
               + "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {})".\
                   format(self.start_date, self.end_date, self.company, self.company_desc, self.job, self.job_desc,
                          phone)


class Project:
    def __init__(self, start_date, end_date, project_name, project_desc, job_desc):
        self.start_date = start_date
        self.end_date = end_date
        self.project_name = project_name
        self.project_desc = project_desc
        self.job_desc = job_desc

    def __str__(self):
        return self.start_date + ', ' + self.end_date + ', ' + self.project_name + ', ' + self.project_desc + '\n' + \
               self.job_desc


class Education:
    def __init__(self, start_date, end_date, school, major, degree):
        self.start_date = start_date
        self.end_date = end_date
        self.school = school
        self.major = major
        self.degree = degree

    def __str__(self):
        return self.start_date + ', ' + self.end_date + ', ' + self.school + ', ' + self.major + ', ' + self.degree

    def insert_cmd(self, phone):
        return 'INSERT OR IGNORE INTO education (start_date, end_date, school, major, degree, phone) ' +\
               "VALUES ('{}', '{}', '{}', '{}', '{}', {})".\
                   format(self.start_date, self.end_date, self.school, self.major, self.degree, phone)


class Resume:
    def __init__(self, person, experiences, projects, educations):
        self.person = person
        self.experiences = experiences
        self.projects = projects
        self.educations = educations

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
        return msg

    def insert_cmds(self):
        cmds = [self.person.insert_cmd()]
        for experience in self.experiences:
            cmds.append(experience.insert_cmd(self.person.phone))
        for education in self.educations:
            cmds.append(education.insert_cmd(self.person.phone))
        return cmds
