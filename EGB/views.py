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
            'urn_image': 'rect_12/urn1.png',
        }

class PaymentRule(Page):
    def is_displayed(self):
        return self.round_number == 1

class Understanding(Page):
	form_model = models.Player
	def is_displayed(self):
		return self.round_number == 1
	def get_form_fields(self):
		fields_to_show=[]
		for key in range(1,Constants.numberunderstandingquestion1+1):
			fields_to_show.append('truefalse{}'.format(key))
		return fields_to_show
	def error_message(self, values):
		if self.player.participant.vars.get('failure1') == 0:
			self.player.failures = 0

		summand = 0
		if values["truefalse1"] != True:
			summand += 1
		if values["truefalse2"] != True:
			summand += 1
		if values["truefalse3"] != True:
			summand += 1
		if values["truefalse4"] != False:
			summand += 1
		if values["truefalse5"] != True:
			summand += 1
		if values["truefalse6"] != False:
			summand += 1
		if values["truefalse7"] != True:
			summand += 1
		if values["truefalse8"] != False:
			summand += 1
		if summand > 1 and self.player.participant.vars.get('failure1') < Constants.failuretolerance1:
			self.player.participant.vars['failure1'] = 1 + self.player.participant.vars.get('failure1')
			self.player.failures = self.player.failures + 1
			return 'Sorry, you got ' + str(summand) + " questions wrong."
		elif summand == 1 and self.player.participant.vars.get('failure1') < Constants.failuretolerance1:
			self.player.participant.vars['failure1'] = 1 + self.player.participant.vars.get('failure1')
			self.player.failures = self.player.failures  + 1
			return 'Almost there! You just got one question wrong!'


class sorrybutton2(Page):
	form_model = models.Player
	def is_displayed(self):
		if self.player.participant.vars.get('failure1') >= Constants.failuretolerance1:
			self.player.participant.vars['failure'] = Constants.failuretolerance + 5
		return self.player.participant.vars.get('failure') >= Constants.failuretolerance and self.round_number == 1


class Task(Page):
	form_model = models.Player

	def get_form_fields(self):
		form_list = []
		if self.player.blue == 1:
			form_list.append('guess_blue')
		if self.player.black == 1:
			form_list.append('guess_black')
		if self.player.yellow == 1:
			form_list.append('guess_yellow')
		if self.player.green == 1:
			form_list.append('guess_green')
		if self.player.red == 1:
			form_list.append('guess_red')
		return form_list

	# def error_message(self, values):
	# 	for form in form_fields:
	# 		if values[form] > 100 or values[form] < 0 or not isinstance(values[form],int):
	# 			return 'The numbers must be integers between 0 and 100.'

	def is_displayed(self):
		return self.player.participant.vars.get('failure1') < Constants.failuretolerance1   # COMMENT THIS OUT WHEN RUNNING THE EXPERIMENT!!!

	def vars_for_template(self):
		return {
			'urn_image': 'rect_12/urn{}.png'.format(self.player.question_id),
			'blue': self.player.blue,
			'black': self.player.black,
			'yellow': self.player.yellow,
			'green': self.player.green,
			'red': self.player.red,
		}

	def before_next_page(self):
		self.player.calculate_bonus()



# class Posterior(Page):
#     form_model = models.Player
#     form_fields = ['guess2']
#
#     def before_next_page(self):
#         self.player.calculate_bonus()
#
#     def vars_for_template(self):
#         return {
#             'urn_image': 'cf_update/urn{}.pdf'.format(self.player.question_id),
#             'ball_image': 'cf_update/ball_{}.pdf'.format(self.player.ball)
#         }

page_sequence = [
    Welcome,
    IRB,
    Instructions,
    PaymentRule,
    Understanding,
    sorrybutton2,
    Task,
]
