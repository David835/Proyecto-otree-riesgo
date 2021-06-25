from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Welcome(Page):
	pass


class CategoryElicitation(Page):
	form_model = "player"
	form_fields = [
		'cat_end_rel_1', 
		'cat_end_rel_2', 
		'cat_end_rel_3',
		'cat_end_rel_4',
		'cat_end_rel_5',

		'cat_end_abs_1', 
		'cat_end_abs_2', 
		'cat_end_abs_3',
		'cat_end_abs_4',
		'cat_end_abs_5',
	]


class Instructions1(Page):
	form_model = "player"
	form_fields = ["question_1", "question_2"]

	def question_1_error_message(self, value):
		if value == "Incorrecto":
			return "Lea las instrucciones nuevamente con atención y corrija su respuesta"

	def question_2_error_message(self, value):
		if value == "Correcto":
			return "Lea las instrucciones nuevamente con atención y corrija su respuesta."

class Instructions2(Page):
	form_model = "player"
	form_fields = ["question_3", "question_4"]

	def question_3_error_message(self, value):
		if value != 20:
			return "Lea las instrucciones nuevamente con atención y corrija su respuesta."

	def question_4_error_message(self, value):
		if value != 4:
			return "Lea las instrucciones nuevamente con atención y corrija su respuesta."


class Instructions3(Page):
	form_model = "player"
	form_fields = ["question_5", "question_6"]

	def question_5_error_message(self, value):
		if value == "Incorrecto":
			return "Lea las instrucciones nuevamente con atención y corrija su respuesta."

	def question_6_error_message(self, value):
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
		# y luego a través de comunicarme con cada jugador sobre la categoría.
		self.subsession.communicate_categories()


class Agent_0(Page):
	form_model = "player"
	form_fields = ["investments"]

class Agent(Page):
	form_model = "player"
	form_fields = ["decision_for_p1"]

	def vars_for_template(self):
		return {
			'p1_category': self.player.category_from_principal,

			'width_a': self.player.cat_end_abs_1,
			'width_b': self.player.cat_end_abs_2 - self.player.cat_end_abs_1,
			'width_c': self.player.cat_end_abs_3 - self.player.cat_end_abs_2,
			'width_d': self.player.cat_end_abs_4 - self.player.cat_end_abs_3,
			'width_e': self.player.cat_end_abs_5 - self.player.cat_end_abs_4,
		}

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


class Last_Page(Page):
	pass



page_sequence = [
	Welcome,
	CategoryElicitation,
	Instructions1,
	Instructions2,
	Instructions3,
	CategoryPick,
	CategoryWaitPage,
	Agent_0,
	Agent,
	WaitForAgents,
	Results_Principals,
	WaitForPrincipals,
	Results_Agents,
	Last_Page
]
