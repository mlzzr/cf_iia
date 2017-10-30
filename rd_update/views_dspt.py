from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page
from .models import Constants


class Welcome(Page):
	def is_displayed(self):
		return self.round_number == 1

class IRB(Page):
	def is_displayed(self):
		return self.round_number == 1

class Instructions_dspt(Page):
	form_model = models.Player
	form_fields = ['truefalse1', 'truefalse2', 'truefalse3', 'truefalse4', 'blank1', 'blank2', 'blank3']


	def is_displayed(self):
		return self.round_number == 1
	
	def vars_for_template(self):
		return {
			'prior_g': Constants.good_prior,
			'prior_b': 100 - Constants.good_prior,
			'acc': Constants.acc,
			'err': 100 - Constants.acc,
			'senior_highbound': self.player.senior_dice_num,
			'senior_lowbound': self.player.senior_dice_num + 1,
			'junior_highbound': self.player.junior_dice_num,
			'junior_lowbound': self.player.junior_dice_num + 1,
		}

	def error_message(self, values):
		if self.player.participant.vars.get('failure') == 0:
			self.player.failures = 0

		summand = 0
		if values["truefalse1"] != True:
			summand += 1
		if values["truefalse2"] != True:
			summand += 1
		if values["truefalse3"] != True:
			summand += 1
		if values["truefalse4"] != True:
			summand += 1
		if values["blank1"] != Constants.good_prior:
			summand += 1
		if values["blank2"] != Constants.acc:
			summand += 1
		if values["blank3"] != 100 - Constants.acc:
			summand += 1
		if summand > 1 and self.player.participant.vars.get('failure') < Constants.failuretolerance:
			self.player.participant.vars['failure'] = 1 + self.player.participant.vars.get('failure')
			self.player.failures = self.player.failures + 1
			return 'Sorry, you got ' + str(summand) + " questions wrong."
		elif summand == 1 and self.player.participant.vars.get('failure') < Constants.failuretolerance:
			self.player.participant.vars['failure'] = 1 + self.player.participant.vars.get('failure')
			self.player.failures = self.player.failures  + 1
			return 'Almost there! You just got one question wrong!'


class sorrybutton2(Page):
	form_model = models.Player
	def is_displayed(self):
		return self.player.participant.vars.get('failure') >= Constants.failuretolerance and self.round_number == 1

class Dice(Page):

	def is_displayed(self):
		return self.player.participant.vars.get('failure') < Constants.failuretolerance   # COMMENT THIS OUT WHEN RUNNING THE EXPERIMENT!!!

	def vars_for_template(self):
		return {
			'senior_highbound': self.player.senior_dice_num,
			'senior_lowbound': self.player.senior_dice_num + 1,
			'junior_highbound': self.player.junior_dice_num,
			'junior_lowbound': self.player.junior_dice_num + 1,
			'senior': self.player.senior,
		}


class Task_dspt(Page):
	form_model = models.Player
	form_fields = ['investment']

	def is_displayed(self):
		return self.player.participant.vars.get('failure') < Constants.failuretolerance   # COMMENT THIS OUT WHEN RUNNING THE EXPERIMENT!!!

	def vars_for_template(self):
		return {
			'prior_g': Constants.good_prior,
			'prior_b': 100 - Constants.good_prior,
			'acc': Constants.acc,
			'err': 100 - Constants.acc,
			'senior': self.player.senior,
			'signal': self.player.signal,
			'lottery_odds': self.player.lottery_odds,
		}

	def before_next_page(self):
		self.player.calculate_bonus()

class Survey(Page):
    form_model = models.Player
    form_fields = ['age', 'education', 'gender', 'major', 'howmuchmturk', 'income', 'howmuchstudies', 'commentsbox']

    def is_displayed(self):
        return self.player.participant.vars.get('failure') < Constants.failuretolerance and self.round_number == Constants.num_rounds



class Results_dspt(Page):
    def is_displayed(self):
        return self.player.participant.vars.get('failure') < Constants.failuretolerance and self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'investment': self.player.investment,
			'good': self.player.good,
			'lottery_win': self.player.lottery_win,
			'win': self.player.participant.payoff > 0,
        }



page_sequence = [
	Welcome,
	IRB,
	Instructions_dspt,
	sorrybutton2,
	Dice,
	Task_dspt,
	Survey,
	Results_dspt,
]
