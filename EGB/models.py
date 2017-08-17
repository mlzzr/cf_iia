from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from os import urandom
import random as r
import numpy as np
import csv


author = 'Yucheng Liang'

doc = """
This survey investigates how people discount future income flows.
"""

class Constants(BaseConstants):
    # Basics
    name_in_url = 'dbernheimStanfordEGBSurvey1'
    players_per_group = None
    failuretolerance = 6  # for understanding questions
    numberunderstandingquestion1 = 3

    # Questions
    with open('EGB/questions.csv') as f:
        questions = list(csv.DictReader(f))
    for item in questions:
        for key in item:
            try:
                try:
                    item[key] = int(item[key])
                except ValueError:
                    item[key] = float(item[key])
            except ValueError:
                pass

    num_rounds = len(questions)

    # Payoff
    base_pay = c(2)

    bonus_0 = c(0)
    bonus_1 = c(0.2)
    bonus_2 = c(0.5)
    
    threshold_0 = 0.3
    threshold_1 = 0.1

    high_bonus = c(5.5)
    low_bonus = c(0)
    total_min = base_pay + low_bonus
    total_max = base_pay + high_bonus

    # Only for templates
    IRB = "IRB-41767"
    minutes = 30

class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number == 1:
            for p in self.get_players():
                ind1 = r.sample([1, 2], 2)
                ind2 = r.sample([3, 4], 2)
                ind3 = r.sample([5, 6], 2)
                ind4 = r.sample([7, 8], 2)
                ind5 = r.sample([9, 10], 2)
                ind = [0] + ind1 + ind2 + ind3 + ind4 + ind5
                p.participant.vars['questions'] = [Constants.questions[i] for i in ind]
                p.participant.vars['complete'] = False
                p.participant.payoff = 0
                p.participant.vars['failure'] = 0

        for p in self.get_players():
            question_data = p.current_question()
            p.question_id = question_data['id']
            p.question_text = question_data['question']
            p.rate = question_data['rate']
            p.withdraw = question_data['withdraw']
            p.start = question_data['start']
            p.end = question_data['end']
            p.correct = p.withdraw / ((1 + p.rate) ** p.start) * (1 - 1/ ((1 + p.rate) ** (p.end - p.start + 1))) / (1 - 1 / (1 + p.rate))
            p.lt = 0
            for t in range(p.start, p.end + 1):
                p.lt += p.withdraw / (1 + p.rate * t)
            p.two_step = p.withdraw / p.rate / (1 + p.rate * (p.start - 1)) - p.withdraw / p.rate / (1 + p.rate * (p.end - p.start + 1)) / (1 + p.rate * (p.start - 1))
            p.one_step = p.withdraw / p.rate / (1 + p.rate * (p.start - 1)) - p.withdraw / p.rate / (1 + p.rate * p.end)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    question_id = models.PositiveIntegerField()
    question_text = models.CharField()
    rate = models.FloatField()
    withdraw = models.FloatField()
    start = models.FloatField()
    end = models.FloatField()
    answer = models.FloatField(min=0)
    correct = models.FloatField()
    lt = models.FloatField()
    two_step = models.FloatField()
    one_step = models.FloatField()


    ## Understanding Questions
    failures = models.PositiveIntegerField()
    truefalse1 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="Each question will count for payment.")
    truefalse2 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="If my answer to a question is too far from the correct answer, I may not get any reward for that question.")
    truefalse3 = models.BooleanField(choices=[[1, '10'], [0, '11']], widget=widgets.RadioSelect(), verbose_name='')

    ## Survey Questions
    age = models.PositiveIntegerField(verbose_name='What is your age?', choices=[(0, "< 23"), (1, "23 ~ 30"), (2, "31 ~ 40"), (3, "41~50"), (4, "51 ~ 60"), (5, "61 ~ 70"), (6, "> 70"), (7, "I prefer not to answer")], initial=None)
    gender = models.CharField(initial=None, choices=['Male', 'Female', 'Other', 'I prefer not to answer'], verbose_name='What is your gender?', widget=widgets.RadioSelect())
    calculator = models.PositiveIntegerField(choices=[(0, 'No'), (1,'Yes'), (2, 'I prefer not to answer')], widget=widgets.RadioSelect(), verbose_name="Did you use a calculator when you answered the questions?")
    software = models.PositiveIntegerField(choices=[(0, 'No'), (1,'Yes'), (2, 'I prefer not to answer')], widget=widgets.RadioSelect(), verbose_name="Did you use any software with pre-programmed financial calculator when you answered the questions?")
    howmuchmturk = models.PositiveIntegerField(verbose_name = "What percentage of your income comes from work on Amazon MTurk?", choices=((0, "0 ~ 10%"), (1, "11 ~ 20%"), (2, "21 ~ 30%"), (3, "31 ~ 40%"), (4, "41 ~ 50%"), (5, "51 ~ 60%"), (6, "61 ~ 70%"), (7, "71 ~ 80%"), (8, "81 ~ 90%"), (9, "91 ~ 100%"), (10, "I prefer not to answer")), initial=None)
    howmuchstudies = models.PositiveIntegerField(initial=None, verbose_name = 'Have you participated in psychological or economics studies before? If so how many?', choices=[(0,"No."), (1,"Yes, one before this study."), (2,"Yes, fewer than five other studies."), (3,"Yes, more than five other studies."), (4,"I prefer not to answer")])
    education = models.PositiveIntegerField(initial=None, verbose_name = "What is your highest level of education?", choices = [(0,"I have no high school diploma"), (1,"High school diploma"), (2,"Some college years"), (3,"Professional further education/ Apprenticeship/ Associate Degree"), (4,"Bachelor's degree"), (5,"Postgraduate degree"), (6,"I prefer not to answer")])
    major = models.CharField(initial=None, blank = True, verbose_name = "If you have some college education, what best describes your major?", choices = ["No College education", "Psychology/ Cognitive Sciences",  "Care Work/ Nursing", "Human Resources/ Communications", "Computer Science/ Engineering/", "Maths/ Phsycis/ Chemistry/ Earth Sciences", "Medicine/ Biology/ Life Sciences", "Economics/ Politics/ Sociology/ Social Sciences", "Langauges/ Literature", "History/ Philosophy/ ", "Art/ Design/ Architecture", "Other/ Not Listed", "I prefer not to answer"])
    commentsbox = models.TextField(initial=None, blank = True, verbose_name = "Do you have any further comments or suggestions?")
    income = models.PositiveIntegerField(verbose_name = 'What is your annual household income?', choices=[(0,"$0 - $10,000"), (1,"$10,001 - $20,000"), (2,"$20,001 - $30,000"), (3, "$30,001 - $45,000"), (4, "$45,001 - $70,000"), (5, "$70,001 - $100,000"), (6, "More than $100,000"), (7, "I prefer not to answer")])

    def current_question(self):
        return self.participant.vars['questions'][self.round_number - 1]
    ## current_question need not be stored in the result table

    def calculate_bonus(self):
        if abs(self.answer - self.correct) < Constants.threshold_1 * self.correct:
            self.participant.payoff += Constants.bonus_2
        elif abs(self.answer - self.correct) < Constants.threshold_0 * self.correct:
            self.participant.payoff += Constants.bonus_1
