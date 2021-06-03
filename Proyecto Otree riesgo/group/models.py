from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import random

class Constants(BaseConstants):
	name_in_url = 'group'
	players_per_group = None
	num_rounds = 1

	category_names = ['sehr konservativ', 'sicherheitsorientiert', 'ausgeglichen', 'wachstumsorientiert', 'offensiv']

	duration = 45

	endowment_principals = c(10)

	# Fixed Compensation
	fixed_payment = c(5)

	#Variable Compensation
	variable_payment = c(5)			# Participación fija para los agentes
	share_result = 25
	share_profit = 35


class Subsession(BaseSubsession):

	def creating_session(self):
		random_number = random.randint(1,2)
		player_list = self.get_players()
		for player in player_list:
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
		group_size = 6
		number_groups = int(total_players / group_size)

		print(cat_lists)

		groups = [[] for i in range(number_groups)]
		temp = []
		for i in range(len(Constants.category_names)):
			for j in range(len(cat_lists[Constants.category_names[i]])):
				temp.append(cat_lists[Constants.category_names[i]][j])
		
		print(temp)
		for i in range(number_groups):
			print(temp[i::number_groups])
			groups[i].append(temp[i::number_groups])

		print([l[0] for l in groups])
		matrix = [l[0] for l in groups]

		# matrix = [[2, 1], [4,3]]


		self.set_group_matrix(matrix)

		print(self.get_group_matrix())

		group_matrix = self.get_group_matrix()
		for group in group_matrix:
			for player in group:
				player.my_group_id = group_matrix.index(group) + 1


	def communicate_categories(self):
		for group in self.get_groups():
			for player in group.get_players():
				player.find_principals()
				player.find_partners()
				player.get_category()


class Group(BaseGroup):
	
	def after_investments(self):
		#self.investment_success = (random.random() <= 1/3)
		for player in self.get_players():
			player.get_investment()
			player.calculate_payoffs_principals()
			player.get_outcome_of_principal()


	def after_results_principals(self):
		for player in self.get_players():
			player.get_invested_amount()
			player.get_msg_payoff_profit()
			player.calculate_payoffs_agents()


class Player(BasePlayer):

	my_group_id = models.IntegerField()

	random_number = models.IntegerField()

	compensation = models.CharField(
		doc="Compensation scheme put in place for agents (see Settings)."
		)

	participation_fee = models.CurrencyField(
		doc="Participation fee for all agents."
		)



	# Los números pares son principales y agentes impares
	def role(self):
		return "Principal" if self.id_in_group % 2 == 0 else "Agent"


# Assign partners (i.e. build principal agent couples: 1-2, 3-4, 5-6)

	partner = models.IntegerField(
		doc="Gives the ID in Group of the partner.")

	def find_partners(self):
		if self.id_in_group == 1:
			self.partner = 2
		elif self.id_in_group == 2:
			self.partner = 1
		elif self.id_in_group == 3:
			self.partner = 4
		elif self.id_in_group == 4:
			self.partner = 3
		elif self.id_in_group == 5:
			self.partner = 6
		elif self.id_in_group == 6:
			self.partner = 5



# Everyone chooses the category:

	category = models.CharField(
		choices=Constants.category_names,
		widget=widgets.RadioSelect(),
		verbose_name="Elija uno de los cinco términos:",
		doc="Principals choose the category which is communicated to their agent"
		)


	category_from_principal = models.CharField(
		doc="Category that agents receive from their principals indicating how they want their agent to invest. Only for the agent who is payoff relevant."
		)


	def get_category(self):
		if self.role() == "Agent":
			principal = self.get_others_in_group()[int(self.partner)-2]
			self.category_from_principal = principal.category



# Part II: Investment for Group members
	
	c_principal_1 = models.IntegerField()
	c_principal_2 = models.IntegerField()
	c_principal_3 = models.IntegerField()
	c_principal_4 = models.IntegerField()
	c_principal_5 = models.IntegerField()

	def find_principals(self):

		# c for corresponding
		if self.id_in_group == 1:
			self.c_principal_1 = 2
			self.c_principal_2 = 3
			self.c_principal_3 = 4
			self.c_principal_4 = 5
			self.c_principal_5 = 6
		elif self.id_in_group == 2:
			self.c_principal_1 = 1
			self.c_principal_2 = 3
			self.c_principal_3 = 4
			self.c_principal_4 = 5
			self.c_principal_5 = 6
		elif self.id_in_group == 3:
			self.c_principal_1 = 1
			self.c_principal_2 = 2
			self.c_principal_3 = 4
			self.c_principal_4 = 5
			self.c_principal_5 = 6
		elif self.id_in_group == 4:
			self.c_principal_1 = 1
			self.c_principal_2 = 2
			self.c_principal_3 = 3
			self.c_principal_4 = 5
			self.c_principal_5 = 6
		elif self.id_in_group == 5:
			self.c_principal_1 = 1
			self.c_principal_2 = 2
			self.c_principal_3 = 3
			self.c_principal_4 = 4
			self.c_principal_5 = 6
		elif self.id_in_group == 6:
			self.c_principal_1 = 1
			self.c_principal_2 = 2
			self.c_principal_3 = 3
			self.c_principal_4 = 4
			self.c_principal_5 = 5


	decision_for_p1 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Nuevo control deslizante
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)
		
	decision_for_p2 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Nuevo control deslizante
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)

	decision_for_p3 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Nuevo control deslizante
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)

	decision_for_p4 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Nuevo control deslizante
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)

	decision_for_p5 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Nuevo control deslizante
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)



