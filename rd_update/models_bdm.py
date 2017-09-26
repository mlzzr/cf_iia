from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from os import urandom
import random as r
import numpy as np
import csv
import itertools


author = 'Yucheng Liang'

doc = """
This experiment investigates various independence conditions in belief updating.
"""

class Constants(BaseConstants):
    # Basics
    name_in_url = 'yliangStanfordUpdateExperiment5'
    players_per_group = None
    failuretolerance = 8  # for understanding questions

    # Treatments
    treatment_dict = {
        'senior_prob': [50, 50, 50, 20, 90],
        'good_prior': [40, 40, 40, 40, 40],
        'high_acc': [75, 90, 75, 75, 75],
        'low_acc': [75, 75, 60, 60, 60],
    }
    num_treatments = len(treatment_dict['senior_prob'])
    num_rounds = 1
    session_treatments = [1, 1, 1, 0, 0]
    sample_sizes = [50, 100, 100, 250, 60]
    treatment_prob = [a*b for a, b in zip(session_treatments, sample_sizes)] / np.dot(session_treatments, sample_sizes)

    # BDM
    num_rows = 20
    right_side_odds = [98 - i * 5 for i in range(num_rows)]
    selection_prob = [.02, .02, .02, .02, .02, .02, .02, .02, .08, .08, .08, .08, .08, .08, .08, .08, .08, .08, .02, .02]

    # Payoff
    base_pay = c(0.5)
    complete_bonus = c(0)
    high_bonus = c(1)
    low_bonus = c(0)
    total_min = base_pay + complete_bonus + low_bonus
    total_max = base_pay + complete_bonus + high_bonus

    # Only for templates
    IRB = "IRB-42199"
    minutes = 8
    good_message = '"The investment is Good."'
    bad_message = '"The investment is Bad."'
    name_list = ['Bob', 'Mike']

