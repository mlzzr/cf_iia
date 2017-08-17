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
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
			'example_question': self.player.question_text,
			'example_chart': 'EGB/chart{}.png'.format(self.player.question_id),
			'threshold_0': Constants.threshold_0 * 100,
			'threshold_1': Constants.threshold_1 * 100,
		}


class Understanding(Page):
	form_model = models.Player
	form_fields = ['truefalse1', 'truefalse2', 'truefalse3']
	def is_displayed(self):
		return self.round_number == 1
	# def get_form_fields(self):
	# 	fields_to_show=[]
	# 	for key in range(1,Constants.numberunderstandingquestion1+1):
	# 		fields_to_show.append('truefalse{}'.format(key))
	# 	return fields_to_show
	def vars_for_template(self):
		return{
			'question_chart': 'EGB/chart2.png',
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
		return self.player.participant.vars.get('failure') < Constants.failuretolerance

	def vars_for_template(self):
		return {
			'round': self.round_number,
			'question': self.player.question_text,
			'chart': 'EGB/chart{}.png'.format(self.player.question_id),
		}

	def before_next_page(self):
		self.player.calculate_bonus()

class Survey(Page):
    form_model = models.Player
    form_fields = ['age', 'education', 'gender', 'major', 'howmuchmturk', 'income', 'howmuchstudies', 'calculator', 'software', 'commentsbox']

    def is_displayed(self):
        return self.player.participant.vars.get('failure') < Constants.failuretolerance and self.round_number == Constants.num_rounds



class Results(Page):
    def is_displayed(self):
        return self.player.participant.vars.get('failure') < Constants.failuretolerance and self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'bonus': self.player.participant.payoff,
			'total_pay': self.player.participant.payoff_plus_participation_fee
        }


page_sequence = [
    Welcome,
    IRB,
    Instructions,
    Understanding,
    sorrybutton2,
    Task,
	Survey,
	Results,
]
