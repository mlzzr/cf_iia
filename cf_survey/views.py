from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page
from .models import Constants


class Survey(Page):
    form_model = models.Player
    form_fields = ['age', 'education', 'gender', 'major', 'colorblind', 'howmuchmturk', 'income', 'howmuchstudies', 'commentsbox']

    def is_displayed(self):
        return self.player.participant.vars.get('failure') < Constants.failuretolerance

    def before_next_page(self):
        self.player.sum_pay()


class Results(Page):
    def is_displayed(self):
        return self.player.participant.vars.get('failure') < Constants.failuretolerance

    def vars_for_template(self):
        return {
            'bonus_part': self.player.participant.vars['bonus_part'],
            'bonus_round': self.player.participant.vars['bonus_round'],
            'bonus_guess': self.player.participant.vars['bonus_guess'],
            'selected_guess': self.player.selected_guess,
            'lottery_odds': self.player.participant.vars['lottery_odds'],
            'bonus': self.player.participant.vars['bonus']
        }

class DetailResults(Page):
    def is_displayed(self):
        return self.player.participant.vars.get('failure') < Constants.failuretolerance

    def vars_for_template(self):
        return {
            'bonus_part': self.player.participant.vars['bonus_part'],
            'bonus_round': self.player.participant.vars['bonus_round'],
            'bonus_guess': self.player.participant.vars['bonus_guess'],
            'selected_guess': self.player.selected_guess,
            'lottery_odds': self.player.participant.vars['lottery_odds'],
            'bonus': self.player.participant.vars['bonus']
        }


page_sequence = [
    Survey,
    Results
]
