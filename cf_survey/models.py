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
This survey appends the experiment investigating various independence conditions in belief updating.
"""

class Constants(BaseConstants):
    # Basics
    name_in_url = 'yliangStanfordUpdateExperiment3'
    players_per_group = None
    failuretolerance1 = 20  # for understanding questions
    failuretolerance = 10  # for understanding questions
    num_rounds = 1

    # Payoff
    base_pay = c(2)
    complete_bonus = c(1.5)
    high_bonus = c(4.5)
    low_bonus = c(0)
    total_min = base_pay + complete_bonus + low_bonus
    total_max = base_pay + complete_bonus + high_bonus
    ## Probability that the payment is based on the prior belief

    # Only for templates
    IRB = "IRB-42199"

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ### Summary
    complete = models.BooleanField()
    payoff = models.CurrencyField()
    failure = models.PositiveIntegerField()
    failure1 = models.PositiveIntegerField()
    bonus_part = models.PositiveIntegerField()
    bonus_round = models.PositiveIntegerField()
    bonus = models.CurrencyField()
    lottery_odds = models.FloatField()
    lottery_num = models.FloatField()
    lottery_win = models.BooleanField()
    selected_guess = models.PositiveIntegerField()
    ### Demographics
    age = models.PositiveIntegerField(verbose_name='What is your age?', choices=[(0, "< 23"), (1, "23 ~ 30"), (2, "31 ~ 40"), (3, "41~50"), (4, "51 ~ 60"), (5, "61 ~ 70"), (6, "> 70"), (7, "I prefer not to answer")], initial=None)
    gender = models.CharField(initial=None, choices=['Male', 'Female', 'Other', 'I prefer not to answer'], verbose_name='What is your gender?', widget=widgets.RadioSelect())
    colorblind = models.PositiveIntegerField(choices=[(0, 'No'), (1,'Yes'), (2, 'I prefer not to answer')], widget=widgets.RadioSelect(), verbose_name="Did you find it challenging to distinguish between colors?")
    howmuchmturk = models.PositiveIntegerField(verbose_name = "What percentage of your income comes from work on Amazon MTurk?", choices=((0, "0 ~ 10%"), (1, "11 ~ 20%"), (2, "21 ~ 30%"), (3, "31 ~ 40%"), (4, "41 ~ 50%"), (5, "51 ~ 60%"), (6, "61 ~ 70%"), (7, "71 ~ 80%"), (8, "81 ~ 90%"), (9, "91 ~ 100%"), (10, "I prefer not to answer")), initial=None)
    howmuchstudies = models.PositiveIntegerField(initial=None, verbose_name = 'Have you participated in psychological or economics studies before? If so how many?', choices=[(0,"No."), (1,"Yes, one before this study."), (2,"Yes, fewer than five other studies."), (3,"Yes, more than five other studies."), (4,"I prefer not to answer")])
    education = models.PositiveIntegerField(initial=None, verbose_name = "What is your highest level of education?", choices = [(0,"I have no high school diploma"), (1,"High school diploma"), (2,"Some college years"), (3,"Professional further education/ Apprenticeship/ Associate Degree"), (4,"Bachelor's degree"), (5,"Postgraduate degree"), (6,"I prefer not to answer")])
    major = models.CharField(initial=None, blank = True, verbose_name = "If you have some college education, what best describes your major?", choices = ["No College education", "Psychology/ Cognitive Sciences",  "Care Work/ Nursing", "Human Resources/ Communications", "Computer Science/ Engineering/", "Maths/ Phsycis/ Chemistry/ Earth Sciences", "Medicine/ Biology/ Life Sciences", "Economics/ Politics/ Sociology/ Social Sciences", "Langauges/ Literature", "History/ Philosophy/ ", "Art/ Design/ Architecture", "Other/ Not Listed", "I prefer not to answer"])
    commentsbox = models.TextField(initial=None, blank = True, verbose_name = "Do you have any further comments or suggestions?")
    income = models.PositiveIntegerField(verbose_name = 'What is your annual household income?', choices=[(0,"$0 - $10,000"), (1,"$10,001 - $20,000"), (2,"$20,001 - $30,000"), (3, "$30,001 - $45,000"), (4, "$45,001 - $70,000"), (5, "$70,001 - $100,000"), (6, "More than $100,000"), (7, "I prefer not to answer")])

    def sum_pay(self):
        self.participant.vars['complete'] = True
        if self.participant.vars['bonus'] == Constants.high_bonus:
            self.participant.vars['payoff'] = Constants.total_max
        else:
            self.participant.vars['payoff'] = Constants.total_min

        self.complete = self.participant.vars['complete']
        self.payoff = self.participant.vars['payoff']
        self.failure = self.participant.vars['failure']
        self.failure1 = self.participant.vars['failure1']
        self.bonus_part = self.participant.vars['bonus_part']
        self.bonus = self.participant.vars['bonus']
        self.lottery_odds = self.participant.vars['lottery_odds']
        self.lottery_num = self.participant.vars['lottery_num']
        self.lottery_win = self.participant.vars['lottery_win']
        self.bonus_round = self.participant.vars['bonus_round']
        # self.selected_guess = 1
        self.selected_guess = self.participant.vars['selected_guess']
