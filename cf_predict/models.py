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
This experiment supplements cf_update to see whether subjects distort objective probabilities.
"""

class Constants(BaseConstants):
    # Basics
    name_in_url = 'yliangStanfordUpdateExperiment2'
    players_per_group = None
    num_parts = 2  # cf_predict and cf_update
    update_prob = 0.8  # prob that cf_update is chosen for payment
    numberunderstandingquestion2 = 4
    failuretolerance1 = 20  # for understanding questions
    failuretolerance = 10  # for understanding questions

    # Questions
    with open('cf_predict/questions_12.csv') as f:
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


    urn_ball_list = ['blue', 'black', 'yellow', 'green', 'red']
    urn1_ball_list = ['blue1', 'black1', 'yellow1', 'green1', 'red1']
    urn2_ball_list = ['blue2', 'black2', 'yellow2', 'green2', 'red2']

    # Payoff
    base_pay = c(2)
    complete_bonus = c(1.5)
    high_bonus = c(4.5)
    low_bonus = c(0)
    total_min = base_pay + complete_bonus + low_bonus
    total_max = base_pay + complete_bonus + high_bonus

    # Only for templates
    IRB = "IRB-42199"
    minutes = 40
    minutes1 = 25
    minutes2 = 10


class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number == 1:
            # Randomizing payment
            for p in self.get_players():
                # p.participant.vars['questions_predict'] = Constants.questions
                p.participant.vars['questions_predict'] = r.sample(Constants.questions, len(Constants.questions))
                if p.participant.vars['bonus_part'] == 2:
                    p.participant.vars['bonus_round'] = r.randrange(Constants.num_rounds) + 1
                    p.participant.vars['bonus_guess'] = np.random.choice([1, 2])

        for p in self.get_players():
            question_data = p.current_question()
            p.question_id = question_data['id']
            [p.prob1, p.prob2] = [question_data[x] for x in ['prob1', 'prob2']]
            [p.size1, p.size2] = [question_data[x] for x in ['size1', 'size2']]
            [p.blue, p.black, p.yellow, p.green, p.red] = [question_data[x] for x in Constants.urn_ball_list]
            [p.blue1, p.black1, p.yellow1, p.green1, p.red1] = [question_data[x] for x in Constants.urn1_ball_list]
            [p.blue2, p.black2, p.yellow2, p.green2, p.red2] = [question_data[x] for x in Constants.urn2_ball_list]
            p.qball = question_data['qball']

            p.urn = np.random.choice(['urn1', 'urn2'], p=[p.prob1, p.prob2])

            if p.urn == 'urn1':
                p.ball = np.random.choice(Constants.urn_ball_list, p=[p.blue1/question_data['size1'], p.black1/question_data['size1'], p.yellow1/question_data['size1'], p.green1/question_data['size1'], p.red1/question_data['size1']])
            else:
                p.ball = np.random.choice(Constants.urn_ball_list, p=[p.blue2/question_data['size2'], p.black2/question_data['size2'], p.yellow2/question_data['size2'], p.green2/question_data['size2'], p.red2/question_data['size2']])

            p.true_guess1 = question_data[p.qball+'1'] / p.size1 * 100
            p.true_guess2 = question_data[p.qball+'2'] / p.size2 * 100



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    question_id = models.PositiveIntegerField()
    prob1 = models.FloatField()
    prob2 = models.FloatField()
    size1 = models.PositiveIntegerField()
    size2 = models.PositiveIntegerField()
    blue1 = models.PositiveIntegerField()
    black1 = models.PositiveIntegerField()
    yellow1 = models.PositiveIntegerField()
    green1 = models.PositiveIntegerField()
    red1 = models.PositiveIntegerField()
    blue2 = models.PositiveIntegerField()
    black2 = models.PositiveIntegerField()
    yellow2 = models.PositiveIntegerField()
    green2 = models.PositiveIntegerField()
    red2 = models.PositiveIntegerField()
    blue = models.PositiveIntegerField()
    black = models.PositiveIntegerField()
    yellow = models.PositiveIntegerField()
    green = models.PositiveIntegerField()
    red = models.PositiveIntegerField()
    urn = models.CharField()
    ball = models.CharField()
    qball = models.CharField()
    guess1 = models.PositiveIntegerField(min=0, max=100)
    guess2 = models.PositiveIntegerField(min=0, max=100)
    true_guess1 = models.FloatField()
    true_guess2 = models.FloatField()
    ## These are variables of players, so they need to be defined under Player. Their values will either be assigned in Subsession or submitted through forms.

    ## Understanding Questions
    failures = models.PositiveIntegerField()
    truefalse1 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="The computer chooses each box with 50% chance.")
    truefalse2 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="Each ball in the selected box is equally likely to be drawn.")
    truefalse3 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name='When being asked the question "How likely do you think that the computer will select Box A AND draw a blue ball from it in this round?", I should assess the odds that both "the computer selects Box A" and "the computer draws a blue ball from Box A" are true statements.')
    truefalse4 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="I'm most likely to receive the extra bonus when I provide my most accurate assessment.")

    def current_question(self):
        return self.participant.vars['questions_predict'][self.round_number - 1]
        # return Constants.questions[self.round_number - 1]
    ## current_question need not be stored in the result table

    def calculate_bonus(self):
        if self.participant.vars['bonus_part'] == 2:
            if self.round_number == self.participant.vars['bonus_round']:
                if self.participant.vars['bonus_guess'] == 1:
                    selected_guess = self.guess1
                    selected_urn = 'urn1'
                else:
                    selected_guess = self.guess2
                    selected_urn = 'urn2'
                if selected_guess < self.participant.vars['lottery_odds']:
                    if self.participant.vars['lottery_win']:
                        self.participant.vars['bonus'] = Constants.high_bonus
                else:
                    if self.urn == selected_urn and self.qball == self.ball:
                        self.participant.vars['bonus'] = Constants.high_bonus
                self.participant.vars['selected_guess'] = selected_guess