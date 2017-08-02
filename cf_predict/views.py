from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page
from .models import Constants

class Transition(Page):
    def is_displayed(self):
        return self.player.participant.vars.get('failure1') < Constants.failuretolerance1 and self.round_number == 1

class Instructions(Page):
    def is_displayed(self):
        return self.player.participant.vars.get('failure1') < Constants.failuretolerance1 and self.round_number == 1

    def vars_for_template(self):
        return{'predict_question': "ins_predict_question.png"}

class PaymentRule(Page):
    def is_displayed(self):
        return self.player.participant.vars.get('failure1') < Constants.failuretolerance1 and self.round_number == 1

class Understanding(Page):
	form_model = models.Player
	def is_displayed(self):
		return self.player.participant.vars.get('failure1') < Constants.failuretolerance1 and self.round_number == 1
	def get_form_fields(self):
		fields_to_show=[]
		for key in range(1,Constants.numberunderstandingquestion2+1):
			fields_to_show.append('truefalse{}'.format(key))
		return fields_to_show
	def error_message(self, values):
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
		if summand > 1 and self.player.participant.vars.get('failure') < Constants.failuretolerance:
			self.player.participant.vars['failure'] = 1 + self.player.participant.vars.get('failure')
			self.player.failures = self.player.failures + 1
			return 'Sorry, you got ' + str(summand) + " questions wrong."
		elif summand == 1 and self.player.participant.vars.get('failure') < Constants.failuretolerance:
			self.player.participant.vars['failure'] = 1 + self.player.participant.vars.get('failure')
			self.player.failures = self.player.failures + 1
			return 'Almost there! You just got one question wrong!'


class sorrybutton2(Page):
	form_model = models.Player
	def is_displayed(self):
		return self.player.participant.vars.get('failure1') < Constants.failuretolerance1 and self.player.participant.vars.get('failure') >= Constants.failuretolerance and self.round_number == 1

class Task(Page):
    form_model = models.Player
    form_fields = ['guess1', 'guess2']

    def is_displayed(self):
        return self.player.participant.vars.get('failure1') < Constants.failuretolerance1 and self.player.participant.vars.get('failure') < Constants.failuretolerance

    def before_next_page(self):
        self.player.calculate_bonus()

    def vars_for_template(self):
        return {
            'urn_image': 'rect_messy_12/urn{}.pdf'.format(self.player.question_id),
        }



page_sequence = [
    Transition,
    Instructions,
    PaymentRule,
    Understanding,
    sorrybutton2,
    Task
]