class Subsession(BaseSubsession):
    # def creating_session(self):
    #     treatments = itertools.cycle(range(Constants.num_treatments))
    #     for p in self.get_players():
    #         p.treatment = next(treatments)
    def before_session_starts(self):
        if self.round_number == 1:
            # treatments = itertools.cycle(range(Constants.num_treatments))
            # for p in self.get_players():
            #     p.treatment = next(treatments)
            for p in self.get_players():
                p.treatment = np.random.choice(Constants.num_treatments, p=Constants.treatment_prob)
                p.participant.vars['failure'] = 0
                p.senior_name, p.junior_name = np.random.permutation(Constants.name_list)
                p.high_acc = Constants.treatment_dict['high_acc'][p.treatment] / 100
                p.low_acc = Constants.treatment_dict['low_acc'][p.treatment] / 100
                p.senior_prob = Constants.treatment_dict['senior_prob'][p.treatment] / 100
                p.good_prior = Constants.treatment_dict['good_prior'][p.treatment] / 100
                p.senior = np.random.binomial(1, p.senior_prob)
                p.acc = p.senior * p.high_acc + (1 - p.senior) * p.low_acc
                p.good = np.random.binomial(1, p.good_prior)
                if p.senior:
                    if p.good: 
                        p.signal = np.random.binomial(1, p.high_acc)
                    else:
                        p.signal = np.random.binomial(1, 1 - p.high_acc)
                    if p.signal:
                        p.posterior = (p.good_prior * p.high_acc) / (p.good_prior * p.high_acc + (1 - p.good_prior) * (1 - p.high_acc))
                    else:
                        p.posterior = (p.good_prior * (1 - p.high_acc)) / (p.good_prior * (1 - p.high_acc) + (1 - p.good_prior) * p.high_acc)
                else:
                    if p.good:
                        p.signal = np.random.binomial(1, p.low_acc)
                    else:
                        p.signal = np.random.binomial(1, 1 - p.low_acc)
                    if p.signal:
                        p.posterior = (p.good_prior * p.low_acc) / (p.good_prior * p.low_acc + (1 - p.good_prior) * (1 - p.low_acc))
                    else:
                        p.posterior = (p.good_prior * (1 - p.low_acc)) / (p.good_prior * (1 - p.low_acc) + (1 - p.good_prior) * p.low_acc)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.PositiveIntegerField()
    senior_name = models.CharField()
    junior_name = models.CharField()
    senior_prob = models.FloatField()
    high_acc = models.FloatField()
    low_acc = models.FloatField()
    good_prior = models.FloatField()
    senior = models.BooleanField()
    acc = models.FloatField()
    good = models.BooleanField()
    signal = models.BooleanField()
    posterior = models.FloatField()
    lottery_odds = models.PositiveIntegerField()
    lottery_win = models.BooleanField()
    answer = models.IntegerField()




    ## Understanding Questions
    failures = models.PositiveIntegerField()
    truefalse1 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect())
    truefalse2 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect())
    truefalse3 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect())
    truefalse4 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect())
    multiple1 = models.IntegerField(widget=widgets.RadioSelect())
    blank1 = models.PositiveIntegerField()
    blank2 = models.PositiveIntegerField()
    blank3 = models.PositiveIntegerField()

    ## Survey Questions
    age = models.PositiveIntegerField(verbose_name='What is your age?', choices=[(0, "< 23"), (1, "23 ~ 30"), (2, "31 ~ 40"), (3, "41~50"), (4, "51 ~ 60"), (5, "61 ~ 70"), (6, "> 70"), (7, "I prefer not to answer")], initial=None)
    gender = models.CharField(initial=None, choices=['Male', 'Female', 'Other', 'I prefer not to answer'], verbose_name='What is your gender?', widget=widgets.RadioSelect())
    howmuchmturk = models.PositiveIntegerField(verbose_name = "What percentage of your income comes from work on Amazon MTurk?", choices=((0, "0 ~ 10%"), (1, "11 ~ 20%"), (2, "21 ~ 30%"), (3, "31 ~ 40%"), (4, "41 ~ 50%"), (5, "51 ~ 60%"), (6, "61 ~ 70%"), (7, "71 ~ 80%"), (8, "81 ~ 90%"), (9, "91 ~ 100%"), (10, "I prefer not to answer")), initial=None)
    howmuchstudies = models.PositiveIntegerField(initial=None, verbose_name = 'Have you participated in psychological or economics studies before? If so how many?', choices=[(0,"No."), (1,"Yes, one before this study."), (2,"Yes, fewer than five other studies."), (3,"Yes, more than five other studies."), (4,"I prefer not to answer")])
    education = models.PositiveIntegerField(initial=None, verbose_name = "What is your highest level of education?", choices = [(0,"I have no high school diploma"), (1,"High school diploma"), (2,"Some college years"), (3,"Professional further education/ Apprenticeship/ Associate Degree"), (4,"Bachelor's degree"), (5,"Postgraduate degree"), (6,"I prefer not to answer")])
    major = models.CharField(initial=None, blank = True, verbose_name = "If you have some college education, what best describes your major?", choices = ["No College education", "Psychology/ Cognitive Sciences",  "Care Work/ Nursing", "Human Resources/ Communications", "Computer Science/ Engineering/", "Maths/ Phsycis/ Chemistry/ Earth Sciences", "Medicine/ Biology/ Life Sciences", "Economics/ Politics/ Sociology/ Social Sciences", "Langauges/ Literature", "History/ Philosophy/ ", "Art/ Design/ Architecture", "Other/ Not Listed", "I prefer not to answer"])
    commentsbox = models.TextField(initial=None, blank = True, verbose_name = "Do you have any further comments or suggestions?")
    income = models.PositiveIntegerField(verbose_name = 'What is your annual household income?', choices=[(0,"$0 - $10,000"), (1,"$10,001 - $20,000"), (2,"$20,001 - $30,000"), (3, "$30,001 - $45,000"), (4, "$45,001 - $70,000"), (5, "$70,001 - $100,000"), (6, "More than $100,000"), (7, "I prefer not to answer")])


    def calculate_bonus(self):
        self.lottery_odds = np.random.choice(Constants.right_side_odds, p=Constants.selection_prob)
        self.lottery_win = np.random.binomial(1, self.lottery_odds / 100)
        if self.answer >= self.lottery_odds:
            self.participant.payoff = Constants.high_bonus * self.good
        else:
            self.participant.payoff = Constants.high_bonus * self.lottery_win
