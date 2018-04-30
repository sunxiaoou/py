#! /usr/bin/python3


class Person:
    def __init__(self, file, name, gender, birth, phone, email):
        self.file = file
        self.name = name
        self.gender = gender
        self.birth = birth
        self.phone = phone
        self.email = email

    def __str__(self):
        return self.file + '\n' +\
               self.name + ', ' + self.gender + ', ' + self.birth + ', ' + self.phone + ', ' + self.email

    def insert_cmd(self):
        return 'INSERT OR IGNORE INTO person (file, name, gender, birth, email, phone) ' +\
               "VALUES ('{}', '{}', '{}', '{}', '{}', {})".\
                    format(self.file, self.name, self.gender, self.birth, self.email, self.phone)


class Objective:
    def __init__(self, spot, salary, field, industry):
        self.spot = spot
        self.salary = salary
        self.field = field
        self.industry = industry

    def __str__(self):
        return self.spot + '\n' + self.salary + '\n' + self.field + '\n' + self.industry

    def insert_cmd(self, phone):
        return 'INSERT OR IGNORE INTO objective (spot, salary, field, industry, phone) ' +\
               "VALUES ('{}', {}, '{}', '{}', {})".format(self.spot, self.salary, self.field, self.industry, phone)


class Experience:
    def __init__(self, start_date, end_date, company, job):
        self.start_date = start_date
        self.end_date = end_date
        self.company = company
        self.job = job

    def __str__(self):
        return self.start_date + ', ' + self.end_date + ', ' + self.company + ', ' + self.job

    def insert_cmd(self, phone):
        return 'INSERT OR IGNORE INTO experience (start_date, end_date, company, job, phone) ' +\
               "VALUES ('{}', '{}', '{}', '{}', {})".\
                   format(self.start_date, self.end_date, self.company, self.job, phone)


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
    def __init__(self, person, objective, experiences, educations):
        self.person = person
        self.objective = objective
        self.experiences = experiences
        self.educations = educations

    def __str__(self):
        msg = 'Person:\n' + str(self.person) + '\n'
        msg = msg + 'Objective:\n' + str(self.objective) + '\n'
        msg += 'Experiences:\n'
        for experience in self.experiences:
            msg = msg + str(experience) + '\n'
        msg += 'Educations:\n'
        for education in self.educations:
            msg = msg + str(education) + '\n'
        return msg

    def insert_cmds(self):
        cmds = [self.person.insert_cmd(), self.objective.insert_cmd(self.person.phone)]
        for experience in self.experiences:
            cmds.append(experience.insert_cmd(self.person.phone))
        for education in self.educations:
            cmds.append(education.insert_cmd(self.person.phone))
        return cmds