# principals can send messages to their agents:

	message = models.CharField(
		choices=["Estoy muy contento con su decisión "," Estoy muy contento con su decisión "," Estoy insatisfecho con su decisión "," Estoy muy insatisfecho con su decisión"],
		widget=widgets.RadioSelect(),
		verbose_name="Para hacer esto, seleccione uno de los mensajes listos para usar:",
		doc="Principals choose the message to send to the agents."
		)


	message_from_principal = models.CharField(
		doc="Message that agents receive from their principals."
		)


# Payoffs:

	investment = models.CurrencyField(
		doc="Indicates for everyone the investment decision as taken by their agents."
		)

	def get_investment(self):
		if self.role() == "Principal":
			agent = self.get_others_in_group()[int(self.partner)-1]
			if self.id_in_group == 2:
				self.investment = agent.decision_for_p1
			if self.id_in_group == 4:
				self.investment = agent.decision_for_p3
			if self.id_in_group == 6:
				self.investment = agent.decision_for_p5


	# Para que los agentes vean sus inversiones para el principal relevante para el pago:

	invested_amount = models.CurrencyField(
		doc="For agents, this gives us the investment in the risky option for their relevant principal (agents own decision).")

	def get_invested_amount(self):
		if self.role() == "Agent":
			principal = self.get_others_in_group()[int(self.partner)-2]
			self.invested_amount = principal.investment




	# Investition in risky asset: Exitoso o no exitoso:
	def determine_outcome(self):
		randomizer = random.randint(1,3)
		if self.role() == "Principal":
			if randomizer == 1:
				self.investment_outcome = 1
			else:
				self.investment_outcome = 0

	investment_outcome = models.IntegerField(
		doc="Turns 1 if the investment was successful and 0 in case it was not."
		)


	# Get outcome of the principals as a variable for the agents:

	outcome_of_principal = models.IntegerField(
		doc="Message that agents receive from their principals."
		)

	def get_outcome_of_principal(self):
		if self.role() == "Agent":
			principal = self.get_others_in_group()[int(self.partner)-2]
			self.outcome_of_principal = principal.investment_outcome



	def calculate_payoffs_principals(self):
		if self.role() == "Principal":
			if self.investment_outcome == 1:
				self.payoff = self.investment * 3.5 + (Constants.endowment_principals - self.investment)
				self.profit = self.investment * 2.5
			elif self.investment_outcome == 0:
				self.payoff = Constants.endowment_principals - self.investment
				self.profit = 0


	profit = models.CurrencyField(
		doc="Gives the profit of the principal."
		)

	payoff_of_principal = models.CurrencyField(
		doc="Gives for each agent the payoff of his principal."
		)

	profit_of_principal = models.CurrencyField(
		doc="Gives for each agent the payoff of his principal."
		)


	def get_msg_payoff_profit(self):
		if self.role() == "Agent":
			principal = self.get_others_in_group()[int(self.partner)-2]
			self.profit_of_principal = principal.profit
			self.payoff_of_principal = principal.payoff
			self.message_from_principal = principal.message


	def calculate_payoffs_agents(self):
		if self.role() == "Agent":
			if self.compensation == "fixed":
				self.payoff = Constants.fixed_payment
			if self.compensation == "variable_result":
				self.payoff = Constants.variable_payment + Constants.share_result/100 * self.payoff_of_principal
			if self.compensation == "variable_profit":
				self.payoff = Constants.variable_payment + Constants.share_profit/100 * self.profit_of_principal



	# Comprehension Questions
	question_1 = models.CharField(
		widget=widgets.RadioSelectHorizontal(),
		choices=["Correcto","Incorrecto"])

	question_2 = models.CharField(
		widget=widgets.RadioSelectHorizontal(),
		choices=["Correcto","Incorrecto"])

	question_3 = models.CurrencyField()

	question_4 = models.CurrencyField()

	question_5 = models.CharField(
		widget=widgets.RadioSelectHorizontal(),
		choices=["Correcto","Incorrecto"])

	question_6 = models.CharField(widget=widgets.RadioSelectHorizontal(), choices=["Correcto","Incorrecto"])





	