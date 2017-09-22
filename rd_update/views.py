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

class Instructions(Page):
	form_model = models.Player
	def get_form_fields(self):
		if self.player.high_acc != self.player.low_acc:
			return ['truefalse1', 'truefalse2', 'truefalse3', 'truefalse4', 'multiple1', 'blank1', 'blank2', 'blank3']
		else:
			return ['truefalse1', 'truefalse2', 'truefalse4', 'blank1', 'blank3']

	def is_displayed(self):
		return self.round_number == 1
	
	def vars_for_template(self):
		return {
			'prior_g': Constants.treatment_dict['good_prior'][self.player.treatment],
			'prior_b': 100 - Constants.treatment_dict['good_prior'][self.player.treatment],
			'high_acc': Constants.treatment_dict['high_acc'][self.player.treatment],
			'high_err': 100 - Constants.treatment_dict['high_acc'][self.player.treatment],
			'low_acc': Constants.treatment_dict['low_acc'][self.player.treatment],
			'low_err': 100 - Constants.treatment_dict['low_acc'][self.player.treatment],
			'senior_prob': Constants.treatment_dict['senior_prob'][self.player.treatment],
			'junior_prob': 100 - Constants.treatment_dict['senior_prob'][self.player.treatment],
		}
	def multiple1_choices(self):
		return [[1, self.player.senior_name], [-1, self.player.junior_name], [0, "I'm equally likely to get each of the two."] ]

	def error_message(self, values):
		if self.player.participant.vars.get('failure') == 0:
			self.player.failures = 0

		summand = 0
		if values["truefalse1"] != True:
			summand += 1
		if values["truefalse2"] != True:
			summand += 1
		if self.player.high_acc != self.player.low_acc and values["truefalse3"] != True:
			summand += 1
		if values["truefalse4"] != True:
			summand += 1
		if self.player.high_acc != self.player.low_acc and values["multiple1"] != (self.player.senior_prob >= 0.5) - (self.player.senior_prob <= 0.5):
			summand += 1
		if values["blank1"] != Constants.treatment_dict['good_prior'][self.player.treatment]:
			summand += 1
		if self.player.high_acc != self.player.low_acc and values["blank2"] != Constants.treatment_dict['high_acc'][self.player.treatment]:
			summand += 1
		if values["blank3"] != 100 - Constants.treatment_dict['low_acc'][self.player.treatment]:
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


class Task(Page):
	form_model = models.Player
	form_fields = ['answer']

	def is_displayed(self):
		return self.player.participant.vars.get('failure') < Constants.failuretolerance   # COMMENT THIS OUT WHEN RUNNING THE EXPERIMENT!!!

	def vars_for_template(self):
		return {
			'prior_g': Constants.treatment_dict['good_prior'][self.player.treatment],
			'prior_b': 100 - Constants.treatment_dict['good_prior'][self.player.treatment],
			'high_acc': Constants.treatment_dict['high_acc'][self.player.treatment],
			'high_err': 100 - Constants.treatment_dict['high_acc'][self.player.treatment],
			'low_acc': Constants.treatment_dict['low_acc'][self.player.treatment],
			'low_err': 100 - Constants.treatment_dict['low_acc'][self.player.treatment],
			'senior_prob': Constants.treatment_dict['senior_prob'][self.player.treatment],
			'junior_prob': 100 - Constants.treatment_dict['senior_prob'][self.player.treatment],
			'senior': self.player.senior,
			'signal': self.player.signal,
			'lottery_odds': self.player.lottery_odds,
			'right_side_odds': [i for i in Constants.right_side_odds if (2 * self.player.signal - 1) * i > (2 * self.player.signal - 1) * Constants.treatment_dict['good_prior'][self.player.treatment]],
			'right_side_start': [i for i in Constants.right_side_odds if (2 * self.player.signal - 1) * i > (2 * self.player.signal - 1) * Constants.treatment_dict['good_prior'][self.player.treatment]][0],
		}

	def before_next_page(self):
		self.player.calculate_bonus()

class Survey(Page):
    form_model = models.Player
    form_fields = ['age', 'education', 'gender', 'major', 'howmuchmturk', 'income', 'howmuchstudies', 'commentsbox']

    def is_displayed(self):
        return self.player.participant.vars.get('failure') < Constants.failuretolerance and self.round_number == Constants.num_rounds



class Results(Page):
    def is_displayed(self):
        return self.player.participant.vars.get('failure') < Constants.failuretolerance and self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'investment': self.player.answer >= self.player.lottery_odds,
			'good': self.player.good,
			'lottery_win': self.player.lottery_win,
			'win': self.player.participant.payoff > 0,
        }



page_sequence = [
	Welcome,
	IRB,
	Instructions,
	sorrybutton2,
	Task,
	Survey,
	Results,
]
