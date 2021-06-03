from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Welcome(Page):
	pass

class CategoryElicitation(Page):
	form_model = "player"

class Instructions1(Page):
	form_model = "player"
	form_fields = ["question_1", "question_2"]

	def question_1_error_message(self, value):
		if value == "Incorrecto":
			return "Lea las instrucciones nuevamente con atención y corrija su respuesta."

	def question_2_error_message(self, value):
		if value == "Correcto":
			return "Lea las instrucciones nuevamente con atención y corrija su respuesta."



class CategoryPick(Page):
	form_model = "player"
	form_fields = ["category"]

	def vars_for_template(self):
		return {
			'width_a': self.player.cat_end_abs_1,
			'width_b': self.player.cat_end_abs_2 - self.player.cat_end_abs_1,
			'width_c': self.player.cat_end_abs_3 - self.player.cat_end_abs_2,
			'width_d': self.player.cat_end_abs_4 - self.player.cat_end_abs_3,
			'width_e': self.player.cat_end_abs_5 - self.player.cat_end_abs_4,
		}


class CategoryWaitPage(WaitPage):
	wait_for_all_groups = True

	def after_all_players_arrive(self):
		self.subsession.set_groups()
	# debido a que wait_for_all_groups está configurado, la función solo se llama una vez, 
	# en consecuencia, tengo que ir un nivel más allá del grupo a la subsesión 
	# en la función llamada en el nivel de subsesión pasa por todos los grupos 
	# y luego a través de comunicarme con cada jugador sobre la categoría
		self.subsession.communicate_categories()


class Agent(Page):
	form_model = "player"
	form_fields = ["decision_for_p1", "decision_for_p2", "decision_for_p3", "decision_for_p4","decision_for_p5"]

	def vars_for_template(self):
		group = self.group.get_players()

		return {
			'p1_category': group[int(self.player.c_principal_1)-1].category, 
			'p2_category': group[int(self.player.c_principal_2)-1].category, 
			'p3_category': group[int(self.player.c_principal_3)-1].category, 
			'p4_category': group[int(self.player.c_principal_4)-1].category, 
			'p5_category': group[int(self.player.c_principal_5)-1].category,

			'width_a': self.player.cat_end_abs_1,
			'width_b': self.player.cat_end_abs_2 - self.player.cat_end_abs_1,
			'width_c': self.player.cat_end_abs_3 - self.player.cat_end_abs_2,
			'width_d': self.player.cat_end_abs_4 - self.player.cat_end_abs_3,
			'width_e': self.player.cat_end_abs_5 - self.player.cat_end_abs_4,
		}
	
	def before_next_page(self):
		self.player.determine_outcome()


class WaitForAgents(WaitPage):

	def after_all_players_arrive(self):
		self.group.after_investments()


class Results_Principals(Page):

	def is_displayed(self):
		return self.player.role() == "Principal"

	form_model = "player"
	form_fields = ["message"]


class WaitForPrincipals(WaitPage):
	def after_all_players_arrive(self):
		self.group.after_results_principals()


class Results_Agents(Page):

	def is_displayed(self):
		return self.player.role() == "Agent"





page_sequence = [
	Welcome,
	CategoryElicitation,
	Instructions1,
	CategoryPick,
	CategoryWaitPage,
	Agent,
	WaitForAgents,
	Results_Principals,
	WaitForPrincipals,
	Results_Agents,
]
