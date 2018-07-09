#! /usr/bin/python3

import abc
from bs4 import BeautifulSoup
from resume import Resume


class ABCParser(abc.ABC):
    def __init__(self, html, file):
        self.html = html
        self.file = file
        self.soup = BeautifulSoup(open(html), 'lxml')

    @abc.abstractclassmethod
    def get_person(self): pass

    @abc.abstractclassmethod
    def get_objective(self): pass

    @abc.abstractclassmethod
    def get_experiences(self): pass

    @abc.abstractclassmethod
    def get_projects(self): pass

    @abc.abstractclassmethod
    def get_educations(self): pass

    @abc.abstractclassmethod
    def get_skills(self): pass

    def new_resume(self):
        return Resume(self.get_person(), self.get_experiences(), self.get_projects(), self.get_educations(),
                      self.get_skills())
