from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import random

author = 'yo =v '

doc = """
Risk Taking for Others Experiment 2018
"""


class Constants(BaseConstants):
	name_in_url = 'single'
	players_per_group = None
	num_rounds = 1


	category_names = ['muy conservador', 'conservador', 'equilibrado', 'enfocado al crecimiento', 'ofensivo']

	duration = 45

	endowment_principals = c(10)


	# Fixed Compensation
	fixed_payment = c(5)

	#Variable Compensation
	share_result = 25				# En porcentaje
	share_profit = 35

class Subsession(BaseSubsession):

	def creating_session(self):
		random_number = random.randint(1,2)
		for player in self.get_players():
			player.compensation = self.session.config["compensation"]
			player.participation_fee = self.session.config["participation_fee"]
			player.random_number = random_number
	
	def set_groups(self):
		# Create category lists
		cat_lists = dict.fromkeys(Constants.category_names)
		for element in cat_lists:
			cat_lists[element] = []

		# sort players into category lists by their choices
		for player in self.get_players():
			for cat_name in cat_lists:
				if player.category == cat_name:
					cat_lists[cat_name].append(player)
					

		total_players = len(self.get_players())
		group_size = 2
		number_groups = int(total_players / group_size)

		# print(cat_lists)

		groups = [[] for i in range(number_groups)]
		temp = []
		for i in range(len(Constants.category_names)):
			for j in range(len(cat_lists[Constants.category_names[i]])):
				temp.append(cat_lists[Constants.category_names[i]][j])
		
		# print(temp)
		for i in range(number_groups):
			#print(temp[i::number_groups])
			groups[i].append(temp[i::number_groups])

		# CK: I am not sure what you are doing here
		# print([l[0] for l in groups])		# hace un corchete menos
		matrix = [l[0] for l in groups]

		self.set_group_matrix(matrix)
		# print(self.get_group_matrix())

		# let players know which group they are in
		group_matrix = self.get_group_matrix()
		for group in group_matrix:
			for player in group:
				player.my_group_id = group_matrix.index(group) + 1 #probablemente porque aparece al inicio


	def communicate_categories(self):
		for group in self.get_groups():
			for player in group.get_players():
				player.get_category()


class Group(BaseGroup):
	investment_success = models.BooleanField(doc="Turns true if the investment was successful and 0 in case it was not.")
	
	def after_investments(self):
		self.investment_success = (random.random() <= 1/3)
		for player in self.get_players():
			player.get_investment()
			player.calculate_payoffs_principals()

	def after_results_principals(self):
		for player in self.get_players():
			player.get_msg_payoff_profit()
			player.calculate_payoffs_agents()


class Player(BasePlayer):
	
	my_group_id = models.PositiveIntegerField(doc="Gives each player his group ID (see subsession)")

	random_number = models.IntegerField(doc="Turns either 1 or 2 (see subsession) and is used to randomly assign roles in the experiment (see def role).")

	compensation = models.CharField(doc="Compensation scheme put in place for agents (see Settings).")

	participation_fee = models.CurrencyField(doc="Participation fee for all agents (can be modified in Settings).")

	def role(self):
		return "Principal" if self.id_in_group == self.random_number else "Agent"

# Everyone chooses the category:

	category = models.CharField(
		choices=Constants.category_names,
		verbose_name="Un consultor debería invertir mis activos por mí de la siguiente manera:"
		, doc = "Los directores eligen la categoría que se comunica a su agente")


	category_from_principal = models.CharField(
		doc="Category that agents receive from their principals indicating how they want their agent to invest.")


	def get_category(self):
		self.category_from_principal = self.get_others_in_group()[0].category


# Everyone takes the investment decision for their principal:

	decision_for_p1 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					
		verbose_name="Su decisión de inversión para su cliente:", 
		doc = "Inversión de agentes para el principal en el activo de riesgo." )

	investment = models.CurrencyField(doc="Indicates for everyone the investment decision as taken by their agents.")

	def get_investment(self):
		agent = self.get_others_in_group()[0]
		self.investment = agent.decision_for_p1


# principals can send messages to their agents:

	message = models.CharField(
		choices=["Estoy muy satisfecho con su decisión", "Estoy satisfecho con su decisión"
		, "Estoy insatisfecho con su decisión", "Estoy muy insatisfecho con su decisión"],
		widget=widgets.RadioSelect(),
		verbose_name="Para hacer esto, seleccione uno de los mensajes listos para usar:"
		, doc = "Los directores eligen el mensaje para enviar a los agentes.")

	message_from_principal = models.CharField(doc="Message that agents receive from their principals.")


# Payoffs:
	def calculate_payoffs_principals(self):
		if self.role() == "Principal":
			if self.group.investment_success:
				self.payoff = self.investment * 3.5 + (Constants.endowment_principals - self.investment)
				self.profit = self.investment * 2.5
			else:
				self.payoff = Constants.endowment_principals - self.investment
				self.profit = 0

	profit = models.CurrencyField(doc="Gives the profit of the principal.")

	payoff_of_principal = models.CurrencyField(doc="Gives for each agent the payoff of his principal.")


	profit_of_principal = models.CurrencyField(doc="Gives for each agent the payoff of his principal.")


	def get_msg_payoff_profit(self):
		principal = self.get_others_in_group()[0]
		self.profit_of_principal = principal.profit
		self.payoff_of_principal = principal.payoff
		self.message_from_principal = principal.message


	def calculate_payoffs_agents(self):
		if self.role() == "Agent":
			if self.compensation == "fixed":
				self.payoff = Constants.fixed_payment
			if self.compensation == "variable_result":
				self.payoff = Constants.fixed_payment + Constants.share_result/100 * self.payoff_of_principal
			if self.compensation == "variable_profit":
				self.payoff = Constants.fixed_payment + Constants.share_profit/100 * self.profit_of_principal


	# Comprehension Questions
	question_1 = models.CharField(
		widget=widgets.RadioSelectHorizontal(),
		choices=["Correcto ", "Incorrecto"])

	question_2 = models.CharField(
		widget=widgets.RadioSelectHorizontal(),
		choices=["Correcto ", "Incorrecto"])

	question_3 = models.CurrencyField()

	question_4 = models.CurrencyField()

	question_5 = models.CharField(
		widget=widgets.RadioSelectHorizontal(),
		choices=["Correcto ", "Incorrecto"])

	question_6 = models.CharField(widget=widgets.RadioSelectHorizontal(), choices=["Correcto ", "Incorrecto"])



	# fields for risk elicitation

	cat_end_rel_1 = models.FloatField(
		doc="Indicates the end point of the first category in relative size.")

	cat_end_rel_2 = models.FloatField(
		doc="Indicates the end point of the second category in relative size.")

	cat_end_rel_3 = models.FloatField(
		doc="Indicates the end point of the third category in relative size.")

	cat_end_rel_4 = models.FloatField(
		doc="Indicates the end point of the fourth category in relative size.")

	cat_end_rel_5 = models.FloatField(
		doc="Indicates the end point of the fifth category in relative size.")

	cat_end_abs_1 = models.PositiveIntegerField(
		doc="Indicates the end point of the first category in pixels.")

	cat_end_abs_2 = models.PositiveIntegerField(
		doc="Indicates the end point of the second category in pixels.")

	cat_end_abs_3 = models.PositiveIntegerField(
		doc="Indicates the end point of the third category in pixels.")

	cat_end_abs_4 = models.PositiveIntegerField(
		doc="Indicates the end point of the fourth category in pixels.")

	cat_end_abs_5 = models.PositiveIntegerField(
		doc="Indicates the end point of the fifth category in pixels.")


	
