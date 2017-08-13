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
This experiment investigates various independence conditions in belief updating using the strategy method.
"""

class Constants(BaseConstants):
    # Basics
    name_in_url = 'yliangStanfordUpdateExperiment4'
    players_per_group = None
    num_parts = 2  # cf_strategy and cf_predict
    update_prob = 0.8  # prob that cf_strategy is chosen for payment
    failuretolerance1 = 20  # for understanding questions
    failuretolerance = 10  # for understanding questions
    numberunderstandingquestion1 = 8

    # Questions
    with open('cf_strategy/questions_12.csv') as f:
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
    button_label = 'Draw a ball from it!'
    update_question = 'Now that you know the color of the ball, how likely do you think that the selected box in this round was Box A?'


class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number == 1:
            for p in self.get_players():
                # p.participant.vars['questions_update'] = Constants.questions
                p.participant.vars['questions_update'] = r.sample(Constants.questions, len(Constants.questions))
                p.participant.vars['complete'] = False
                p.participant.vars['payoff'] = Constants.base_pay
                p.participant.vars['failure'] = 0
                p.participant.vars['failure1'] = 0
                p.participant.vars['bonus_part'] = np.random.choice(Constants.num_parts, p=[Constants.update_prob, 1 - Constants.update_prob]) + 1
                p.participant.vars['bonus'] = Constants.low_bonus
                p.participant.vars['lottery_odds'] = r.randrange(100) + 0.5
                ## The selected lottery to be compared with the guess
                p.participant.vars['lottery_num'] = r.random() * 100
                ## The lottery number to be compared with lottery_odds if lottery is implemented
                p.participant.vars['lottery_win'] = p.participant.vars['lottery_odds'] > p.participant.vars['lottery_num']
                ## The result of the lottery

                if p.participant.vars['bonus_part'] == 1:
                    p.participant.vars['bonus_round'] = r.randrange(Constants.num_rounds) + 1
                    p.participant.vars['bonus_guess'] = 1

        for p in self.get_players():
            question_data = p.current_question()
            p.question_id = question_data['id']
            [p.prob1, p.prob2] = [question_data[x] for x in ['prob1', 'prob2']]
            [p.size1, p.size2] = [question_data[x] for x in ['size1', 'size2']]
            [p.blue, p.black, p.yellow, p.green, p.red] = [question_data[x] for x in Constants.urn_ball_list]
            [p.blue1, p.black1, p.yellow1, p.green1, p.red1] = [question_data[x] for x in Constants.urn1_ball_list]
            [p.blue2, p.black2, p.yellow2, p.green2, p.red2] = [question_data[x] for x in Constants.urn2_ball_list]

            p.urn = np.random.choice(['urn1', 'urn2'], p=[p.prob1, p.prob2])

            if p.urn == 'urn1':
                p.ball = np.random.choice(Constants.urn_ball_list, p=[p.blue1/question_data['size1'], p.black1/question_data['size1'], p.yellow1/question_data['size1'], p.green1/question_data['size1'], p.red1/question_data['size1']])
            else:
                p.ball = np.random.choice(Constants.urn_ball_list, p=[p.blue2/question_data['size2'], p.black2/question_data['size2'], p.yellow2/question_data['size2'], p.green2/question_data['size2'], p.red2/question_data['size2']])




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
    guess1 = models.PositiveIntegerField(min=0, max=100)
    guess_blue = models.PositiveIntegerField(min=0, max=100)
    guess_black = models.PositiveIntegerField(min=0, max=100)
    guess_yellow = models.PositiveIntegerField(min=0, max=100)
    guess_green = models.PositiveIntegerField(min=0, max=100)
    guess_red = models.PositiveIntegerField(min=0, max=100)


    ## Understanding Questions
    failures = models.PositiveIntegerField()
    truefalse1 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="The computer chooses each box with 50% chance.")
    truefalse2 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="Each ball in the selected box is equally likely to be drawn.")
    truefalse3 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="I will not see the ball that is drawn by the computer, but Bob will.")
    truefalse4 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="Sometimes, Bob will give a different answer than the one I instruct him to give.")
    truefalse5 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="I'm most likely to get the extra bonus if I instruct Bob to report my best guess under every circumstance.")
    truefalse6 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="I can choose which question counts for payment at the end of the survey.")
    truefalse7 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="The experimenter has no influence on which question is counted for the extra bonus. All randomization is made by the computer. Only one question in one part is randomly selected to count for the extra bonus.")
    truefalse8 = models.BooleanField(choices=[[1, 'True'], [0, 'False']], widget=widgets.RadioSelect(),
                                     verbose_name="The computer selects the question to count for payment that is least profitable for me.")

    def current_question(self):
        return self.participant.vars['questions_update'][self.round_number - 1]
    ## current_question need not be stored in the result table

    def calculate_bonus(self):
        guess = {'blue': self.guess_blue, 'black': self.guess_black, 'yellow': self.guess_yellow, 'green': self.guess_green, 'red': self.guess_red}
        self.guess1 = guess[self.ball]
        if self.participant.vars['bonus_part'] == 1:
            if self.round_number == self.participant.vars['bonus_round']:
                if self.guess1 < self.participant.vars['lottery_odds']:
                    if self.participant.vars['lottery_win']:
                        self.participant.vars['bonus'] = Constants.high_bonus
                else:
                    if self.urn == 'urn1':
                        self.participant.vars['bonus'] = Constants.high_bonus
                self.participant.vars['selected_guess'] = self.guess1
